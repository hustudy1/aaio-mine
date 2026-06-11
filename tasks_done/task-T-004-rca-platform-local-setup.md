# T-004 — RCA 플랫폼 로컬(k3d) 구축 · 재현성 · 벤치마크 채점

- 상태: ✅ 완료
- 소유자: 김민후
- 등록/완료: 2026-06-11
- 트랙: RCA (agenticaiops-rca-platform)
- 결과물 위치: **별도 repo + explaination 폴더** (이 파일은 기록·링크만)

---

## BLUF

새로 공유받은 `agenticaiops-rca-platform`을 **macOS + k3d 로컬에 전부 띄우고**, 장애 자동탐지→분석→복구→보고서 파이프라인을 **end-to-end로 검증**했다. 오늘 발견·해결한 모든 보정을 **repo 선언적 산출물로 승격**해 "clone하면 동작"하게 만들고, **벤치마크 채점·대시보드 정직성·기존 인프라 충돌 회피**까지 추가해 **PR #1**로 제출했다.

## 한 일 (요약)

- 로컬 k3d 전체 스택 기동 + 자동 파이프라인 1→7 검증 (결제 장애→자동 탐지→Claude 분석→보고서)
- LLM을 **호스트 Claude Code CLI 게이트웨이**로 전환 (AWS Bedrock 토큰 불필요, stub 탈출)
- 수정 검증 루프 실제 통과 (error rate 100%→0% 실측)
- 대시보드 정직성: 실패 단계를 빨강으로 (초록=실행됨 오해 제거)
- 런타임 패치 전부 kustomize 승격 → **네임스페이스 삭제 후 `apply -k`만으로 재현** 검증
- 벤치마크 채점(Service/Type Hit@1) + fault 분류기 → F4·connection_pool 100%/100%
- 기존 인프라 충돌 회피 + 통합 질문 프로토콜 (멀티 사용자 대비)
- 에이전트 부트스트랩(AGENTS.md → RUN-RCA-LOCAL.md) — Claude/Codex/Kilo 공용

## 결과물 링크

- **PR**: https://github.com/edolramba/agenticaiops-rca-platform/pull/1 (브랜치 `feat/local-reproducible-setup-and-benchmark`)
- **이론/검증 문서**: `/Users/data1/lab/explaination/rca-platform/`
  - `01~08-*.md` (개요·구조·내 작업·런북·정직성감사·단계별보고·쉬운설명·테스트데이터)
  - `test/2026-06-11-7단계-파이프라인-단계별-검증.md` (단계별 증거·해결과정)
- **repo 내 진입점**: `agenticaiops-rca-platform/RUN-RCA-LOCAL.md`, `AGENTS.md`, `scripts/setup-local.sh`

## 정직한 한계 (미완 — 별도 작업)

- RCAEval RE2 270건 전체 데이터셋/자동화 미구현 (채점 표본 2건)
- remediation = "시뮬레이션 리셋"형 (임의 코드 실제 patch = Phase C5 full 미완)
- Scene4 대시보드 실데이터(C6) 미완

## 다음 행동 (사람)

- PR #1 팀 리뷰 → main 병합 (팀 repo라 직접 push 회피, 브랜치만 올림)
