---
last_session_id: 2026-06-05-sandbox-first-dogfood
last_updated: 2026-06-05T00:00:00+09:00
last_summary: "본 session 의 의사결정 자료 (raw 1) + 합성 페이지 (concepts · entities · topics · timelines 각 1) 4 + meta 갱신 2. Karpathy 패턴 첫 dogfood evidence 확보."
next_entry_hint: "다음 세션 시작 시 사용자가 추가 raw 자료 dump 가능 — 외부 자료 · 회의록 · PDF 등. Claude · Codex 양쪽에서 'wiki 합성' 발화 시 본 합성 페이지들을 cross-link 로 갱신 가능."
---

# Hot Cache

세션 종료 시 Agent 가 본 파일 업데이트. 다음 세션 시작 시 Agent 가 먼저 읽음.

## 최근 작업 흐름

2026-06-05 첫 dogfood — Karpathy LLM Wiki 패턴이 sandbox 안에서 동작하는지 검증.

- raw 자료 1 dump (본 session 의사결정 통합) — [llm-wiki-decision-202606.md](../raw/llm-wiki-decision-202606.md)
- 합성 페이지 4 (concept · entity · topic · timeline 각 1)
- cross-link 4 페어 자동 유지
- changelog 5 entry 기록

## 다음 작업 후보

- 추가 raw 자료 (외부 자료 · 회의록 · PDF) dump 후 합성 시도
- 같은 raw 를 Codex CLI 가 합성하면 결과 비교 (이중 CLI schema hash 검사)
- 1주 후 hot cache 효용 측정 (cold start 시간)
- 사용자 발화 "wiki 합성" trigger 로 자동 발동 검증 (skill 활성화 흐름)

## 누적 합성 페이지

- concepts/llm-wiki-pattern.md
- entities/karpathy.md
- topics/sandbox-vs-ecosystem-wide.md
- timelines/2026-06-sandbox-bootstrap.md
