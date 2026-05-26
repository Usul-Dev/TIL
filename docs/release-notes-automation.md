# Release Notes Automation

이 저장소의 릴리즈 노트는 GitHub Actions의 `Release Notes` workflow로 생성한다.

## Versioning

버전은 ISO 8601 주차 기준의 `vYYYY-Wxx` 형식을 사용한다.

- `YYYY`: ISO week-numbering year
- `Wxx`: ISO week number

ISO 주차는 월요일에 시작하고 일요일에 끝난다. 월이 바뀌는 주도 하나의 주로 유지한다.

연말/연초에는 ISO year가 달력상의 연도와 다를 수 있다. 예를 들어 `2027-01-01`은 ISO 기준 `2026-W53`이다.

예를 들어 `2026-05-26`은 `v2026-W22`가 된다.

## Pull Request Range

릴리즈 노트에는 `release_date`가 속한 ISO 주에 머지된 PR만 포함한다.

- 시작: 해당 ISO 주의 월요일 `00:00:00`
- 종료: 다음 ISO 주의 월요일 `00:00:00` 직전
- 기준 시간대: `Asia/Seoul`

예를 들어 `release_date`가 `2026-05-24`면 `2026-05-18T00:00:00+09:00`부터 `2026-05-25T00:00:00+09:00` 전까지 머지된 PR만 포함한다.

GitHub Release 태그는 릴리즈 노트에 포함된 마지막 PR merge commit을 가리킨다. 따라서 과거 주차를 나중에 수동 생성해도 현재 `HEAD`가 과거 릴리즈 태그에 잘못 묶이지 않는다.

## Release Note Format

릴리즈 노트는 변경된 최상위 디렉터리별로 PR을 나열한다. 예를 들어 `레디스/**`만 변경되면 `레디스`만 노출하고, 변경이 없는 대목은 표시하지 않는다.

```markdown
## 레디스

- #25 chore(redis): 개발 가이드라인 및 실행 진입점 정리
- #3 ci: upload Redis coverage to Codecov
```

기본적으로 `.github`, `.idea`, `scripts`, `docs`는 릴리즈 노트 주제에서 제외한다. 필요하면 workflow 또는 로컬 실행에서 `RELEASE_NOTE_IGNORED_TOPICS`로 바꿀 수 있다. 이 값을 바꾸면 `.github`처럼 점으로 시작하는 디렉터리도 포함할 수 있다.

## Manual Run

GitHub Actions에서 `Release Notes` workflow를 수동 실행할 수 있다.

- `release_date`: 비우면 `Asia/Seoul` 기준 오늘 날짜를 사용한다.
- `base_ref`: 비우면 직전 `vYYYY-Wxx` 태그부터 비교한다. 날짜 범위 필터는 항상 적용된다. 태그, 브랜치, SHA, `HEAD~N` 형태의 안전한 ref만 허용한다.
- `dry_run`: `true`면 GitHub Release를 만들지 않고 노트 파일만 artifact로 남긴다.

스케줄 실행은 매주 월요일 `00:05` KST에 동작한다. 이때는 막 끝난 ISO 주차를 릴리즈하기 위해 전날인 일요일 날짜로 버전을 계산한다.

## Local Preview

로컬에서 형식만 확인하려면 아래 명령을 실행한다.

```bash
python scripts/generate_release_notes.py \
  --date 2026-05-26 \
  --output /tmp/til-release-notes.md \
  --metadata /tmp/til-release-metadata.json
```
