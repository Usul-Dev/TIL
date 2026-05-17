1) 자료구조 선택 질문: “왜 Redis를 썼고, 어떤 타입을 왜 골랐나?”

Redis는 여러 네이티브 데이터 타입을 제공하고, 용도에 따라 성능/원자성/모델링이 달라진다.  ￼

구현 과제 A: “장바구니 + 재고 차감” 모델링
	•	질문 포인트
	•	Hash vs String(JSON) vs Set을 왜 선택?
	•	단일 키에 몰아넣는 것 vs 키를 쪼개는 것의 트레이드오프?
	•	구현
	•	cart:{userId}: Hash로 itemId→qty
	•	stock:{itemId}: String(정수)로 재고
	•	체크아웃 시 재고 차감 + 장바구니 비우기
	•	체크 포인트
	•	race condition 방지(원자성) 어떻게 보장?
	•	실패 시 롤백/재시도 전략?

구현 과제 B: “랭킹/리더보드”
	•	Sorted Set으로 점수 기반 랭킹(Top N, 내 순위)  ￼
	•	체크 포인트: 동점 처리, score 업데이트 빈도, range 조회 비용

⸻

2) 원자성/트랜잭션/동시성: “Redis에서 트랜잭션이 DB 트랜잭션이랑 뭐가 다른가?”

구현 과제: “쿠폰 1회성 발급” (선착순)
	•	질문 포인트
	•	WATCH/MULTI/EXEC 낙관적 락 흐름
	•	Lua 스크립트로 원자 연산을 묶는 이유
	•	구현
	•	재고 키 coupon:remain
	•	발급 집합 coupon:issued(Set)
	•	“남은 수량 감소 + 중복발급 방지 + 발급 기록”을 한 번에 처리
	•	체크 포인트
	•	재시도 루프(낙관적 실패 시)
	•	Lua vs MULTI의 선택 기준(성능/네트워크 RTT)

⸻

3) TTL/만료/캐싱 전략: “캐시 무효화 어떻게 했나?”

구현 과제: “Cache-aside + stampede 방지”
	•	질문 포인트
	•	cache-aside 패턴, stale 데이터 허용 여부
	•	cache stampede(동시 미스 폭발) 대응
	•	구현
	•	읽기: 캐시 미스면 DB 조회 후 set + TTL
	•	stampede 방지:
	•	(1) 분산락(간단한 락 키)으로 1명만 DB 조회
	•	(2) soft TTL(값에 만료시간 포함) + 백그라운드 갱신 흉내
	•	체크 포인트
	•	TTL jitter(랜덤)로 동시 만료 분산
	•	“캐시 삭제 vs 갱신” 어느 쪽을 쓰는지

⸻

4) 메모리/삭제 정책: “Redis가 메모리 꽉 차면 무슨 일이 벌어지나?”

Redis는 maxmemory와 eviction policy로 초과 시 키를 내보내는 방식을 선택한다.  ￼

구현 과제: “eviction 정책별 캐시 히트율 비교”
	•	질문 포인트
	•	allkeys-lru / allkeys-lfu / volatile-ttl 차이
	•	“중요키가 날아가면?” 어떻게 방지?
	•	구현
	•	동일 워크로드(핫키/콜드키 섞인 트래픽) 생성
	•	정책 바꿔가며 hit rate, latency 비교
	•	체크 포인트
	•	volatile-*는 TTL 없는 키는 안 날아감(설계에 영향)
	•	eviction 때문에 write 실패가 아니라 “예상치 못한 키 손실”이 생길 수 있음

⸻

5) 운영/성능 진단: “Redis 느려졌을 때 무엇부터 보나?”

Redis는 latency 진단 가이드를 제공하고, 원인(커널/가상화/네트워크/명령어/백그라운드 작업 등)을 체계적으로 보라고 한다.  ￼

구현 과제: “SLOWLOG/latency spikes 재현”
	•	질문 포인트
	•	느린 명령의 패턴(큰 키, O(N) 명령, KEYS 같은 금기)
	•	네트워크 vs 서버 내부 병목 구분
	•	구현
	•	큰 List/SortedSet 만들고 무거운 연산 수행
	•	slowlog로 느린 커맨드 추적, p99 지연 비교
	•	체크 포인트
	•	데이터 모델 바꾸면 해결되는가?
	•	pipelining/배치로 RTT 줄일 수 있는가?

(참고로 “latency” 모니터링 주제는 공식 운영 문서가 가장 신뢰도가 높다.)  ￼

⸻

6) 보안: “Redis를 인터넷에 그냥 열어두면?”

Redis는 보안 문서에서 접근 제어(ACL), 안전한 배포, 암호화(TLS) 등을 다룬다.  ￼

구현 과제: “ACL로 최소권한 사용자 만들기”
	•	질문 포인트
	•	AUTH만으로 충분한가?
	•	사용자별 허용 커맨드/키 패턴 제한 가능?
	•	구현
	•	read-only 사용자
	•	특정 prefix 키만 접근 가능한 사용자
	•	체크 포인트
	•	운영에서 권한 분리(앱/배치/관리자) 어떻게 할지

⸻

7) 실전 분산 시스템 질문: “세션/레이트리밋/큐를 Redis로 어떻게 구현?”

구현 과제 A: “API Rate Limiter 3종”
	•	Fixed window / Sliding window / Token bucket을 각각 구현
	•	체크 포인트: 정확도 vs 비용, burst 허용, 클러스터 환경에서의 일관성

구현 과제 B: “작업 큐”
	•	List 기반 간단 큐 (LPUSH/RPOP)
	•	Streams 기반 컨슈머 그룹 큐(재처리/ACK)도 확장 학습(이벤트 로그 성격)
(Streams는 Redis 데이터 타입 문서에서 공식적으로 다룸)  ￼

⸻

추천 “학습 우선순위” (면접 대비 효율 순)
	1.	TTL/캐싱 + stampede 방지
	2.	원자성(트랜잭션, Lua) + 동시성 이슈 재현
	3.	eviction 정책 + 메모리 모델링  ￼
	4.	운영 진단(SLOWLOG/latency)  ￼
	5.	자료구조 모델링(특히 Sorted Set, Hash)  ￼
	6.	보안(ACL/TLS/네트워크 격리)  ￼

⸻

바로 시작 가능한 “미니프로젝트” 3개
	1.	Leaderboard 서비스: 점수 갱신, Top-N, 내 랭킹, 동점 규칙
	2.	Coupon Drop(선착순): 원자성/Lua/재시도/중복 방지
	3.	Cache Layer: cache-aside + 락 + TTL jitter + eviction 실험
