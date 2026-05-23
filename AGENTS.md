# AGENTS.md

## 공통 규칙
- 작업 대상 디렉터리에 `AGENTS.md`가 있으면 루트 규칙을 먼저 적용한 뒤, 하위 규칙을 추가로 반영한다.
- 하위 `AGENTS.md`는 루트 규칙을 반복하지 않고, 해당 디렉터리에만 필요한 추가 규칙이나 예외만 기록한다.

## 커밋 메시지 규칙

- 커밋 메시지는 Conventional Commits 형식의 `<type>: <summary>`를 따른다.
- scope는 기본적으로 생략한다.
- 허용 type은 `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`를 우선 사용한다.
- summary는 72자 이내로 간결하게 작성한다.
- 한 커밋에는 하나의 목적만 포함한다.
- 기능 추가와 리팩토링은 분리한다.

## PR 제목 규칙

- PR 제목은 Conventional Commits 형식의 `<type>: <summary>`를 따른다.
- scope는 기본적으로 생략한다.
- 허용 type은 `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`를 우선 사용한다.

## PR 작성 규칙

- PR은 하나의 학습 주제 또는 하나의 기능 단위로 작게 유지한다.
- PR 설명에는 반드시 아래 내용을 포함한다.
    - 변경 요약
    - 변경 이유
    - 영향 범위
    - 검증 방법
- 단순히 코드가 동작한다는 설명보다, 설계 선택과 트레이드오프를 기록한다.
