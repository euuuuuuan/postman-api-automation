# API 테스트 케이스 템플릿

## TC-001: GET /posts - 전체 게시글 조회

| 항목 | 내용 |
|------|------|
| **테스트 목적** | 전체 게시글 목록을 정상적으로 조회할 수 있는지 확인 |
| **API 엔드포인트** | `GET https://jsonplaceholder.typicode.com/posts` |
| **전제 조건** | - API 서버가 정상 동작 중<br>- 네트워크 연결 상태 양호 |
| **테스트 단계** | 1. GET 요청을 /posts 엔드포인트로 전송<br>2. 응답 확인 |
| **예상 결과** | - 상태 코드: 200<br>- Content-Type: application/json<br>- 응답 본문: 게시글 배열 (100개)<br>- 각 게시글은 id, title, body, userId 필드 포함 |
| **우선순위** | High |
| **카테고리** | Smoke Test, Positive Test |

---

## TC-002: GET /posts/{id} - 특정 게시글 조회 (정상 케이스)

| 항목 | 내용 |
|------|------|
| **테스트 목적** | 유효한 ID로 특정 게시글을 조회할 수 있는지 확인 |
| **API 엔드포인트** | `GET https://jsonplaceholder.typicode.com/posts/1` |
| **테스트 데이터** | id = 1 (유효한 값) |
| **전제 조건** | - 해당 ID의 게시글이 존재 |
| **테스트 단계** | 1. GET 요청을 /posts/1 엔드포인트로 전송<br>2. 응답 데이터 검증 |
| **예상 결과** | - 상태 코드: 200<br>- 응답 본문: 단일 게시글 객체<br>- id: 1, title, body, userId 필드 존재 |
| **우선순위** | High |
| **카테고리** | Functional Test, Positive Test |

---

## TC-003: GET /posts/{id} - 존재하지 않는 게시글 조회

| 항목 | 내용 |
|------|------|
| **테스트 목적** | 존재하지 않는 ID로 조회 시 적절한 에러 처리가 되는지 확인 |
| **API 엔드포인트** | `GET https://jsonplaceholder.typicode.com/posts/999` |
| **테스트 데이터** | id = 999 (존재하지 않는 값) |
| **전제 조건** | - 해당 ID의 게시글이 존재하지 않음 |
| **테스트 단계** | 1. GET 요청을 /posts/999 엔드포인트로 전송<br>2. 에러 응답 확인 |
| **예상 결과** | - 상태 코드: 404<br>- 적절한 에러 메시지 또는 빈 객체 |
| **우선순위** | Medium |
| **카테고리** | Negative Test, Error Handling |

---

## TC-004: POST /posts - 새 게시글 생성

| 항목 | 내용 |
|------|------|
| **테스트 목적** | 새로운 게시글을 정상적으로 생성할 수 있는지 확인 |
| **API 엔드포인트** | `POST https://jsonplaceholder.typicode.com/posts` |
| **요청 헤더** | Content-Type: application/json |
| **요청 본문** | ```json<br>{<br>  "title": "테스트 게시글",<br>  "body": "테스트 내용입니다.",<br>  "userId": 1<br>}<br>``` |
| **전제 조건** | - 유효한 JSON 형식의 데이터<br>- 필수 필드 모두 포함 |
| **테스트 단계** | 1. JSON 데이터를 포함한 POST 요청 전송<br>2. 생성된 리소스 정보 확인 |
| **예상 결과** | - 상태 코드: 201<br>- 응답 본문: 생성된 게시글 정보 (id 포함)<br>- Location 헤더 존재 (선택적) |
| **우선순위** | High |
| **카테고리** | Functional Test, Positive Test |

---

## TC-005: POST /posts - 필수 필드 누락

| 항목 | 내용 |
|------|------|
| **테스트 목적** | 필수 필드 누락 시 적절한 검증 에러가 발생하는지 확인 |
| **API 엔드포인트** | `POST https://jsonplaceholder.typicode.com/posts` |
| **요청 헤더** | Content-Type: application/json |
| **요청 본문** | ```json<br>{<br>  "body": "제목이 없는 게시글"<br>}<br>``` |
| **전제 조건** | - title 필드가 필수라고 가정 |
| **테스트 단계** | 1. title 필드가 누락된 POST 요청 전송<br>2. 검증 에러 응답 확인 |
| **예상 결과** | - 상태 코드: 400 또는 422<br>- 에러 메시지: 필수 필드 누락 관련 |
| **우선순위** | Medium |
| **카테고리** | Negative Test, Validation Test |

---

## 테스트 실행 체크리스트

### 실행 전 준비사항
- [ ] 테스트 환경 접근 가능 여부 확인
- [ ] 필요한 테스트 도구 준비 (Postman, curl 등)
- [ ] 테스트 데이터 준비

### 실행 중 확인사항
- [ ] 요청/응답 로그 기록
- [ ] 응답 시간 측정
- [ ] 예상 결과와 실제 결과 비교

### 실행 후 작업
- [ ] 테스트 결과 기록
- [ ] 발견된 이슈 리포트 작성
- [ ] 다음 테스트를 위한 환경 정리