# Codex LLM Wiki Path C Review (Round 1 + Round 2)

본 자료는 Codex CLI 가 두 라운드에 걸쳐 사용자의 LLM Wiki 적용 plan (Path C 자체 구현) 을 검토한 결과 본문입니다. 두 결과 JSON 파일을 사람 친화 markdown 으로 정리.

## Round 1 (2026-06-04)

신뢰도 0.82, verdict approve-with-changes. 자동 통과 임계값 0.9 미달.

### 식별된 추가 Risk 7 종 (Claude 가 놓친 영역)

1. Writer authority inversion — LLM 이 wiki maintainer 인데 OO single-writer bootstrap/session-state 와 충돌
2. Provenance decay — synthesized wiki 페이지의 claim 출처 추적 손실
3. Dual-CLI concurrent writes — Claude · Codex 가 같은 wiki 페이지 편집 시 lost update
4. Starter/public distribution leakage — 사용자 personal governance / private knowledge 외부 노출
5. Golden-query eval 부재 — wiki 품질 · staleness 측정 fixture 없음
6. Methodology migration — LYT → PARA 등 rename 시 backlink 깨짐
7. Security redaction gap — raw source ingest 시 비밀 redaction 누락

### 핵심 권고

- 3 위치 (ai-pkm + starter + OO 본체) 동시 구현 X, 순차 rollout 권장
- LLM Wiki 가 새 root layer 가 아님 — ai-pkm 가 owner / EKI 가 indexer / OO 가 control plane writer 유지
- Methodology mode default 는 domain-folder (LYT/PARA/Zettelkasten 강제 X)
- starter 의 LLM Wiki 는 ai-pkm 검증 통과 후 활성

## Round 2 (2026-06-04, framing 정정 후)

신뢰도 0.86 (Round 1 보다 0.04 향상), verdict approve-with-changes.

### Round 1 잔여 5 종

- Claude · Codex 동시 wiki edits — single-writer applier policy lock 필요
- Codex 자연어 trigger drift — dual-CLI schema/hash enforcement 필요
- EKI 중복 · stale 인덱싱 — ai-pkm snapshot manifest + tombstone contract 필요
- non-opt-in repo boundary — registry-derived scan/write policy 필요
- MCP / skill broad filesystem access — deny-first resolved-path guards 필요

### Round 2 추가 8 종

1. ecosystem-wide scan 비용 + token budget 폭발
2. Control plane self-reference — 거버넌스가 LLM Wiki 의 input 이면서 동시에 control
3. Cross-repo visibility leakage — 합성 페이지를 통한 누설
4. Registry scope drift — 27 / 28 / 흡수된 / 외부 project count mismatch
5. Symlink / junction traversal 의도된 root 외부
6. Dirty worktree 의 uncommitted private notes publish
7. Binary / OCR 추출이 hidden PII 누설
8. Hallucinated synthesis 가 future retrieval prior (claim provenance 없이)

### 누락 카테고리 8 종 (12 → 20)

- Build / generated artifacts
- Dependency / vendor / cache
- Logs / traces / runtime telemetry
- Test fixtures / golden / eval datasets
- VCS metadata (.git)
- Binary / media (PDF · 이미지 · 음성 · 영상)
- 컴파일된 entrypoint + 거버넌스 산출물
- Runtime state / job queue / lock files

### 핵심 권고

- Stage 1 ADR 진입 전 5 사전작업: 누락 카테고리 추가 + #5/#6 broad write 권한 → explicit write-target registry 격하 + single-writer applier concurrency lock + ai-pkm snapshot/tombstone contract + dual-CLI policy schema 컴파일

### 동시성 default 권장

"Single-writer applier plus file-first proposal queue" — lock file 은 local mutex 만, PR branch 는 high-risk reviewed batches.

## 두 라운드 통합 — 13 critical risk

Round 1 잔여 5 + Round 2 추가 8 = 13 종.

## 사용자 결정 (Round 2 후)

ecosystem-wide LLM Wiki 보류 + starter 안 isolated sandbox 단일 트랙 채택.

Codex 의 권고 5 사전작업 중 sandbox scale 에서 의미 있는 영역만 적용 (정책 SSOT · write-target registry · dual-CLI policy schema). ai-pkm snapshot/tombstone contract · 27 repo registry 는 sandbox 무관.
