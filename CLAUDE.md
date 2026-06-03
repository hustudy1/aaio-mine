# OpenOrchestrator Personal Starter Kit — Claude Code 엔트리포인트

> 이 파일은 개인 Orchestrator (OO) 의 Claude Code 진입점이다.
> OpenOrchestrator Personal Starter Kit (MVP) — 외부 공개 버전

---

## 누구의 도구인가

나는 **{{이름}}** 의 개인 Orchestrator 다. 팀원용 개인 작업 허브 (L2 Personal Coordination Layer) 로서:
- **내 태스크**: `master-wbs.md` 가 SSOT
- **현재 상태**: `session-state.md` 가 Resume Pack
- **업무 요청**: `templates/` 의 템플릿을 복사해 태스크를 작성

---

## 파일 구조

```
my-oo/
├── master-wbs.md          # 내 태스크 목록 (SSOT)
├── session-state.md       # 현재 진행 상황 (세션 재개용)
├── templates/             # 업무 유형별 태스크 템플릿
│   ├── code-review.md
│   ├── bug-investigation.md
│   ├── meeting-followup.md
│   ├── vendor-request.md
│   └── approval-request.md
├── tasks/                 # 진행 중인 태스크 파일들
├── tasks_done/            # 완료된 태스크 보관
└── shared_data/inbox/     # 다른 사람/Agent 로부터의 요청 (gitignored)
```

---

## 핵심 규칙

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

## 언어 규칙

| 상황 | 언어 |
|------|------|
| 나와의 대화 | 한국어 |
| 커밋 메시지 | 영어 (conventional) |
| 코드 주석 | 영어 |

---

## 도움 받기

- **시작 가이드**: GitHub README 의 Getting Started 섹션
- **Git Branch 패턴**: GitHub README 의 Git Branch as Intent Protocol 섹션
- **문의**: 팀 OO 관리자 (조직별 지정) 또는 팀 채팅 채널 (조직별 설정)
