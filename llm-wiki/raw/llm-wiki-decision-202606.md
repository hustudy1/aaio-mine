# LLM Wiki 적용 결정 — 2026-06-04 ~ 2026-06-05

본 자료는 본 session 의 의사결정 흐름을 raw 형태로 보존합니다. LLM Wiki sandbox 의 첫 합성 input 으로 활용됩니다.

## 배경

사용자가 wikidocs.net 의 박재홍 블로그 글 (claude-obsidian 소개) 을 본 후 LLM Wiki 패턴을 본인 자산에 흡수하고 싶다는 의도를 표현. 다만 Claude Code 종속이 아니라 Codex CLI 도 동작해야 한다는 조건.

## Karpathy 원본 패턴 핵심

Andrej Karpathy 가 2026-04 에 5K+ star gist 로 공개한 패턴. raw 자료 → LLM 이 1회 컴파일 → 누적 markdown wiki. RAG (검색 후 답변 생성) 의 매 query reasoning 재시작 비효율 해결.

원본 명시: "This document is intentionally abstract. The right way to use this is to share it with your LLM agent and work together to instantiate a version that fits your needs."

vendor 호환: "OpenAI Codex, Claude Code, OpenCode / Pi, or etc." 양쪽 명시.

## 검토 흐름

Codex Round 1 (신뢰도 0.82) + Round 2 (신뢰도 0.86) — Path C (자체 구현) 잠정 approve-with-changes.

식별된 critical risk 13 종:

Round 1 잔여 5 종:
- Claude · Codex 동시 wiki 편집
- Codex 자연어 trigger drift
- EKI (knowledge 인덱싱) 중복 · stale 인덱싱
- non-opt-in repo boundary
- MCP · skill broad filesystem access

Round 2 추가 8 종:
- ecosystem-wide scan 비용 폭발
- control plane self-reference (거버넌스 가 input 이면서 동시에 control)
- cross-repo visibility leakage
- registry scope drift
- symlink · junction 탈출
- dirty worktree 의 uncommitted private notes publish
- binary · OCR hidden PII
- hallucinated synthesis 가 future retrieval prior

Round 2 누락 카테고리 8 종 추가 권고 (12 → 20 카테고리).

## 최종 결정

ecosystem-wide LLM Wiki 적용 보류. starter 안 isolated sandbox 단일 트랙 채택.

이유:
- 사용자 통제권 100% 보존 — 외부 fork 없음 (Path C 자체 구현)
- blast radius 통제 — starter 의 llm-wiki 폴더 단독, ai-pkm · OO 본체 · 27 managed projects 영향 0
- 사용자 진짜 pain (데이터 산재 해소) 직접 해결 안 됨 — sandbox 단계에서는 learning evidence 만 확보, ecosystem 확장은 sandbox 검증 후 재평가

## 4 Layer 책임 분리

- **Control**: OO 본체 거버넌스 (정책 SSOT · schema 정의)
- **Curation**: LLM Wiki (scan + dedupe + categorize + compile + maintain)
- **Storage**: ai-pkm (LLM Wiki output indexing · RAG 검색)
- **Distribution**: starter (외부 배포 wrap, A2A + LLM Wiki sandbox 두 트랙 공존)

## A2A 통신 결정

후배 2명 협업 구조 — file-first JSON over GitHub PR cross-create. 환류 3 type (protocol_proposal · incident · decision_request) 만 사용자 OO 본체로. 일상 debrief · 통계는 후배 fork 안 머무름.

대칭 응답 transport — 사용자 OO 본체 → 후배 fork cross-PR JSON. 후배 → 사용자 upstream feedback only.

## starter repo 구현 결과

3 commit / 33 파일 / 1155 줄 insertion / pytest 20/20 통과:
- LLM Wiki sandbox 24 파일 (sandbox 본체 14 + 검증 자산 10)
- A2A 통신 9 파일 (schemas 3 + peers · workflow · 가이드 2 · skill · hook)
- feedback-classifier 보강 (placeholder → JSONL parse + 17 패턴 + dedup + body schema 정합)

origin push 완료 — github.com/edolramba/openorchestrator-starter.

## 보류 작업

- GitHub Actions workflow cross-repo PR placeholder 보강 (사용자 "나중에 진행" 결정)
- Codex 13 risk 실측 (사용자 "OK" — raw dump + 합성 실행 후, 본 자료가 첫 measurement)
