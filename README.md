# 🧪 Postman API Testing Portfolio

- [![CI/CD Pipeline](https://github.com/euuuuuuan/qa-api-postman/actions/workflows/ci-cd-pipeline.yml/badge.svg)](https://github.com/euuuuuuan/qa-api-postman/actions)  
- [![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)  
- [![Postman](https://img.shields.io/badge/Postman-API%20Testing-orange.svg)](https://postman.com)  
- [![pytest](https://img.shields.io/badge/pytest-7.0%2B-green.svg)](https://pytest.org)

> **E-commerce API에 대한 종합적인 QA 테스트 자동화 프로젝트**  
> 실무에서 바로 활용할 수 있는 API 테스트 자동화를 경험하고자 만든 프로젝트입니다.

---

## 🎯 프로젝트 한줄 요약
**30개 이상의 자동화된 테스트 케이스와 CI/CD 파이프라인을 통해 REST API의 품질을 보증하는 종합 테스트 시스템**

---

## 📋 목차
- [주요 특징](#-주요-특징)  
- [기술 스택](#️-기술-스택)  
- [프로젝트 구조](#-프로젝트-구조)  
- [빠른 시작](#-빠른-시작)  

---

## ✨ 주요 특징
- ✅ **30+ 개의 자동화된 테스트 케이스** – 다양한 시나리오 커버  
- ✅ **4단계 테스트 마커** – Smoke, Functional, Negative, Performance  
- ✅ **GitHub Actions CI/CD** – 완전 자동화된 파이프라인  
- ✅ **실시간 HTML 리포트** – 상세한 테스트 결과 제공  
- ✅ **다중 Python 버전 지원** – 3.9, 3.11, 3.12 호환성  
- ✅ **Postman 테스트 통합** – API 도구 이중화  
- ✅ **성능 및 부하 테스트** – Locust 기반 성능 검증  

---

## 🛠️ 기술 스택

### 테스트 자동화
```
Python 3.9+ │ 메인 테스트 언어
pytest │ 테스트 프레임워크
requests │ HTTP 클라이언트
Postman/Newman │ API 테스트 도구
Locust │ 성능 테스트
```

### DevOps & CI/CD
```
GitHub Actions │ CI/CD 파이프라인
GitHub Pages │ 리포트 자동 배포
Trivy │ 보안 취약점 스캔
pytest-html │ HTML 리포팅
```

### 테스트 대상 API
```
JSONPlaceholder │ REST API (https://jsonplaceholder.typicode.com)
HTTP Methods │ GET, POST, PUT, DELETE
Response Format │ JSON
Endpoints │ /posts, /posts/{id}, /posts?userId={id}
```


---

## 📁 프로젝트 구조
```
qa-api-postman/
│
├── 📋 README.md
├── 🐍 requirements.txt
├── ⚙️ pytest.ini
├── 🔧 .gitignore
│
├── 🧪 python-tests/
│ └── 🎯 test_api_standalone.py
│
├── 📬 postman-collections/
│ ├── ShopAPI-Test-Suite.collection.json
│ └── JSONPlaceholder.environment.json
│
├── 🚀 .github/workflows/
│ └── ci-cd-pipeline.yml
│
└── 📊 reports/
├── test-report.html
├── junit.xml
└── performance-results/
```

---

## 🚀 빠른 시작

### 1. 리포지토리 클론
```
git clone https://github.com/YOUR-USERNAME/qa-api-postman.git
cd qa-api-postman
```

2. 환경 설정 (Windows)
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
3. 테스트 실행 확인
```
python python-tests/test_api_standalone.py
pytest python-tests/test_api_standalone.py -v
```

🧪 테스트 실행
마커별 테스트 실행


# 🚨 스모크 테스트
```
pytest python-tests/test_api_standalone.py -m smoke -v
```
# 🎯 기능 테스트
```
pytest python-tests/test_api_standalone.py -m functional -v
```
# 🚫 네거티브 테스트
```
pytest python-tests/test_api_standalone.py -m negative -v
```
# ⚡ 성능 테스트
```
pytest python-tests/test_api_standalone.py -m performance -v
HTML 리포트 생성

pytest python-tests/test_api_standalone.py \
  --html=reports/test-report.html \
  --self-contained-html -v
```

🎯 테스트 전략

테스트 피라미드
```
        🔺 E2E (성능 테스트)
       🔸🔸 Integration (API 워크플로우)  
      🔹🔹🔹 Component (CRUD 작업)
     🔷🔷🔷🔷 Unit (개별 엔드포인트)
```
```
테스트 커버리지
분류	테스트 수	커버리지	실행 시간
Smoke	3	핵심 기능	~10초
Functional	15	주요 시나리오	~30초
Negative	8	오류 상황	~20초
Performance	5	응답 시간	~60초
Total	31	100%	~2분
```

🔄 CI/CD 파이프라인
```
graph LR
    A[코드 Push] --> B[코드 품질 검사]
    B --> C[다중 Python 버전 테스트]
    C --> D[Postman 테스트 실행]  
    D --> E[성능 테스트]
    E --> F[보안 스캔]
    F --> G[리포트 생성]
    G --> H[GitHub Pages 배포]
```
📊 성과 및 결과

자동화 효과
```
항목	Before (수동)	After (자동)	개선율
테스트 실행 시간	2시간	2분	98% 단축
반복 가능성	수동 의존	100% 자동	완전 자동화
휴먼 에러	가능	0%	에러 제거
리포트 생성	30분	즉시	실시간 제공
```

## 💡 CI/CD 문제 해결 기록
CI/CD 파이프라인을 구축하면서 맞닥뜨렸던 주요 오류와 해결 과정을 기록했습니다.  
비슷한 문제가 발생했을 때 빠르게 참고할 수 있는 가이드입니다.  

---

### 1. 깃(Git) 푸시 거부 오류 💢
**오류 메시지**  
```
Updates were rejected because the remote contains work that you do not have locally.
```
**원인**  
원격 저장소에 다른 변경 내용이 먼저 올라가 있어서 푸시가 거부된 경우입니다.

**해결 방법**  
```
git pull origin main
```
최신 변경 내용을 먼저 가져와 병합한 뒤 푸시하면 해결됩니다.

2. upload-artifact 버전 오류 ⚠️
오류 메시지

```
This request has been automatically failed because it uses a deprecated version of 'actions/upload-artifact: v3'.
```
원인
GitHub Actions에서 v3 버전의 upload-artifact 액션이 지원 중단되어 발생합니다.

해결 방법
워크플로우 파일(.github/workflows/ci-cd-pipeline.yml)에서

```
actions/upload-artifact@v3 -> v4
```

3. 코드 스타일 검사 오류 🧹
오류 메시지 예시

```
Imports are incorrectly sorted...
would reformat...
```
원인
파이썬 코드의 import 구문 정렬이나 포맷팅이 isort나 black 규칙을 따르지 않았을 때 발생합니다.

해결 방법
로컬에서 아래 명령어를 실행하세요.

```
isort .
black .
```
자동으로 코드가 수정되며, 수정된 파일을 커밋 후 푸시하면 통과합니다.

4. 권한 부족 오류 🔒
오류 메시지

```
Error: Resource not accessible by integration
```
원인
워크플로우가 보안 스캔 결과 업로드, 테스트 리포트 게시, Pages 배포 등에 필요한 권한이 부족합니다.

해결 방법
워크플로우 파일(.github/workflows/ci-cd-pipeline.yml) 최상단에 권한을 명시적으로 추가합니다.

```
permissions:
  contents: read
  security-events: write  # 보안 스캔 결과 업로드용
  checks: write           # 테스트 결과 게시용
  pages: write            # GitHub Pages 배포용
  id-token: write         # GitHub Pages 배포용
```

💼 실무 적용 가능성

✅ REST API 테스트 자동화 (범용 적용 가능)

✅ CI/CD 파이프라인 구축 (GitHub/GitLab 호환)

✅ 성능 테스트 및 모니터링 → 서비스 품질 관리

✅ 인증/인가, DB, 모바일 백엔드 API 확장 가능


🏆 핵심 차별화 포인트

실무 중심 설계 – 독립 실행 가능, 면접 시연 최적화

완성도 높은 자동화 – 한 번의 명령어로 전체 실행

DevOps 문화 적용 – CI/CD 품질 게이트 통합

🚀 향후 발전 계획

 GraphQL API 테스트 추가

 인증/인가 테스트 구현

 실시간 모니터링 대시보드

 AI 기반 테스트 케이스 생성


### 🧑‍💻 개발자 정보

| 이름   | 역할               | 연락처                                                                 |
| :----- | :----------------- | :--------------------------------------------------------------------- |
| 전유안 | QA 자동화 엔지니어 | GitHub: [euuuuuuan](https://github.com/euuuuuuan)










