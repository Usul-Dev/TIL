# CLAUDE.md (레디스)

이 디렉터리의 규칙은 @AGENTS.md 를 따른다. 루트 `../AGENTS.md` 규칙을 먼저
적용한 뒤 이 디렉터리 규칙을 추가로 반영한다. 규칙은 `AGENTS.md`에서 관리한다.

## Claude Code 실행 메모

- 모든 명령은 `레디스` 디렉터리에서 실행한다. 루트 `.venv`가 아니라
  `레디스/.venv`를 사용한다.
- 의존성 설치: `uv sync --all-groups`
- 테스트: `uv run pytest -q` (별도 `docker compose up` 불필요, 단 Docker는
  실행 중이어야 한다. 꺼져 있으면 사용자에게 알린다.)
- 서버: `uv run fastapi dev app/main.py` 또는
  `uv run uvicorn app.main:app --reload` (`app/main.py` 직접 실행 금지,
  `레디스/app` 안에서 실행 금지 — `from app...` import가 깨진다)
- 린트/포맷: `uv run ruff check .`, `uv run ruff format .`
- Redis 연결은 `REDIS_URL`을 우선, 기본값 `redis://localhost:6379/0`.
