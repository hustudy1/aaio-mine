---
title: Sandbox vs Ecosystem-wide LLM Wiki 결정 흐름
type: topic
sources:
  - path: ../../raw/llm-wiki-decision-202606.md
    ts: 2026-06-05T00:00:00+09:00
    claim: "ecosystem-wide 보류 + sandbox 채택 결정 lock"
cross_links:
  - ../concepts/llm-wiki-pattern.md
  - ../timelines/2026-06-sandbox-bootstrap.md
confidence: 0.92
last_synthesized_at: 2026-06-05T00:00:00+09:00
agent: claude-code
schema_version: "1.0"
---

# Sandbox vs Ecosystem-wide LLM Wiki

2026-06-04 ~ 2026-06-05 에 결정된 LLM Wiki 적용 범위. 두 선택지를 비교한 결과 sandbox 채택.

## 두 선택지 비교

### Ecosystem-wide (보류)

OO 본체 거버넌스 + ai-pkm + 27 managed projects 모두 통합. 사용자 진짜 pain (데이터 산재 해소) 직접 해결.

단 Codex 두 라운드 검토에서 식별된 critical risk 13 종:

Round 1 잔여 5:
- Claude · Codex 동시 wiki 편집 corruption
- Codex 자연어 trigger drift
- EKI 중복 · stale 인덱싱
- non-opt-in repo boundary
- MCP · skill broad filesystem access

Round 2 추가 8:
- ecosystem-wide scan 비용 폭발
- control plane self-reference
- cross-repo visibility leakage
- registry scope drift
- symlink · junction 탈출
- dirty worktree 의 uncommitted private notes publish
- binary · OCR hidden PII
- hallucinated synthesis 가 future retrieval prior

### Sandbox (채택)

starter 의 `llm-wiki/` 단독 폴더. blast radius starter 단독. 사용자 personal 자산 · ai-pkm · OO 본체 · 27 managed projects 영향 0.

학습 evidence 확보 → ecosystem 확장 결정의 근거.

## 향후 재평가 trigger

sandbox 에서 검증해야 할 영역:
- 다양한 raw 자료 형식 (markdown · PDF 변환 · 회의록) 의 합성 품질
- Claude Code · Codex CLI 양쪽 동작 일관성 (이중 CLI schema hash 검사)
- redaction (PII) 정밀도
- hallucinated claim 비율 (sources 필드 검증)

이 측정 결과가 좋으면 사용자가 ecosystem 확장 결정 가능. 결정은 사용자 단독 (외부 Agent 자동 진행 X) — [feedback_sole_control_ownership] 원칙.

## 관련

- [LLM Wiki Pattern](../concepts/llm-wiki-pattern.md) — 본 결정의 기반 개념
- [2026-06 Sandbox Bootstrap](../timelines/2026-06-sandbox-bootstrap.md) — 시간순 정리
