# LLM Wiki Sandbox

Karpathy 가 제안한 LLM Wiki 패턴을 starter 안에서 실험하는 영역입니다. 원본 자료를 `raw/` 에 두고 명시 호출하면 `synthesized/` 에 합성 페이지가 누적됩니다.

## 어떻게 쓰나

1. `raw/` 폴더에 자료 (markdown · PDF 변환본 · 회의록 등) 를 둡니다.
2. Agent (Claude Code 또는 Codex CLI) 에게 "wiki 합성" 또는 "raw 자료 wiki 화" 라고 말합니다.
3. Agent 가 자료를 읽고 `synthesized/` 의 4 폴더 중 적절한 위치에 합성 페이지를 만듭니다.
   - concepts: 추상 개념
   - entities: 사람 · 조직 · 도구
   - topics: 주제별
   - timelines: 시간순
4. `meta/hot.md` 는 세션 사이 작업 흐름 cache 입니다. 다음 세션 시작 시 Agent 가 먼저 읽습니다.
5. `meta/changelog.md` 는 Agent 의 모든 wiki 편집 이력입니다. 사람이 직접 검토 가능합니다.

## 무엇이 다른가

- 일반 노트와 다른 점: Agent 가 자동으로 cross-link 합니다. 같은 인물이 여러 문서에 나오면 entity 페이지 1 장으로 합쳐집니다.
- RAG (Retrieval-Augmented Generation, 검색 후 답변 생성) 와 다른 점: 자료가 누적될수록 합성 페이지가 진화합니다. 매번 fragment 검색이 아닌 사람이 읽는 페이지 단위입니다.

## 안전 boundary

- `raw/` 는 immutable 입니다. Agent 가 안 건드립니다.
- Agent 는 `synthesized/` 와 `meta/` 만 쓰기 가능합니다. starter 의 다른 폴더 영향 0.
- 개인 식별 정보 (이메일 · 전화번호 · 주민번호 형식) 가 raw 에 들어오면 Agent 가 격리 후 사용자에게 알립니다.

## 깊이 있는 설명

설계 의도 · ecosystem 와의 분리 · 향후 확장 판단 자료는 [docs/explanation/llm-wiki-sandbox.md](../docs/explanation/llm-wiki-sandbox.md) 참고.
