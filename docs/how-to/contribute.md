# 협업 가이드

후배 onboarding 흐름 — fork 만들고 peers.yaml 작성한 뒤 첫 task 보내기.

## 1. fork 만들기

GitHub 에서 starter repo 를 본인 계정으로 fork. clone 후 본인 PC 에 둡니다.

```
git clone github.com/<your-handle>/aaio-mine-fork
```

## 2. peers.yaml 작성

`config/peers.yaml.example` 를 `config/peers.yaml` 로 복사하고 본인 peer 정보 입력합니다. peer-A · peer-B 자리에 협업 후배의 GitHub handle 적습니다. peers.yaml 자체는 gitignore — 외부에 노출 안 됩니다.

## 3. GitHub PAT 발급

fine-grained personal access token 발급. 권한:
- 본인 fork repo: contents read/write + pull-requests write
- 협업 후배 fork repo: contents read/write + pull-requests write

발급한 token 을 본인 fork repo 의 Secrets and variables 에 `A2A_CROSS_REPO_TOKEN` 으로 저장합니다.

## 4. 첫 task 보내기

Agent (Claude Code 또는 Codex CLI) 에게 "후배 A 에게 task 보내" 라고 말합니다. Agent 가 task JSON 을 `shared_data/outbox/peer-A/tasks/<id>.json` 에 작성하고 commit + push 합니다. GitHub Actions 가 후배 A 의 fork 에 PR 자동 생성합니다.

## 5. 받은 task 확인

본인 fork 의 `shared_data/inbox/<sender>/tasks/` 에 다른 후배로부터 PR 이 들어옵니다. 머지하면 Agent 가 inbox 의 새 JSON 을 읽고 자연어로 본인에게 요약합니다. 응답하거나 후속 task 로 답합니다.

## 함께 살아 있는 트랙 — LLM Wiki Sandbox

starter 안에 또 다른 트랙 (`llm-wiki/`) 이 있습니다. A2A 통신과 분리된 영역으로, Karpathy 의 LLM Wiki 패턴을 격리 환경에서 실험합니다. 본 협업 흐름과 무관하게 작동합니다. 자세한 내용은 [LLM Wiki 사용자 가이드](../explanation/llm-wiki-sandbox.md) 참고.

## 환류 (사용자 OO 본체로 보내는 3 종)

후배 fork 가 사용자 (upstream) 에게 보내는 환류는 3 종:

- **protocol_proposal** — schema · protocol 개선 제안 (예: task JSON 에 새 필드 필요)
- **incident** — 사고 보고 (예: hook 이 정상 task 를 reject)
- **decision_request** — 사용자 결정 필요한 질문 (예: 외부 라이브러리 추가 승인)

세션 종료 시 Agent 가 자동 분류 후 `shared_data/outbox/openorchestrator-upstream/feedback/<id>.json` 작성합니다. 일상 debrief 는 환류 안 감 — 본인 fork 안 `state/debrief/` 에만 머무릅니다.
