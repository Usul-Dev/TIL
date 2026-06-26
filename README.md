# TIL

백엔드 엔지니어로서 경쟁력을 키우기 위한 학습 기록 저장소입니다.

## 디렉터리

- `독후감`: 책을 읽고 남기는 회고와 정리
- `코딩테스트`: 알고리즘 문제 풀이와 코딩 테스트 루틴
- `레디스`: Redis 개념, 구현, 성능, 운영 관점 학습
- `RAG`: RAG 개념, 구현, 검색 파이프라인, 성능/운영 관점 학습

## 학습 티켓 운영

GitHub Issues와 Projects를 사용해 학습을 티켓 단위로 관리합니다.

- `Project`: 전체 학습 보드입니다. 예: `Backend Study Roadmap`
- `Milestone`: 큰 기술 영역입니다. 예: `Redis`
- `Parent Issue`: 깊게 팔 세부 주제입니다. 예: `Redis Lock`
- `Sub-issue`: 실제 실행 단위입니다. 예: `SET NX PX 기반 락 구현`
- `Pull Request`: 학습 결과를 저장소에 반영하는 단위입니다.

자세한 운영 방식은 [GitHub Study Workflow](docs/github-study-workflow.md)를 따릅니다.

## 개발 환경 원칙

이 저장소의 루트는 전체 학습 주제를 묶는 인덱스 역할만 합니다.

Python 실행 환경, 의존성, `uv.lock`은 필요한 학습 주제 디렉터리 안에서
각각 독립적으로 관리합니다. 예를 들어 `코딩테스트/`는 자체
`pyproject.toml`과 `uv.lock`을 가지고, 이후 `아키텍처/`나
`시스템디자인/`에서 별도 실습 환경이 필요해지면 해당 디렉터리 안에
독립적인 uv 프로젝트를 둡니다.
