---
name: inbox-triage
description: starter 의 shared_data/inbox/<peer>/tasks/*.json 새 task 감지 시 발동, 사용자에게 자연어 요약 후 처리 분기.
trigger_keywords_korean:
  - "inbox 확인"
  - "받은 task"
  - "A2A 메시지"
  - "후배 요청 확인"
---

# Inbox Triage Skill (Claude Code)

## 활성화

사용자가 키워드 발화 시 또는 session 시작 시 자동:
- `inbox 확인` / `받은 task` / `A2A 메시지` / `후배 요청 확인`

## 작업 흐름

1. `shared_data/inbox/` 의 모든 peer 폴더 scan
2. 새 task JSON 파일 식별 (이전 세션 이후 추가, mtime 기준)
3. 각 JSON 의 schema 검증 (`schemas/task-v1.json`)
4. `config/peers.yaml` 의 known peer 인지 확인 — 모르는 peer 면 사용자에게 경고
5. dispatch_chain 검사 — 자기 자신 (`from == self.name`) 등장 시 reject (loop guard)
6. 각 task 의 `intent` 필드 (사람말 1~2줄) 를 사용자에게 자연어로 요약
7. 사용자 응답에 따라 분기:
   - **즉시 처리**: 처리 후 환류 task 작성 (필요 시)
   - **후속 dispatch**: 다른 peer 에게 cross-PR (`shared_data/outbox/<target>/`)
   - **사용자 결정 필요**: `decision_request` type 의 feedback JSON 작성 (upstream 으로)
   - **거부**: 처리 안 함, changelog 기록

## 종료 시

- 처리한 task 별 결과를 `state/debrief/<session_id>.json` 의 `peer_interactions` 배열에 추가
- Stop hook 이 본 session 의 incidents · proposals · decisions 를 자동 분류해서 feedback JSON 작성

## 금지

- task JSON 본문 임의 변경 금지
- 모르는 peer 의 task 자동 처리 금지
- 사용자 결정 없이 외부 통신 금지
- LLM Wiki sandbox 트랙 (`llm-wiki/`) 영향 금지
