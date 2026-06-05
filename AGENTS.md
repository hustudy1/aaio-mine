# AGENTS.md — Codex CLI Entrypoint

starter 의 Codex CLI 진입 문서. 사용자가 자연어 발화로 작업 trigger.

## Identity

aaio-mine — OpenOrchestrator 의 wrap product (외부 배포용 키트, agentic AIOps mine). 세 트랙 공존:
- A2A 트랙: `shared_data/` (후배 협업 task JSON 통신)
- LLM Wiki Sandbox 트랙: `llm-wiki/` (Karpathy 패턴 검증)
- 노션 협업 view 트랙 (옵션): `config/notion.yaml.example` + [docs/explanation/notion-collab-layer.md](docs/explanation/notion-collab-layer.md) (사람 가독성 협업 view, source-of-truth 아님)

세 트랙은 폴더 단위로 완전 분리. 한 트랙 작업이 다른 트랙 영향 0.

## Trigger Keywords (자연어, slash command 없음)

### A2A 트랙

- `task 보내` / `후배에게 dispatch` / `inbox 확인` / `A2A 메시지`

### LLM Wiki Sandbox

- `wiki 합성` / `wiki 정리` / `llm-wiki update` / `raw 자료 wiki 화` / `Karpathy wiki`

### 노션 협업 view (옵션)

- `노션` / `Notion` / `회의록` / `Kanban` / `워크스페이스`

키워드 발견 시 해당 트랙 작업 흐름 진입. 모호한 경우 사용자에게 어느 트랙인지 확인.

## LLM Wiki Sandbox 작업 흐름 (Codex CLI)

1. `llm-wiki/policy.yaml` Read + `schemas/llm-wiki-policy-v1.json` 검증
2. `llm-wiki/meta/.lock` 확인 — 존재 시 즉시 종료 + 사용자 알림
3. `.lock` 생성
4. `llm-wiki/meta/hot.md` Read — 이전 세션 흐름 복구
5. 사용자 의도 확인 — raw 의 어느 자료를 합성?
6. `llm-wiki/raw/` 의 대상 자료 Read
7. policy 의 PII (개인 식별 정보) 패턴 detect — 발견 시 `llm-wiki/meta/quarantine/` 격리 + 사용자 알림
8. 자료 의미 단위 식별 — concept · entity · topic · timeline 분류
9. `llm-wiki/synthesized/<type>/` 페이지 신설/갱신 — frontmatter 의 `sources` 필수
10. cross_links 갱신 — 같은 entity 가 다른 페이지 언급 시 양쪽 cross_links
11. `llm-wiki/meta/changelog.md` entry 추가
12. `llm-wiki/meta/hot.md` 갱신
13. `.lock` 삭제
14. 사용자에게 결과 보고

## Schema Version Check

policy.yaml 의 `schema_version` + `schema_hash` 가 Claude Code 의 진입 (`.claude/skills/llm-wiki-sandbox/SKILL.md`) 와 일치하지 않으면 fail_closed (작업 안 함). 사용자에게 sync 요청.

## 금지

- `llm-wiki/raw/` write 금지 (immutable)
- `llm-wiki/` 외부 폴더 write 금지 (policy.yaml 의 forbidden 영역)
- 사용자 personal 자산 노출 금지

## A2A 트랙

A2A 트랙 진입 시 `shared_data/inbox/<self>/tasks/*.json` 처리 흐름. 본 트랙의 schema · 동작은 별도 문서 (`docs/explanation/a2a-protocol.md`, 미작성 — A2A 부트스트랩 task 처리 시 신설 예정).

## 노션 협업 view 트랙 (옵션)

노션 워크스페이스를 협업 view 로 채택한 경우 한정. Codex CLI 는 노션 API 직접 호출 안 함 — 사람이 노션 페이지에서 결정 · 액션 아이템을 작성한 뒤, 그 결과를 `tasks/T-NNN-*.md` 또는 A2A `shared_data/outbox/<peer>/tasks/*.json` 으로 옮기는 흐름.

**거버넌스 (강제)**:

- 노션 = view, source-of-truth 아님. A2A task JSON · `tasks/T-NNN-*.md` · git lineage 가 진실
- 노션 워크스페이스 URL 은 `config/notion.yaml` (gitignored) 에만, repo 본문 · commit message · PR 본문 publish 금지
- 4 hard constraint Must Not (위반 시 즉시 노션 페이지에서 제거):
  1. 회사 코드 · 회사 시스템 정보 · 고객 정보 · 사내 운영 데이터
  2. 본인 personal 자산 lineage (자동매매 전략 코어 · personal 인프라 credentials 등)
  3. Personal Agent ops SSOT 본문 (master-wbs / session-state / 메모리 · `private_root` `internal-sensitive` 영역)
  4. Tier 1 backend 정보 (DB URL · 클러스터 config · queue endpoint · gateway 내부 구조)
- 노션 카드 ↔ task JSON 양방향 자동 sync 도입 금지

상세: [docs/explanation/notion-collab-layer.md](docs/explanation/notion-collab-layer.md)
