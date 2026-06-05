# 노션 협업 view layer (옵션 트랙) — Agent flow 거버넌스

## 위치

본 trip 는 aaio-mine starter 안 **옵션 layer**. 사용 안 해도 핵심 트랙 (5 templates / A2A / LLM Wiki) 영향 0. 활성 시 starter 의 기존 패턴(file-first + git intent broadcast) 을 **대체하지 않고 view 만 추가**한다.

본 layer 는 사람 가독성 협업(회의록 / 일정 / 작업 분담 view / 자료 인용) 한정. 실 작업 / 코드 / source-of-truth 는 그대로 git + file-first.

## 1. Layer 분리 (다른 트랙과의 관계)

| Layer | 도구 | 역할 | Source-of-Truth? |
|---|---|---|---|
| Personal Agent ops | 본인 자기 환경 (OO 본체 또는 별 personal stack) | 사용자 본인 자산 path | YES (본인 git) |
| Starter pattern | aaio-mine (본 repo) | Agent framework + 5 templates + 옵션 트랙 | YES (git) |
| Peer 협업 (file-first) | A2A 트랙 (`shared_data/inbox/` + GitHub PR cross-repo) | task / debrief / feedback JSON | YES (git lineage) |
| **Peer 협업 (human-readable, 본 trip)** | **노션 워크스페이스** | 회의록 / 일정 / 작업 분담 view / 자료 인용 | **NO (view only)** |

핵심: **노션 = view, A2A = transport**. A2A 가 옮기는 task / debrief / feedback JSON 은 git 안에 남고, 노션은 그것을 사람 읽기 좋게 카드 / 페이지로 비추는 보조 view.

## 2. 워크스페이스 등록 절차

1. 노션 워크스페이스 owner (멤버 중 한 명, 사용자 본인 또는 다른 멤버) 가 워크스페이스 생성
2. 멤버 (협업자) 에게 access 권한 부여
3. 본인 fork 안 `config/notion.yaml.example` 을 `config/notion.yaml` 로 복사 (gitignored)
4. `config/notion.yaml` 에 워크스페이스 URL · owner · members 채움
5. 본 워크스페이스에 §3 의 6 요소 페이지 생성 (회의록 템플릿 · 자료 인용 · Kanban · 캘린더 · 학습 진척 · 공통 지식 정리)
6. §4 의 4 hard constraint 멤버 전원 공유 + 합의

워크스페이스 URL 은 절대 repo 본문/PR/이슈/commit message 에 publish 하지 않는다. 외부 인터넷 검색 노출 방지 + owner 결정 영역 보존.

## 3. 노션에 두는 6 요소

1. **회의록 페이지 템플릿** — 주기 모임 (예: 주 1회) 용. 형식: 일시 / 참석 / 어젠다 / 결정 / 액션 아이템. 결정 · 액션 아이템은 작업 시점에 `tasks/T-NNN-*.md` 또는 A2A `shared_data/outbox/<peer>/tasks/*.json` 으로 옮긴다 (옮길 때 노션 회의록 페이지 URL 을 task 본문에 reference).
2. **자료 인용 페이지** — 외부 참고 자료 (논문 / 블로그 글 / 영상 등) link 모음. 본인 fork 안 자료는 git 안 source link 그대로, 노션은 인용·요약만.
3. **작업 분담 Kanban** — Todo / In progress / Done 보드. 각 카드 description 에 매칭되는 `T-NNN` task id 명시 (cross-reference). Kanban 은 진행 가시화, 실 작업은 git/file 에서.
4. **일정 캘린더** — 주기 모임 + 학습 자료 마감 + 정합 점검 시점.
5. **학습 진척 1pager** — 각 멤버가 자기 Agent (또는 작업 영역) 빌드 진척 1줄씩 자가 update.
6. **공통 지식 정리** — Agent framework 기본 개념 학습자 요약. 원본 git link 동반.

## 4. 4 Hard Constraint (Must Not)

| 절대 금지 | 이유 |
|---|---|
| 회사 코드 · 회사 시스템 정보 · 고객 정보 · 사내 운영 데이터 | 사내 데이터 반출 0 — 본인이 회사 후배·동료와 협업하는 경우 회사 surface 외부 노출 차단 |
| 본인 personal 자산 lineage (자동매매 전략 코어 · personal 인프라 credentials · 본인 home stack 구성 등) | 본인 자산 path 분리. 협업 멤버에게 공유하는 영역은 별 framing |
| 본인 Personal Agent ops SSOT 본문 (master-wbs / session-state / 메모리 · `private_root` `internal-sensitive` 영역) | Mode A 본체 보호. 노션은 inherit 금지 |
| Tier 1 backend 정보 (DB URL · 클러스터 config · queue endpoint · gateway 내부 구조 등) | 본인 personal stack 외부 노출 금지 |

본 4 constraint 위반은 멤버 전원 합의 항목. 위반 시 즉시 노션 페이지에서 제거 + 본인 측 OO 본체에 incident 1줄 carry.

## 5. A2A 트랙은 노션이 대체하지 않는다

A2A 트랙의 `task-v1.json` · `debrief-v1.json` · `feedback-v1.json` 은 file-first + git lineage 가 핵심 가치. 노션 카드로 옮기면 다음이 깨진다:

- **재현성**: 시점 lock 자료가 노션 cloud 안에 종속됨. owner 권한 변경 / 워크스페이스 삭제 시 lineage 손실
- **Cross-repo PR 자동화**: `.github/workflows/a2a-cross-repo-pr.yml` 가 file path 기반으로 작동. 노션은 file path 없음
- **schema 검증**: `schemas/task-v1.json` 등 schema validation 이 file 기반. 노션 카드 → JSON 변환은 별 자동화 필요
- **git intent broadcast**: `wip/T-NNN-*` 브랜치 패턴이 사라짐

따라서:
- A2A task JSON 자체는 git/file 그대로
- 노션 Kanban 의 카드는 *A2A task 의 view* (T-NNN id cross-reference)
- 노션 카드 update → 즉시 task JSON 갱신 (역방향 sync 안 함, 양방향 자동화 도입 금지)

## 6. Source-of-Truth flow (방향 1차원)

```
git/file (source-of-truth)
   │
   ├─ A2A task JSON
   ├─ aaio-mine tasks/T-NNN-*.md
   ├─ aaio-mine master-wbs.md
   └─ docs / schemas / config
            │
            ↓ (사람 가독성 view 만)
        노션 페이지 / 카드 / Kanban
```

역방향(노션 → git) sync 자동화는 도입 안 한다. 노션에서 발생한 결정 · 액션 아이템은 *사람이 직접* git/file 에 옮긴다. 그래야 4 hard constraint 위반 자동 유입 차단.

## 7. 사용 안 함 option

본 layer 는 옵션. 사용 안 해도 starter 핵심 트랙 (5 templates / A2A / LLM Wiki) 영향 0. 사용 안 함 결정 시:
- `config/notion.yaml.example` 참고만, 실 `config/notion.yaml` 작성 안 함
- CLAUDE.md / AGENTS.md 의 노션 섹션 무시
- 노션 거버넌스 적용 영역 0

## 8. Cross-reference

- [docs/explanation/a2a-protocol.md](a2a-protocol.md) — A2A 트랙 (transport)
- [docs/explanation/llm-wiki-sandbox.md](llm-wiki-sandbox.md) — LLM Wiki Sandbox 트랙 (knowledge view)
- [docs/how-to/contribute.md](../how-to/contribute.md) — 후배 onboarding 흐름
- [config/notion.yaml.example](../../config/notion.yaml.example) — 워크스페이스 등록 placeholder
- [CLAUDE.md](../../CLAUDE.md) · [AGENTS.md](../../AGENTS.md) — Agent flow 진입점 (노션 섹션 1단락)
