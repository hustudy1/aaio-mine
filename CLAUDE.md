# OpenOrchestrator Personal Starter Kit — Claude Code 엔트리포인트

> 이 파일은 개인 Orchestrator (OO) 의 Claude Code 진입점이다.
> OpenOrchestrator Personal Starter Kit (MVP) — 외부 공개 버전
> Claude Code CLI 가 기준 hub. Codex CLI 는 [AGENTS.md](AGENTS.md) 진입점 별도 (대칭 명시).

---

## 누구의 도구인가

나는 **{{이름}}** 의 개인 Orchestrator 다. 팀원용 개인 작업 허브 (L2 Personal Coordination Layer) 로서:

- **내 태스크**: `master-wbs.md` 가 SSOT
- **현재 상태**: `session-state.md` 가 Resume Pack
- **업무 요청**: `templates/` 의 템플릿을 복사해 태스크를 작성

---

## 트랙 인덱스 (Track Index)

본 starter 는 3 트랙으로 구성된다. **5 templates 트랙은 핵심** (clone 직후 즉시 사용), **A2A + LLM Wiki 는 옵션** (필요 시 활성).

| 트랙 | 폴더 | 진입점 | 핵심도 | 용도 |
|---|---|---|:-:|---|
| 5 templates + WBS + Session | `templates/` + `master-wbs.md` + `session-state.md` + `tasks/` + `tasks_done/` | 본 CLAUDE.md | 핵심 | 개인 태스크 관리, 세션 재개 |
| A2A (Agent-to-Agent 통신) | `shared_data/inbox/` + `.claude/skills/inbox-triage/` + `.claude/hooks/feedback-classifier.py` + `schemas/{task,debrief,feedback}-v1.json` + `config/peers.yaml.example` | [docs/explanation/a2a-protocol.md](docs/explanation/a2a-protocol.md) | 옵션 | 동료 / 후배와 file-first task JSON 교환 |
| LLM Wiki Sandbox | `llm-wiki/` + `.claude/skills/llm-wiki-sandbox/` + `schemas/llm-wiki-{page,policy}-v1.json` | [llm-wiki/README.md](llm-wiki/README.md) | 옵션 | Karpathy LLM Wiki 패턴 검증 sandbox |

세 트랙은 폴더 단위로 완전 분리. 한 트랙 작업이 다른 트랙 영향 0.

---

## 도구별 진입점

| 도구 | 진입 파일 | scope |
|---|---|---|
| Claude Code CLI | 본 `CLAUDE.md` | 3 트랙 hub + 자연어 발화 routing |
| Codex CLI | [AGENTS.md](AGENTS.md) | A2A 트랙 + LLM Wiki Sandbox 트랙 (14 stage workflow) |
| Cursor / Copilot / Kiro | 본 `CLAUDE.md` (alwaysApply 형태) | 5 templates 트랙 기준 |

`CLAUDE.md` ↔ `AGENTS.md` 두 진입점은 동일 starter repo 의 다른 face. 같은 트랙 구조를 다른 도구에서 안내.

---

## 파일 구조

```
my-oo/
├── CLAUDE.md               # Claude Code 진입점 (본 파일, 3 트랙 hub)
├── AGENTS.md               # Codex CLI 진입점 (A2A + LLM Wiki)
├── README.md               # 외부 사용자 첫 인상
├── LICENSE                 # Apache 2.0
├── .gitignore
│
├── master-wbs.md           # 내 태스크 목록 (5 templates 트랙 SSOT)
├── session-state.md        # 현재 진행 상황 (세션 재개용)
│
├── templates/              # 5 templates 트랙 — 핵심
│   ├── code-review.md
│   ├── bug-investigation.md
│   ├── meeting-followup.md
│   ├── vendor-request.md
│   └── approval-request.md
├── tasks/                  # 진행 중인 태스크 파일들 (.gitkeep 만 추적)
├── tasks_done/             # 완료된 태스크 보관 (.gitkeep 만 추적)
│
├── shared_data/inbox/      # A2A 트랙 — 다른 사람/Agent 로부터의 요청 (gitignored)
│
├── llm-wiki/               # LLM Wiki Sandbox 트랙
│   ├── README.md
│   ├── policy.yaml
│   ├── raw/                # 원본 자료 (immutable)
│   ├── synthesized/        # 합성 페이지 (concept/entity/topic/timeline)
│   ├── meta/               # changelog / hot / lock
│   └── tests/              # PII 검출 + page schema + policy schema
│
├── .claude/
│   ├── skills/
│   │   ├── inbox-triage/   # A2A 트랙 skill
│   │   └── llm-wiki-sandbox/  # LLM Wiki 트랙 skill
│   └── hooks/
│       └── feedback-classifier.py  # A2A 트랙 hook
│
├── schemas/                # JSON Schema 자산
│   ├── task-v1.json        # A2A
│   ├── debrief-v1.json     # A2A
│   ├── feedback-v1.json    # A2A
│   ├── llm-wiki-page-v1.json    # LLM Wiki
│   └── llm-wiki-policy-v1.json  # LLM Wiki
│
├── config/
│   └── peers.yaml.example  # A2A peer 설정 placeholder (실 peer 정보는 .gitignored)
│
└── docs/
    ├── explanation/        # A2A protocol / LLM Wiki sandbox 설명
    └── how-to/             # contribute 가이드
```

---

## 핵심 규칙 (5 templates 트랙 기준)

### 반드시 할 것 (Do)
- ✅ 모든 태스크는 `master-wbs.md` 에 먼저 기록 (WBS-first intake)
- ✅ 세션 시작 시 `session-state.md` 의 `active_task` 확인
- ✅ 세션 종료 시 `session-state.md` 업데이트 후 git commit
- ✅ 외부 대기 (벤더 / 승인) 발생 시 태스크를 Park 상태로 전환
- ✅ 작업 완료 태스크는 `tasks_done/` 으로 이동

### 하지 말 것 (Don't)
- ❌ `session-state.md` 없이 세션 재개
- ❌ 완료 확인 전 태스크 삭제
- ❌ 중요 결정사항을 대화창에만 남기고 문서화 생략

---

## 빠른 시작 (Quick Start)

### 세션 시작

```
1. session-state.md 확인 → active_task 파악
2. 해당 태스크 파일 열기
3. 작업 시작
```

### 새 태스크 등록

```
1. master-wbs.md 에 행 추가
2. templates/ 에서 해당 템플릿 복사 → tasks/task-T-NNN-slug.md
3. 내용 채우기 → git commit (intent broadcast)
```

### 세션 종료

```
1. session-state.md 업데이트 (done_today, next_action)
2. git add . && git commit -m "chore: 세션 요약"
3. git push (팀과 의도 공유)
```

### Park (외부 대기)

```
외부 응답 대기가 필요하면:
1. 태스크 파일에 "park 상태: 대기 이유" 기록
2. session-state.md 4번 섹션에 추가
3. git commit → 다음 태스크로 이동
```

---

## Git Branch = Intent

```
새 태스크 시작 → git checkout -b wip/T-{id}-{summary}
작업 완료      → git checkout main && git merge wip/T-{id}-{summary}
팀 현황 확인   → git fetch --all && git branch -r | grep wip/
```

wip/* 브랜치가 "지금 누가 무엇을 하고 있는지" 를 실시간으로 알려준다.

---

## 옵션 트랙 활성 방법

### A2A 트랙 활성 (동료 / 후배와 task 교환)

```
1. config/peers.yaml.example 을 config/peers.yaml 로 복사
2. peer 정보 (이름 / inbox path / GitHub username) 채움 — 본 파일은 gitignored
3. .claude/skills/inbox-triage/SKILL.md 의 trigger 키워드 사용 (예: "inbox 확인")
4. shared_data/inbox/ 에 들어오는 task JSON 자동 triage
5. 자세한 내용: docs/explanation/a2a-protocol.md
```

### LLM Wiki Sandbox 활성

```
1. llm-wiki/raw/ 에 원본 자료 추가 (immutable — write 후 변경 금지)
2. .claude/skills/llm-wiki-sandbox/SKILL.md 의 trigger 키워드 사용 (예: "wiki 합성")
3. llm-wiki/synthesized/ 아래 concept/entity/topic/timeline 페이지 자동 생성
4. llm-wiki/meta/changelog.md 에 entry 자동 추가
5. 자세한 내용: llm-wiki/README.md
```

---

## 언어 규칙

| 상황 | 언어 |
|------|------|
| 나와의 대화 | 한국어 |
| 커밋 메시지 | 영어 (conventional) |
| 코드 주석 | 영어 |

---

## 도움 받기

- **시작 가이드**: [README.md](README.md) 의 Getting Started 섹션
- **Git Branch 패턴**: [README.md](README.md) 의 Git Branch as Intent Protocol 섹션
- **A2A 트랙 상세**: [docs/explanation/a2a-protocol.md](docs/explanation/a2a-protocol.md)
- **LLM Wiki Sandbox 상세**: [llm-wiki/README.md](llm-wiki/README.md)
- **문의**: 본 starter 를 본인 팀에 도입한 경우 — `{{팀 OO 관리자 이름}}` 또는 `{{팀 채팅 채널}}` (Personalize 단계에서 README "Personalize" 안내와 함께 치환)

### Personalize 체크리스트

clone 직후 다음 placeholder 를 본인 정보로 치환:

- 본 파일 `CLAUDE.md` — `{{이름}}` (L10), `{{팀 OO 관리자 이름}}` + `{{팀 채팅 채널}}` (위 §도움 받기)
- `master-wbs.md` — `{{이름}}` + `{{YYYY-MM-DD}}`
- `session-state.md` — `{{이름}}` + `{{YYYY-MM-DD}}`
