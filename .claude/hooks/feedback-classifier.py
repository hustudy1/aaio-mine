#!/usr/bin/env python3
"""Stop hook — 세션 동안 발생한 이벤트 scan 후 환류 3 type 분류.

발견 이벤트가 protocol_proposal / incident / decision_request 중 어디 해당 시
shared_data/outbox/openorchestrator-upstream/feedback/<id>.json 자동 작성.
해당 없으면 조용히 종료.

본 hook 은 starter fork 본인 환경에서만 동작. 사용자 OO 본체는 본 hook 영향 0.
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


PATTERNS = {
    "protocol_proposal": [
        r"schema.{0,20}(부족|gap|missing|새 필드|추가 필요)",
        r"protocol.{0,20}(진화|개선|propose)",
        r"task JSON.{0,30}(field|필드).{0,20}필요",
    ],
    "incident": [
        r"hook.{0,20}(차단|block|reject)",
        r"schema.{0,20}(validation 실패|invalid|fail)",
        r"dispatch loop",
        r"silent failure",
    ],
    "decision_request": [
        r"사용자.{0,20}(결정|승인) 필요",
        r"human.{0,20}required",
        r"approval.{0,20}needed",
    ],
}


def detect_events(transcript_text: str) -> list[dict]:
    """Transcript 에서 환류 후보 이벤트 추출."""
    events = []
    for event_type, patterns in PATTERNS.items():
        for pattern in patterns:
            matches = re.findall(pattern, transcript_text, re.IGNORECASE)
            for m in matches:
                events.append({
                    "type": event_type,
                    "matched_text": m if isinstance(m, str) else str(m),
                    "pattern": pattern,
                })
    return events


def write_feedback(event_type: str, body: dict, intent: str, self_name: str = "starter-self") -> Path:
    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
    feedback_id = f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid4().hex[:8]}"
    payload = {
        "schema_version": "1.0",
        "feedback_id": feedback_id,
        "type": event_type,
        "intent": intent,
        "from": self_name,
        "ts": datetime.now(timezone.utc).isoformat(),
        "body": body,
    }
    target = OUTBOX_DIR / f"{feedback_id}.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return target


def main() -> int:
    transcript = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if transcript is None or not transcript.exists():
        return 0
    text = transcript.read_text(encoding="utf-8", errors="replace")
    events = detect_events(text)
    if not events:
        return 0
    written = 0
    for ev in events:
        body_skeleton = {"detected_pattern": ev["pattern"], "matched_text": ev["matched_text"]}
        intent = f"환류 후보 감지 — {ev['type']} pattern: {ev['pattern'][:50]}"
        write_feedback(ev["type"], body_skeleton, intent)
        written += 1
    print(f"feedback-classifier: {written} feedback written to {OUTBOX_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
