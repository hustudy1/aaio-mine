# AGENTS.md — Codex CLI Entrypoint

starter 의 Codex CLI 진입 문서. 사용자가 자연어 발화로 작업 trigger.

## Identity

aaio-mine — OpenOrchestrator 의 wrap product (외부 배포용 키트, agentic AIOps mine). 두 트랙 공존:
- A2A 트랙: `shared_data/` (후배 협업 task JSON 통신)
- LLM Wiki Sandbox 트랙: `llm-wiki/` (Karpathy 패턴 검증)

두 트랙은 폴더 단위로 완전 분리. 한 트랙 작업이 다른 트랙 영향 0.

## Trigger Keywords (자연어, slash command 없음)

### A2A 트랙

- `task 보내` / `후배에게 dispatch` / `inbox 확인` / `A2A 메시지`

### LLM Wiki Sandbox

- `wiki 합성` / `wiki 정리` / `llm-wiki update` / `raw 자료 wiki 화` / `Karpathy wiki`

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
