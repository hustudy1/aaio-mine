#!/usr/bin/env python3
"""Stop hook — 세션 종료 시 transcript scan 후 환류 3 type 분류.

발견된 이벤트를 shared_data/outbox/openorchestrator-upstream/feedback/<id>.json 작성.
해당 없으면 조용히 종료.

본 hook 은 starter fork 본인 환경에서만 동작. 사용자 OO 본체 영향 0.

Transcript 형식 (Claude Code JSONL):
    각 line = {"type": "user|assistant|...", "message": {"content": ...}}
    content 는 string 또는 list (text/tool_use/tool_result blocks).
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
OUTBOX_DIR = REPO_ROOT / "shared_data" / "outbox" / "openorchestrator-upstream" / "feedback"


PATTERNS: dict[str, list[tuple[str, str]]] = {
    "protocol_proposal": [
        (r"schema\s*(?:가|이)?\s*(?:부족|gap|missing|새 필드|추가 필요)", "schema gap"),
        (r"protocol\s*(?:이)?\s*(?:진화|개선|propose)\s*(?:해야|필요)", "protocol evolution"),
        (r"task JSON.{0,30}(?:field|필드).{0,20}(?:필요|추가)", "task JSON field addition"),
        (r"새\s*카테고리\s*(?:가)?\s*필요", "new category needed"),
        (r"(?:schema|spec)\s*(?:v1|버전)\s*(?:업|update|개선)", "schema version update"),
    ],
    "incident": [
        (r"hook\s*(?:이)?\s*(?:차단|block|reject|fail(?:ed)?)", "hook failure"),
        (r"schema\s*validation\s*(?:실패|invalid|fail(?:ed)?)", "schema validation failed"),
        (r"dispatch\s*loop", "dispatch loop"),
        (r"silent\s*failure", "silent failure"),
        (r"unexpected\s*(?:error|exception)", "unexpected error"),
        (r"redaction\s*(?:fail|miss|leaked?)", "redaction failure"),
        (r"PII\s*(?:leaked?|exposed)", "PII leaked"),
    ],
    "decision_request": [
        (r"사용자\s*(?:에게)?\s*(?:결정|승인)\s*(?:요청|필요)", "user decision needed"),
        (r"human\s*(?:approval|review)\s*(?:required|needed)", "human approval required"),
        (r"PR\s*(?:머지|merge)\s*(?:결정|approval)\s*(?:필요|needed)", "PR merge approval"),
        (r"외부\s*(?:라이브러리|dependency)\s*추가\s*(?:해도|승인)", "external dependency approval"),
        (r"비용\s*(?:발생|승인)\s*(?:필요|결정)", "cost approval"),
    ],
}


def parse_transcript(transcript_path: Path) -> list[dict]:
    """JSONL transcript 를 list of message entries 로 parse."""
    entries: list[dict] = []
    for line in transcript_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def extract_text(entry: dict) -> str:
    """message entry 에서 text 추출 (assistant text · user message · tool_result 모두)."""
    msg = entry.get("message", {})
    content = msg.get("content")
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for block in content:
        if not isinstance(block, dict):
            continue
        block_type = block.get("type")
        if block_type == "text":
            parts.append(block.get("text", ""))
        elif block_type == "tool_result":
            result = block.get("content", "")
            if isinstance(result, str):
                parts.append(result)
            elif isinstance(result, list):
                for r in result:
                    if isinstance(r, dict) and r.get("type") == "text":
                        parts.append(r.get("text", ""))
        elif block_type == "tool_use":
            tool_input = block.get("input", {})
            if isinstance(tool_input, dict):
                parts.append(json.dumps(tool_input, ensure_ascii=False))
    return "\n".join(parts)


def detect_events(entries: list[dict]) -> list[dict]:
    """transcript entry list 에서 환류 후보 이벤트 추출."""
    events: list[dict] = []
    for idx, entry in enumerate(entries):
        text = extract_text(entry)
        if not text:
            continue
        for event_type, patterns in PATTERNS.items():
            for pattern, description in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if not match:
                    continue
                context_before = extract_text(entries[idx - 1]) if idx > 0 else ""
                context_after = extract_text(entries[idx + 1]) if idx + 1 < len(entries) else ""
                events.append({
                    "type": event_type,
                    "description": description,
                    "pattern": pattern,
                    "matched_text": match.group(0)[:200],
                    "entry_index": idx,
                    "entry_type": entry.get("type", "unknown"),
                    "context_before": context_before[-200:] if context_before else "",
                    "context_after": context_after[:200] if context_after else "",
                })
    return events


def deduplicate(events: list[dict]) -> list[dict]:
    """같은 type + pattern 의 중복 이벤트 제거 (첫 occurrence 유지)."""
    seen: set[tuple[str, str]] = set()
    unique: list[dict] = []
    for ev in events:
        key = (ev["type"], ev["pattern"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(ev)
    return unique


def build_body(event: dict) -> dict:
    """type 별 body schema (feedback-v1.json oneOf) 정합 형태로 구성."""
    event_type = event["type"]
    if event_type == "protocol_proposal":
        return {
            "current_schema_version": "1.0",
            "affected_fields": [],
            "use_case": event["description"],
            "proposed_change": f"matched: {event['matched_text']}",
        }
    if event_type == "incident":
        return {
            "occurred_at": datetime.now(timezone.utc).isoformat(),
            "component": event.get("entry_type", "unknown"),
            "failure_mode": event["description"],
            "repro_fixture": f"context: {event['context_before']} ... [matched] {event['matched_text']} ... {event['context_after']}",
        }
    if event_type == "decision_request":
        return {
            "question": event["description"],
            "options": [],
            "waiting_on_task_id": "unknown",
            "deadline": None,
        }
    return {"raw": event}


def write_feedback(event: dict, self_name: str = "starter-self") -> Path:
    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
    feedback_id = f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid4().hex[:8]}"
    intent = f"환류 후보 감지 — {event['type']}: {event['description']}"
    payload = {
        "schema_version": "1.0",
        "feedback_id": feedback_id,
        "type": event["type"],
        "intent": intent,
        "from": self_name,
        "ts": datetime.now(timezone.utc).isoformat(),
        "body": build_body(event),
    }
    target = OUTBOX_DIR / f"{feedback_id}.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return target


def main() -> int:
    transcript = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if transcript is None or not transcript.exists():
        return 0
    entries = parse_transcript(transcript)
    if not entries:
        return 0
    events = detect_events(entries)
    if not events:
        return 0
    unique = deduplicate(events)
    written = 0
    for ev in unique:
        write_feedback(ev)
        written += 1
    print(
        f"feedback-classifier: {written} feedback "
        f"(from {len(events)} matches, {len(unique)} unique) "
        f"written to {OUTBOX_DIR}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
