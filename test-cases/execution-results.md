### TC-001 실행결과
- 실행일시: 2025-09-16
- 상태코드: 200
- 응답시간: 47ms
- 특이사항: 실제로는 100개가 아닌 100개의 게시글 반환됨

### TC-002 실행결과
- 실행일시: 2025-09-16
- 상태코드: 200
- 응답시간: 49ms
- 특이사항: 1번 객체만 반환

### TC-003 실행결과
- 실행일시: 2025-09-16
- 상태코드: 404
- 응답시간: 158ms
- 특이사항: "{}" 빈 객체 반환

### TC-004 실행결과
- 실행일시: 2025-09-16
- 상태코드: 200
- 응답시간: 124ms
- 특이사항:
- <img src="https://github.com/user-attachments/assets/3b464355-7176-4c42-b2ff-7840c8872ea6" width="300px" alt="result4" />

### TC-005 실행결과
- 실행일시: 2025-09-16
- 상태코드: 200
- 응답시간: 43ms
- 특이사항:
- <img width="300" alt="result5" src="https://github.com/user-attachments/assets/dacd576e-02ff-45d8-9d27-fd6322866b9d" />


---
### 결과요약 ###

jsonplaceholder는 실제 데이터베이스에 저장/검증하지 않는 테스트용 API이다.

그래서 POST, PUT, DELETE 요청은:

실제로는 데이터가 추가/수정/삭제되지 않음

그냥 보낸 요청 내용을 그대로 돌려주거나, 성공 상태(200/201)만 반환

따라서 필수 필드 누락 여부 같은 유효성 검증 로직도 아예 구현돼 있지 않음.


---

#### 🔹 TC-004: POST /posts (새 게시글 생성)

설정:
메서드 → POST 선택

URL 입력:
https://jsonplaceholder.typicode.com/posts

Body 탭 → raw → JSON 선택

요청 본문 입력:

{
"title": "테스트 게시글",

  "body": "테스트 내용입니다.",

  "userId": 1
}
실행하면 응답으로 생성된 게시글 데이터가 반환됨 (id 자동 생성됨)

TC-004 (POST 정상 케이스)
응답: 201 Created
응답 본문: 새 게시글 JSON (id 포함)

----

#### 🔹 TC-005: POST /posts (필수 필드 누락)
설정: 4번과 동일, 단 요청 본문만 다르게 입력

TC-005 (POST 필수 필드 누락)
응답: 400 Bad Request 또는 422 Unprocessable Entity
응답 본문: 에러 메시지





