# A2A Protocol — Agent-to-Agent 통신 (starter)

## Overview

starter 가 외부 배포될 때, 후배 · 외부 사용자가 본인 fork 를 만들고 그 fork 들끼리 task JSON 으로 자동 통신하는 구조. 사용자 (OO 본체 운영자) 는 starter peer 가 아니라 upstream — 환류만 받습니다.

## 4 구성요소

### 1. Schema SSOT

`schemas/` 폴더의 3 종 JSON Schema:
- `task-v1.json`: peer 간 task 전달용
- `debrief-v1.json`: 세션 종료 시 본인 fork 안 보존
- `feedback-v1.json`: upstream (사용자 OO 본체) 으로 보내는 환류 3 종 enum

### 2. Peer Discovery

`config/peers.yaml` 가 본인 fork 의 peer 목록 + role + direction 보유. self / peer / upstream 3 role. peers.yaml 자체는 gitignore 권장 (peer credential 노출 방지).

### 3. Dispatch Transport

GitHub PR 기반 cross-repo:
- Agent 가 `shared_data/outbox/<peer>/tasks/<id>.json` 에 commit + push
- GitHub Actions (`.github/workflows/a2a-cross-repo-pr.yml`) 가 detect
- peers.yaml 에서 target peer 의 repo + inbox_path 조회
- fine-grained PAT (`A2A_CROSS_REPO_TOKEN`) 으로 target repo 에 PR cross-create
- PR body 에 intent 필드 노출 (사람말 1~2줄)
- 머지는 target repo 가 결정

### 4. Hygiene

- **Idempotency**: task_id 중복 시 receiver 가 skip
- **Loop guard**: dispatch_chain 배열 — 자기 자신 등장 시 reject
- **Authentication**: GitHub PR author = peer 신원. peers.yaml 미등록 시 reject
- **Schema validation**: 받는 쪽 GitHub Actions 가 머지 전 schema 검증

## Control / Data plane 분리

| Plane | 위치 | 역할 |
|---|---|---|
| Control | 사용자 OO 본체 | schema 정의 + 환류 수신 + 옵션 dispatch |
| Data | 후배 fork 2 개 | peer A2A 통신 + 본인 자원 사용 |

사용자 = upstream 만 (환류 수신 only). 일상 통신은 후배 fork 끼리.

## 환류 3 종 enum (`feedback-v1.json`)

| type | 내용 | 사용자 OO 본체 도착 후 |
|---|---|---|
| protocol_proposal | schema · protocol 개선 제안 | starter 다음 버전 input |
| incident | hook 차단 · validation 실패 · dispatch loop | starter 본체 fix → hotfix 배포 |
| decision_request | 사용자 결정 필요한 질문 | 사용자 응답 → 대칭 cross-PR 회신 |

일상 debrief / 통계 / knowledge 는 환류 안 감 (후배 fork 안 state/debrief/ 에만).

## 함께 살아 있는 트랙

starter 안에 또 다른 트랙 `llm-wiki/` (Karpathy LLM Wiki Sandbox) 가 있습니다. 폴더 단위 완전 분리 — A2A 통신과 LLM Wiki sandbox 가 서로 영향 0. 상세는 [LLM Wiki Sandbox 사용자 가이드](llm-wiki-sandbox.md) 참고.
