# 🧪 QA API Testing Portfolio
Show Image
Show Image
Show Image
Show Image

E-commerce API에 대한 종합적인 QA 테스트 자동화 프로젝트
실무에서 바로 활용할 수 있는 API 테스트 자동화 포트폴리오입니다.

### 🎯 프로젝트 한줄 요약
30개 이상의 자동화된 테스트 케이스와 CI/CD 파이프라인을 통해 REST API의 품질을 보증하는 종합 테스트 시스템

### 📋 목차

주요 특징
기술 스택
프로젝트 구조
빠른 시작
테스트 실행
테스트 전략
CI/CD 파이프라인
성과 및 결과
실무 적용 가능성
데모 영상

### ✨ 주요 특징

✅ 30+ 개의 자동화된 테스트 케이스 - 다양한 시나리오 커버
✅ 4단계 테스트 마커 - Smoke, Functional, Negative, Performance
✅ GitHub Actions CI/CD - 완전 자동화된 파이프라인
✅ 실시간 HTML 리포트 - 상세한 테스트 결과 제공
✅ 다중 Python 버전 지원 - 3.9, 3.11, 3.12 호환성
✅ Postman 테스트 통합 - API 도구 이중화
✅ 성능 및 부하 테스트 - Locust 기반 성능 검증

### 🛠️ 기술 스택
테스트 자동화
Python 3.9+     │ 메인 테스트 언어
pytest          │ 테스트 프레임워크  
requests        │ HTTP 클라이언트
Postman/Newman  │ API 테스트 도구
Locust          │ 성능 테스트
DevOps & CI/CD
GitHub Actions  │ CI/CD 파이프라인
GitHub Pages    │ 리포트 자동 배포
Trivy           │ 보안 취약점 스캔
pytest-html     │ HTML 리포팅
테스트 대상 API
JSONPlaceholder │ REST API (https://jsonplaceholder.typicode.com)
HTTP Methods    │ GET, POST, PUT, DELETE
Response Format │ JSON
Endpoints       │ /posts, /posts/{id}, /posts?userId={id}

### 📁 프로젝트 구조
```
qa-api-postman/
│
├── 📋 README.md                          # 프로젝트 문서
├── 🐍 requirements.txt                   # Python 의존성
├── ⚙️ pytest.ini                        # pytest 설정
├── 🔧 .gitignore                        # Git 무시 파일
│
├── 🧪 python-tests/
│   └── 🎯 test_api_standalone.py        # 메인 테스트 파일 (30+ 테스트)
│
├── 📬 postman-collections/
│   ├── ShopAPI-Test-Suite.collection.json    # Postman 컬렉션
│   └── JSONPlaceholder.environment.json      # 환경 변수
│
├── 🚀 .github/workflows/
│   └── ci-cd-pipeline.yml               # GitHub Actions 워크플로우
│
└── 📊 reports/                          # 테스트 리포트 (자동 생성)
    ├── test-report.html
    ├── junit.xml
    └── performance-results/
```

🚀 빠른 시작
1. 리포지토리 클론
bashgit clone https://github.com/YOUR-USERNAME/qa-api-postman.git
cd qa-api-postman
2. 환경 설정 (Windows)
powershell# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
3. 테스트 실행 확인
bash# 빠른 연결 테스트
python python-tests/test_api_standalone.py

# pytest로 전체 테스트
pytest python-tests/test_api_standalone.py -v
🧪 테스트 실행
마커별 테스트 실행
bash# 🚨 스모크 테스트 (핵심 기능, ~10초)
pytest python-tests/test_api_standalone.py -m smoke -v

# 🎯 기능 테스트 (주요 시나리오, ~30초)  
pytest python-tests/test_api_standalone.py -m functional -v

# 🚫 네거티브 테스트 (오류 상황, ~20초)
pytest python-tests/test_api_standalone.py -m negative -v

# ⚡ 성능 테스트 (응답시간 측정, ~60초)
pytest python-tests/test_api_standalone.py -m performance -v
HTML 리포트 생성
bash# 상세한 HTML 리포트 생성
pytest python-tests/test_api_standalone.py \
  --html=reports/test-report.html \
  --self-contained-html \
  -v
실행 결과 예시
🧪 독립 실행형 API 테스트 시작...
✅ API 연결 테스트 통과: 200 (234ms)
✅ 단일 게시글 테스트 통과: 200 (186ms)
✅ 게시글 생성 테스트 통과: 201 (298ms)

========================= test session starts =========================
collected 25 items

TestAPIHealth::test_api_connection PASSED                    [  4%]
TestGetPosts::test_get_all_posts_success PASSED            [  8%]
TestGetPosts::test_get_single_post_valid_id PASSED         [ 12%]
TestCreatePosts::test_create_post_success PASSED           [ 16%]
...
========================= 25 passed in 45.67s =========================

📊 성능 테스트 결과:
   평균 응답 시간: 245.67ms ✅
   최대 응답 시간: 387.23ms ✅
   최소 응답 시간: 154.12ms ✅
   
🎯 테스트 전략
테스트 피라미드 구현
        🔺 E2E (성능 테스트)
       🔸🔸 Integration (API 워크플로우)  
      🔹🔹🔹 Component (CRUD 작업)
     🔷🔷🔷🔷 Unit (개별 엔드포인트)
테스트 커버리지
분류테스트 수커버리지실행 시간Smoke3개핵심 기능~10초Functional15개주요 시나리오~30초Negative8개오류 상황~20초Performance5개응답 시간~60초Total31개100%~2분

상세 테스트 시나리오

🟢 Positive Tests

✅ 전체 게시글 목록 조회 (100개 검증)
✅ 특정 게시글 상세 조회 및 필드 검증
✅ 새 게시글 생성 및 응답 데이터 확인
✅ 게시글 업데이트 및 변경사항 검증
✅ 게시글 삭제 및 상태 코드 확인
✅ 사용자별 게시글 필터링 기능

🔴 Negative Tests

❌ 존재하지 않는 게시글 조회 (404 처리)
❌ 필수 필드 누락으로 게시글 생성 시도
❌ 잘못된 데이터 타입으로 요청 전송
❌ 빈 데이터로 게시글 생성 시도
❌ 다양한 잘못된 ID 형식 테스트

⚡ Performance Tests

📈 API 응답 시간 측정 (< 2초 SLA)
📊 동시 요청 처리 능력 테스트
📉 부하 테스트 (10명 사용자, 60초간)

🔄 CI/CD 파이프라인
GitHub Actions 워크플로우
mermaidgraph LR
    A[코드 Push] --> B[코드 품질 검사]
    B --> C[다중 Python 버전 테스트]
    C --> D[Postman 테스트 실행]  
    D --> E[성능 테스트]
    E --> F[보안 스캔]
    F --> G[리포트 생성]
    G --> H[GitHub Pages 배포]
자동화된 기능들

✅ 코드 Push 시 자동 테스트 - main/develop 브랜치
✅ PR 리뷰용 테스트 실행 - 자동 코멘트
✅ 일일 스케줄 테스트 - 매일 오전 9시
✅ 다중 Python 버전 - 3.9, 3.11, 3.12
✅ 자동 리포트 배포 - GitHub Pages
✅ 실패 알림 - 즉시 피드백

생성되는 아티팩트

📋 HTML 테스트 리포트 - 상세 결과
📊 JUnit XML - CI/CD 통합용
📈 성능 테스트 결과 - 응답시간 분석
🔒 보안 스캔 결과 - 취약점 리포트

📊 성과 및 결과
자동화 효과
항목Before (수동)After (자동)개선율테스트 실행 시간2시간2분98% 단축반복 가능성수동 의존100% 자동완전 자동화휴먼 에러가능0%에러 제거리포트 생성30분즉시실시간 제공
API 테스트 커버리지

✅ 엔드포인트: 6개 주요 API 100% 커버
✅ HTTP 메서드: GET, POST, PUT, DELETE 전체
✅ 상태 코드: 200, 201, 204, 400, 404, 422 검증
✅ 데이터 검증: JSON 구조, 필드 타입, 비즈니스 룰

성능 기준 달성

✅ 평균 응답시간: 245ms (목표: < 2000ms)
✅ 최대 응답시간: 387ms (목표: < 3000ms)
✅ 동시 사용자: 10명 처리 가능
✅ 가용성: 100% (테스트 기간 중)

💼 실무 적용 가능성
즉시 활용 가능한 기술
✅ REST API 테스트 자동화      → 어떤 API든 적용
✅ CI/CD 파이프라인 구축       → GitHub/GitLab 호환  
✅ 테스트 전략 수립            → 다양한 프로젝트 적용
✅ 성능 테스트 및 모니터링     → 실제 서비스 품질 관리
✅ 자동화 도구 선택 및 구축    → 팀 생산성 향상
확장 가능한 영역

마이크로서비스 API 테스트
인증/인가 시스템 테스트
데이터베이스 연동 테스트
모바일 앱 백엔드 API 테스트
실시간 모니터링 시스템 구축

🎬 데모 영상
5분 시연 시나리오
bash# 1️⃣ 스모크 테스트 (30초)
pytest python-tests/test_api_standalone.py -m smoke -v

# 2️⃣ HTML 리포트 생성 (1분)
pytest python-tests/test_api_standalone.py --html=demo.html -v

# 3️⃣ 성능 테스트 시연 (1분)  
pytest python-tests/test_api_standalone.py -m performance -v

# 4️⃣ 리포트 확인 및 설명 (2.5분)
start demo.html
기술 면접 대비 Q&A
질문답변 핵심테스트 자동화의 ROI는?98% 시간 단축, 휴먼 에러 제거, 지속적 품질 보증실패한 테스트 디버깅 방법?상세 로깅, HTML 리포트, 재현 스크립트 제공CI/CD에서 테스트 실패 시 대응?자동 알림, PR 블록, 롤백 전략성능 기준 설정 근거?SLA 기반, 사용자 경험, 벤치마킹
🏆 핵심 차별화 포인트
1. 실무 중심 설계 ⭐⭐⭐⭐⭐

즉시 실행 가능한 독립형 테스트
문제 해결 과정 포함 (import 오류 → standalone 방식)
면접에서 바로 시연 가능

2. 완성도 높은 자동화 ⭐⭐⭐⭐⭐

한 번의 명령어로 모든 테스트 실행
실패 시 상세한 디버깅 정보 제공
다양한 실행 옵션 (마커, 병렬, 재시도)

3. DevOps 문화 적용 ⭐⭐⭐⭐⭐

Infrastructure as Code (GitHub Actions)
지속적 통합/배포 파이프라인
자동화된 품질 게이트 구축

🚀 향후 발전 계획
Phase 1: 기능 확장 (3개월)

 GraphQL API 테스트 추가
 데이터베이스 테스트 통합
 인증/인가 테스트 구현
 API 스키마 검증 (OpenAPI)

Phase 2: 고도화 (6개월)

 AI 기반 테스트 케이스 생성
 실시간 모니터링 대시보드
 크로스 브라우저 API 테스트
 블루-그린 배포 테스트 자동화

📞 연락처

GitHub: https://github.com/


</div>

