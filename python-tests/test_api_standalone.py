"""
독립 실행형 API 테스트 파일
Import 문제 없이 바로 실행 가능
"""
import json
import time
from datetime import datetime
from typing import Any, Dict, List

import pytest
import requests

# 설정 상수들
BASE_URL = "https://jsonplaceholder.typicode.com"
VALID_POST_ID = 1
INVALID_POST_ID = 999
VALID_USER_ID = 1
TIMEOUT = 10
MAX_RESPONSE_TIME = 2000  # milliseconds


class APITestClient:
    """API 테스트를 위한 클라이언트 클래스"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "QA-API-Test-Suite/1.0"
        })
        self.last_response = None
        self.response_history = []

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """HTTP 요청 실행 및 응답 시간 측정"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()

        try:
            response = self.session.request(method, url, timeout=TIMEOUT, **kwargs)
            response_time = (time.time() - start_time) * 1000
            response.response_time = response_time

            self.last_response = response
            self.response_history.append({
                'method': method,
                'url': url,
                'status_code': response.status_code,
                'response_time': response_time,
                'timestamp': time.time()
            })

            print(f"🌐 {method} {endpoint} - {response.status_code} ({response_time:.2f}ms)")
            return response

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {method} {endpoint} - {str(e)}")
            raise

    def get_all_posts(self):
        """모든 게시글 조회"""
        return self._make_request("GET", "/posts")

    def get_post_by_id(self, post_id: int):
        """ID로 게시글 조회"""
        return self._make_request("GET", f"/posts/{post_id}")

    def create_post(self, post_data: Dict[str, Any]):
        """새 게시글 생성"""
        return self._make_request("POST", "/posts", json=post_data)

    def update_post(self, post_id: int, post_data: Dict[str, Any]):
        """게시글 업데이트"""
        return self._make_request("PUT", f"/posts/{post_id}", json=post_data)

    def delete_post(self, post_id: int):
        """게시글 삭제"""
        return self._make_request("DELETE", f"/posts/{post_id}")

    def get_posts_by_user(self, user_id: int):
        """사용자별 게시글 조회"""
        return self._make_request("GET", "/posts", params={"userId": user_id})

    def close(self):
        """세션 정리"""
        if self.session:
            self.session.close()


# Pytest Fixtures
@pytest.fixture(scope="session")
def api_client():
    """API 클라이언트 픽스처"""
    client = APITestClient()
    yield client
    client.close()


@pytest.fixture
def valid_post_data():
    """유효한 게시글 데이터"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return {
        "title": f"Automated Test Post {timestamp}",
        "body": f"This is a test post created by automated testing at {datetime.now().isoformat()}",
        "userId": VALID_USER_ID
    }


@pytest.fixture
def invalid_post_data():
    """무효한 게시글 데이터 (필수 필드 누락)"""
    return {
        "body": "Post without title field",
        "userId": VALID_USER_ID
        # title 필드 의도적으로 누락
    }


# 테스트 클래스들
class TestAPIHealth:
    """API 기본 동작 테스트"""

    @pytest.mark.smoke
    def test_api_connection(self, api_client):
        """API 서버 연결 테스트"""
        response = api_client.get_all_posts()

        assert response.status_code == 200
        assert 'application/json' in response.headers.get('content-type', '')
        assert response.response_time < MAX_RESPONSE_TIME

        print(f"✅ API 연결 성공: {response.response_time:.2f}ms")


class TestGetPosts:
    """게시글 조회 테스트"""

    @pytest.mark.functional
    def test_get_all_posts_success(self, api_client):
        """전체 게시글 조회 성공 테스트"""
        response = api_client.get_all_posts()

        # 기본 응답 검증
        assert response.status_code == 200

        # JSON 데이터 검증
        posts = response.json()
        assert isinstance(posts, list)
        assert len(posts) == 100

        # 첫 번째 게시글 구조 검증
        first_post = posts[0]
        required_fields = ['id', 'title', 'body', 'userId']
        for field in required_fields:
            assert field in first_post, f"Missing field: {field}"
            assert first_post[field] is not None, f"Field {field} is None"

        # 데이터 타입 검증
        assert isinstance(first_post['id'], int)
        assert isinstance(first_post['title'], str)
        assert isinstance(first_post['body'], str)
        assert isinstance(first_post['userId'], int)

        print(f"✅ 전체 게시글 조회: {len(posts)}개 게시글")

    @pytest.mark.functional
    def test_get_single_post_valid_id(self, api_client):
        """유효한 ID로 단일 게시글 조회"""
        response = api_client.get_post_by_id(VALID_POST_ID)

        assert response.status_code == 200

        post = response.json()
        assert isinstance(post, dict)
        assert post['id'] == VALID_POST_ID

        # 필수 필드 검증
        required_fields = ['id', 'title', 'body', 'userId']
        for field in required_fields:
            assert field in post
            assert post[field] is not None

        # 내용 검증
        assert len(post['title'].strip()) > 0
        assert len(post['body'].strip()) > 0
        assert post['userId'] > 0

        print(f"✅ 게시글 조회 성공: ID {VALID_POST_ID}")

    @pytest.mark.negative
    def test_get_single_post_invalid_id(self, api_client):
        """존재하지 않는 ID로 게시글 조회"""
        response = api_client.get_post_by_id(INVALID_POST_ID)

        # JSONPlaceholder는 404 대신 빈 객체를 반환할 수 있음
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            post = response.json()
            assert isinstance(post, dict)

        print(f"✅ 존재하지 않는 게시글 조회: ID {INVALID_POST_ID}, 상태: {response.status_code}")

    @pytest.mark.functional
    def test_get_posts_by_user(self, api_client):
        """사용자별 게시글 조회"""
        response = api_client.get_posts_by_user(VALID_USER_ID)

        assert response.status_code == 200

        user_posts = response.json()
        assert isinstance(user_posts, list)
        assert len(user_posts) > 0

        # 모든 게시글이 해당 사용자의 것인지 확인
        for post in user_posts:
            assert post['userId'] == VALID_USER_ID

        print(f"✅ 사용자 {VALID_USER_ID}의 게시글: {len(user_posts)}개")


class TestCreatePosts:
    """게시글 생성 테스트"""

    @pytest.mark.functional
    def test_create_post_success(self, api_client, valid_post_data):
        """새 게시글 생성 성공 테스트"""
        response = api_client.create_post(valid_post_data)

        assert response.status_code == 201

        created_post = response.json()
        assert isinstance(created_post, dict)
        assert 'id' in created_post
        assert isinstance(created_post['id'], int)
        assert created_post['id'] > 0

        # 제출한 데이터와 비교
        assert created_post['title'] == valid_post_data['title']
        assert created_post['body'] == valid_post_data['body']
        assert created_post['userId'] == valid_post_data['userId']

        print(f"✅ 게시글 생성 성공: ID {created_post['id']}")

    @pytest.mark.negative
    def test_create_post_missing_title(self, api_client, invalid_post_data):
        """필수 필드 누락으로 게시글 생성"""
        response = api_client.create_post(invalid_post_data)

        # JSONPlaceholder는 실제 검증을 하지 않으므로 201을 반환할 수 있음
        valid_status_codes = [201, 400, 422]
        assert response.status_code in valid_status_codes

        print(f"✅ 필수 필드 누락 테스트: 상태 코드 {response.status_code}")

    @pytest.mark.negative
    def test_create_post_empty_data(self, api_client):
        """빈 데이터로 게시글 생성"""
        response = api_client.create_post({})

        valid_status_codes = [201, 400, 422]
        assert response.status_code in valid_status_codes

        print(f"✅ 빈 데이터 테스트: 상태 코드 {response.status_code}")


class TestUpdateDeletePosts:
    """게시글 수정/삭제 테스트"""

    @pytest.mark.functional
    def test_update_post_success(self, api_client):
        """게시글 업데이트 테스트"""
        update_data = {
            "id": VALID_POST_ID,
            "title": f"Updated Title {int(time.time())}",
            "body": "Updated content by automated test",
            "userId": VALID_USER_ID
        }

        response = api_client.update_post(VALID_POST_ID, update_data)

        assert response.status_code == 200

        updated_post = response.json()
        assert updated_post['id'] == VALID_POST_ID
        assert updated_post['title'] == update_data['title']
        assert updated_post['body'] == update_data['body']

        print(f"✅ 게시글 업데이트 성공: ID {VALID_POST_ID}")

    @pytest.mark.functional
    def test_delete_post_success(self, api_client):
        """게시글 삭제 테스트"""
        response = api_client.delete_post(VALID_POST_ID)

        # 삭제 성공 코드
        assert response.status_code in [200, 204]

        print(f"✅ 게시글 삭제: ID {VALID_POST_ID}, 상태 {response.status_code}")


class TestPerformance:
    """성능 테스트"""

    @pytest.mark.performance
    def test_response_time_get_all_posts(self, api_client):
        """전체 게시글 조회 성능 테스트"""
        response_times = []

        for i in range(5):
            response = api_client.get_all_posts()
            assert response.status_code == 200
            response_times.append(response.response_time)
            time.sleep(0.1)  # API 부하 방지

        avg_time = sum(response_times) / len(response_times)
        max_time = max(response_times)
        min_time = min(response_times)

        print(f"\n📊 성능 테스트 결과:")
        print(f"   평균 응답 시간: {avg_time:.2f}ms")
        print(f"   최대 응답 시간: {max_time:.2f}ms")
        print(f"   최소 응답 시간: {min_time:.2f}ms")
        print(f"   모든 응답 시간: {[f'{t:.2f}ms' for t in response_times]}")

        # 성능 기준 검증
        assert avg_time < 2000, f"평균 응답 시간이 너무 느림: {avg_time:.2f}ms"
        assert max_time < 3000, f"최대 응답 시간이 너무 느림: {max_time:.2f}ms"

    @pytest.mark.performance
    def test_concurrent_requests_simulation(self, api_client):
        """동시 요청 시뮬레이션"""
        import queue
        import threading

        results = queue.Queue()

        def make_request():
            try:
                response = api_client.get_post_by_id(1)
                results.put({
                    'success': True,
                    'status_code': response.status_code,
                    'response_time': response.response_time
                })
            except Exception as e:
                results.put({
                    'success': False,
                    'error': str(e)
                })

        # 5개의 동시 요청
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()

        # 모든 쓰레드 완료 대기
        for thread in threads:
            thread.join()

        # 결과 수집
        successful_requests = 0
        response_times = []

        while not results.empty():
            result = results.get()
            if result['success']:
                successful_requests += 1
                response_times.append(result['response_time'])

        print(f"\n🚀 동시 요청 테스트:")
        print(f"   성공한 요청: {successful_requests}/5")
        if response_times:
            print(f"   평균 응답 시간: {sum(response_times) / len(response_times):.2f}ms")

        assert successful_requests >= 4, "동시 요청 중 너무 많은 실패"


if __name__ == "__main__":
    # 직접 실행 시 간단한 테스트
    print("🧪 독립 실행형 API 테스트 시작...")

    client = APITestClient()

    try:
        # 기본 연결 테스트
        response = client.get_all_posts()
        print(f"✅ API 연결 테스트 통과: {response.status_code}")

        # 단일 게시글 테스트
        response = client.get_post_by_id(1)
        print(f"✅ 단일 게시글 테스트 통과: {response.status_code}")

        # 게시글 생성 테스트
        test_data = {
            "title": "Direct Test Post",
            "body": "This is a direct test",
            "userId": 1
        }
        response = client.create_post(test_data)
        print(f"✅ 게시글 생성 테스트 통과: {response.status_code}")

        print("\n🎉 모든 기본 테스트 통과!")

    except Exception as e:
        print(f"❌ 테스트 실패: {e}")

    finally:
        client.close()
        print("테스트 완료!")