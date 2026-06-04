# LLM Wiki Sandbox — 사용자 가이드 (깊이)

## 왜 sandbox 인가

starter 의 `llm-wiki/` 폴더는 Karpathy 가 제안한 LLM Wiki 패턴을 작은 격리 환경에서 검증하는 영역입니다. 사용자의 personal 자산 · 회사 자료 · 다른 27 개 프로젝트 데이터 어디에도 영향 없습니다.

## ecosystem 전체 적용과의 차이

검토된 다른 선택지는 OpenOrchestrator 본체 거버넌스에 LLM Wiki 를 결합해서 모든 프로젝트의 데이터를 통합 관리하는 것이었습니다. 두 라운드의 검토 결과 13 종 critical risk (동시 쓰기 충돌 · 사용자 자료 누설 · 토큰 비용 폭발 · ecosystem-wide scan 의 control plane self-reference 등) 가 즉시 적용에 부적합으로 판단됐고, sandbox 만 진행으로 결정됐습니다.

본 sandbox 검증 결과가 좋으면 ecosystem 적용을 재평가합니다. 그 결정은 사용자가 직접 합니다.

## 데이터 흐름

1. 사용자가 `raw/` 에 자료를 둡니다. 이 폴더는 immutable — Agent 가 안 건드립니다.
2. Agent (Claude Code 또는 Codex CLI) 에게 "wiki 합성" 이라고 말하면 raw 의 자료를 읽고 분류합니다.
3. 합성 결과가 `synthesized/` 의 4 폴더 중 하나에 페이지로 누적됩니다.
   - **concepts**: 추상 개념 (예: "단일 작가 보장", "역할 분리")
   - **entities**: 사람 · 조직 · 도구 (예: 후배 A, OpenOrchestrator, ai-pkm)
   - **topics**: 주제별 (예: "data 산재 해소 전략")
   - **timelines**: 시간순 (예: "2026-06 의 design 결정 흐름")
4. 같은 entity 가 여러 자료에 나오면 entity 페이지 1 장으로 합쳐지고 다른 페이지에서 cross_link 됩니다.

## 안전 boundary 3 단

1. **시크릿 차단**: 정책 SSOT 의 `forbidden` 영역 — `.env` · 키 파일 등 영구 제외
2. **PII (개인 식별 정보) detect**: raw 의 이메일 · 전화번호 · 주민번호 형식 자동 식별 후 격리
3. **이중 CLI schema lock**: Claude Code 와 Codex CLI 가 같은 정책 SSOT (`policy.yaml`) 참조, 버전 불일치 시 작업 안 함

## 다른 트랙과의 분리

starter 안에는 다른 트랙 (`shared_data/` — 후배 협업 A2A 통신) 도 있습니다. 두 트랙은 폴더 단위로 완전히 분리됩니다. LLM Wiki 작업이 A2A 통신 메시지를 건드리지 않고, A2A 통신이 LLM Wiki 의 합성 페이지를 건드리지 않습니다.

## 향후 확장 판단 자료

sandbox 에서 다음을 검증하면 ecosystem 적용 결정에 evidence 가 됩니다.

- 다양한 자료 종류 (외부 자료 · 회의록 · PDF · markdown) 의 raw → synthesized 변환 품질
- Claude Code 와 Codex CLI 양쪽의 동작 일관성
- redaction 정책의 false positive · false negative 비율
- LLM 합성 페이지의 hallucinated claim 비율 (`changelog.md` 의 `sources` 검증으로 측정)
- 세션 간 hot cache 의 효용 (다음 세션 cold start 시간 측정)
- 동시 쓰기 충돌 빈도 (single_session_one_at_a_time 정책의 실효성)

## 누가 본 sandbox 를 쓰나

- 사용자 본인: starter repo 안에서 작업할 때
- 후배 (외부 배포 시): starter fork 받아 본인 fork 의 llm-wiki/ sandbox 활용
- 사용자의 다른 Agent (Claude Code · Codex CLI · Cursor · Kiro 등): policy.yaml 의 dual-CLI 정책에 따라 모두 같은 동작

## 본 sandbox 가 만들지 않는 것

- ai-pkm 의 RAG 인덱스 — 별 시스템 (분리)
- OpenOrchestrator 의 control plane 변경 — 본 sandbox 와 결합 0
- 27 managed projects 의 자료 — sandbox 가 scan 안 함
- starter 외부 배포 시 사용자 personal 자산 노출 — redaction layer 가 차단
