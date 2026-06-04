# Claude vs Codex CLI 합성 비교 (첫 dual-CLI dogfood, 2026-06-05)

본 자료는 starter LLM Wiki sandbox 의 같은 raw 자료 3 개 (본 session 의사결정 + Karpathy 원본 gist + Codex 두 라운드 검토 요약) 를 Claude Code 와 Codex CLI 가 각각 합성한 결과 비교. Karpathy 원본의 vendor-neutral 의도 작동 검증.

## 비교 dimensions

| 차원 | Claude | Codex |
|---|---|---|
| 페이지 개수 | 4 | 5 |
| 카테고리 분포 | concept 1 · entity 1 · topic 1 · timeline 1 | concept 2 · entity 1 · topic 1 · timeline 1 |
| 평균 신뢰도 | 0.91 | 0.892 |
| cross-link 페어 | 4 | 9 |
| 합성 시간 | 즉시 (OO session 내) | 249 초 (codex_runner sync) |

## entity 선택 차이

- **Claude**: `Andrej Karpathy` — LLM Wiki 패턴 원본 저자, origin narrative 시각
- **Codex**: `Codex CLI Reviewer` — 검토자 entity, review/governance 시각

같은 raw 에서 다른 entity 추출. 두 시각 모두 유효.

## concept 분리 양상

- **Claude**: `LLM Wiki Pattern` 단일 개념
- **Codex**: 2 분리 — `Compile-time Knowledge Accumulation` + `Provenance-First Synthesis`

Codex 가 같은 패턴을 2 개념으로 분해 — Karpathy 의 RAG 한계 진단 (누적 효과) 과 hallucinated synthesis 차단 (provenance) 을 별 차원으로 분리. 더 fine-grained 분류.

## topic 차이

- **Claude**: `Sandbox vs Ecosystem-wide LLM Wiki` (결정 흐름 narrative)
- **Codex**: `Starter Sandbox Boundary` (정책 boundary 명세)

Claude 는 decision story, Codex 는 policy contract.

## timeline 차이

- **Claude**: `2026-06 Sandbox Bootstrap` (사건 시간순)
- **Codex**: `2026-06 Dual-CLI Sandbox Measurement` (측정 가능 차원 timeline)

Codex 가 측정 가능 차원 (cross-link density · 신뢰도 분포 · false positive · hallucinated claim 비율) 을 timeline 단위로 정리.

## cross-link 양상

Claude 의 4 페어 모두 자기 합성 페이지 끼리. Codex 의 9 페어 중 일부가 Claude 합성 페이지 reference — 즉 Codex 가 Claude 합성을 인식하고 cross-link 가능. 양방향 보강 가능 양상.

## 합치 가능 여부

두 합성이 **상호 배타가 아닌 보완 관계**. 같은 sandbox 안 synthesized 에 두 합성 페이지 모두 살아 있을 수 있음 (다른 카테고리 또는 다른 sub-페이지로 분리). 단 이중 CLI schema hash 검사를 통과해야 — 본 첫 dogfood 는 schema 정합 통과 (양쪽 모두 sources 필수 + agent 명시 + schema_version 1.0).

## dual-CLI vendor-neutral 의도 검증

Karpathy 원본 명시: "OpenAI Codex, Claude Code, OpenCode / Pi, or etc." 양쪽에서 동작.

본 비교가 첫 evidence — 같은 정책 SSOT (`policy.yaml`) + 같은 schema (`schemas/llm-wiki-page-v1.json`) + 같은 raw 자료에서 두 CLI 가 다른 시각으로 의미 있는 합성 생성. 두 합성 모두 schema 정합 + sources 필수 충족.

## 결과 위치

- **Claude 합성**: `llm-wiki/synthesized/` (starter repo 안, commit `9092357` 에서 push 완료)
- **Codex 합성**: `OpenOrchestrator/tmp/codex-comparison/synthesized/` (OO 본체 tmp, gitignored)

starter repo 의 sandbox 는 Claude 합성만 영속화. Codex 합성은 비교 evidence 만 본 meta 파일에 보존.

## 향후 측정 영역 (Codex 13 risk 부분 검증)

본 dogfood 가 측정한 영역:
- ✅ 이중 CLI schema hash 검사 (양쪽 schema 정합 통과)
- ✅ 두 CLI 의 합성 의도 차이 (entity · concept 분리 양상)

본 dogfood 가 측정 못 한 영역:
- 추가 raw dump 시 cross-update 작동
- redaction (PII) 정밀도 — raw 에 PII 포함된 자료 ingest
- hallucinated claim 비율 — sources 의 raw 와 page claim 매칭 검증
- 동시 wiki 편집 시 lost update (single-writer applier policy 실측)

이 영역들은 후속 dogfood 누적 후 측정.
