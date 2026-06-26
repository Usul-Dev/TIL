# GitHub Study Workflow

이 저장소는 개인 학습을 실제 백엔드 업무처럼 티켓 단위로 관리합니다.

## 기본 구조

```txt
Project: Backend Study Roadmap
  Milestone: Redis
    Parent Issue: Redis Lock 학습
      Sub-issue: Redis 분산락 개념 정리
      Sub-issue: SET NX PX 기반 락 구현
      Sub-issue: Redlock 알고리즘 분석
      Sub-issue: 락 만료/재시도/장애 케이스 실험
      Sub-issue: 경력직 면접 질문 정리
```

## GitHub 기능 역할

- `Project`: 전체 학습 보드입니다. 하나만 두고 모든 학습 티켓을 모읍니다.
- `Milestone`: 큰 기술 영역입니다. 예: `Redis`, `Kafka`, `Database`, `System Design`.
- `Parent Issue`: 깊게 팔 세부 주제입니다. 예: `Redis Lock`, `Cache Aside`, `DB Index`.
- `Sub-issue`: 실제 실행 단위입니다. 개념, 구현, 성능 실험, 운영 정리, 면접 질문으로 쪼갭니다.
- `Label`: 티켓의 성격과 산출물을 분류합니다.
- `Pull Request`: 학습 결과를 저장소에 반영하는 단위입니다.

## 초기 GitHub 세팅

저장소 파일로 기본 제공되는 것은 Issue Forms와 라벨 기준 문서입니다.
GitHub의 실제 Project, Milestone, Label은 GitHub UI 또는 `gh` CLI로 한 번 생성해야 합니다.

1. Project를 하나 만듭니다.
   - 권장 이름: `Backend Study Roadmap`
2. 큰 기술 영역별 Milestone을 만듭니다.
   - 예: `Redis`, `RAG`, `Kafka`, `Database`, `System Design`
3. `.github/labels.yml` 기준으로 라벨을 만듭니다.
4. 이후 Issue 생성 시 `Backend Study Topic` 또는 `Backend Study Task` 템플릿을 사용합니다.

## Project 권장 설정

Project 이름은 `Backend Study Roadmap`을 권장합니다.

권장 views:

- `Board`: `Status` 기준 Kanban 보드
- `Table`: 전체 티켓 목록
- `Redis`: `area/redis` 또는 `Milestone: Redis` 필터
- `Interview`: `type/interview` 필터
- `Production`: `type/production` 필터

권장 fields:

| Field | Type | Values |
| --- | --- | --- |
| `Status` | Single select | `Backlog`, `Ready`, `In Progress`, `Review`, `Done` |
| `Area` | Single select | `Redis`, `RAG`, `Kafka`, `Database`, `System Design`, `Coding Test` |
| `Work Type` | Single select | `Concept`, `Implementation`, `Performance`, `Production`, `Interview`, `Documentation` |
| `Output` | Single select | `Docs`, `Code`, `Benchmark`, `Experiment` |
| `Priority` | Single select | `P0`, `P1`, `P2`, `P3` |
| `Effort` | Number | `1`, `2`, `3`, `5` |

## 티켓 작성 규칙

1. 큰 기술 영역을 정하고 Milestone을 만듭니다.
   - 예: `Redis`
2. 깊게 팔 주제를 `Backend Study Topic` 템플릿으로 Parent Issue로 만듭니다.
   - 예: `[Study] Redis Lock`
3. 실제 실행 단위를 `Backend Study Task` 템플릿으로 만듭니다.
   - 예: `[Task] SET NX PX 기반 락 구현`
4. Task Issue를 Parent Issue의 Sub-issue로 연결합니다.
5. 작업이 끝나면 PR로 문서, 코드, 실험 결과를 반영합니다.

## Redis 학습 티켓 예시

### Parent Issue

```txt
Title: [Study] Redis Lock
Milestone: Redis
Labels: type/topic, track/backend, area/redis, priority/p0
```

### Sub-issues

```txt
[Task] Redis 분산락이 필요한 상황 정리
[Task] SET NX PX 기반 락 구현
[Task] Lua 기반 unlock 원자성 보장
[Task] Redlock 알고리즘과 비판점 분석
[Task] 락 만료, 재시도, 장애 케이스 실험
[Task] Redis Lock 경력직 면접 질문 정리
```

## 완료 기준

Parent Issue는 아래 조건을 만족할 때 닫습니다.

- 관련 Sub-issues를 완료했습니다.
- 코드 또는 실험 결과를 남겼습니다.
- 성능, 운영, 장애 관점의 고민을 기록했습니다.
- 경력직 면접 질문과 답변을 정리했습니다.
- 주제 디렉터리의 README 또는 별도 문서에 최종 정리를 반영했습니다.
