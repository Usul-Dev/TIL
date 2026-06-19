# CLAUDE.md (코딩테스트)

공통 규칙(커밋/PR/리뷰)은 루트 @../AGENTS.md 를 단일 소스로 따른다.
이 디렉터리에는 자체 `AGENTS.md`가 없으므로 규칙은 루트에서 관리한다.

## Claude Code 실행 메모

- 이 디렉터리는 루트와 분리된 독립 uv 프로젝트다. 명령은 `코딩테스트`
  디렉터리에서 실행한다.
- 의존성 설치: `uv sync`
- 풀이 실행: `uv run python warm_up/<파일명>.py`
  (예: `uv run python warm_up/12_step_블랙잭.py`)
- 풀이 파일은 `warm_up/` 아래 백준 단계별로 정리한다.
- 린트/포맷: `uv run ruff check .`, `uv run ruff format .`
  (`pyproject.toml` 기준: py313, line-length 79, tab indent)
