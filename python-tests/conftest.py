"""
pytest 설정 및 공통 픽스처
"""
import pytest
import requests
import os
import sys
from typing import Generator
import json
from datetime import datetime

# 프로젝트 루트 경로 추가 (여러 방법으로 시도)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

try:
    from config.config import TestConfig
    from python_tests.utils.api_client import APIClient
except ImportError:
    # 대안 import 경로 시도
    try:
        import sys
        sys.path.append(os.path.join(project_root, 'python-tests', 'utils'))
        sys.path.append(os.path.join(project_root, 'config'))

        from config import TestConfig
        from api_client import APIClient
    except ImportError as e:
        # 최후의 수단: 직접 정의
        print(f"Import 오류로 인해 기본 설정 사용: {e}")

        class TestConfig:
            class JSONPLACEHOLDER_API:
                base_url = "https://jsonplaceholder.typicode.com"
                timeout = 10
                retry_count = 3
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }

            VALID_POST_ID = 1
            INVALID_POST_ID = 999
            VALID_USER_ID = 1
            RESPONSE_TIME_THRESHOLD = 2000
            MAX_POSTS_COUNT = 100
            REPORT_DIR = os.path.join(os.getcwd(), "python-tests", "reports")

            @classmethod
            def get_config_by_env(cls, env="test"):
                return cls.JSONPLACEHOLDER_API

        # 간단한 API 클라이언트 정의
        import requests
        import time

        class APIClient:
            def __init__(self, config):
                self.config = config
                self.session = requests.Session()
                self.session.headers.update(config.headers)
                self.last_response = None
                self.response_history = []

            def _make_request(self, method, endpoint, **kwargs):
                url = f"{self.config.base_url}{endpoint}"
                start_time = time.time()
                response = self.session.request(method, url, timeout=self.config.timeout, **kwargs)
                response.response_time = (time.time() - start_time) * 1000
                self.last_response = response
                return response

            def get(self, endpoint, params=None):
                return self._make_request("GET", endpoint, params=params)

            def post(self, endpoint, json_data=None):
                return self._make_request("POST", endpoint, json=json_data)

            def get_all_posts(self):
                return self.get("/posts")

            def get_post_by_id(self, post_id):
                return self.get(f"/posts/{post_id}")

            def create_post(self, post_data):
                return self.post("/posts", json_data=post_data)

            def close(self):
                if hasattr(self, 'session'):
                    self.session.close()

# pytest 설정
def pytest_configure(config):
    """pytest 실행 전 설정"""
    # 리포트 디렉토리 생성
    os.makedirs(TestConfig.REPORT_DIR, exist_ok=True)

    # 테스트 시작 시간 기록
    config._test_start_time = datetime.now()

def pytest_sessionfinish(session, exitstatus):
    """테스트 세션 종료 후 실행"""
    print(f"\n{'='*50}")
    print("테스트 실행 완료!")
    print(f"종료 코드: {exitstatus}")
    print(f"{'='*50}")

@pytest.fixture(scope="session")
def api_config():
    """API 설정 픽스처"""
    return TestConfig.get_config_by_env("test")

@pytest.fixture(scope="session")
def api_client(api_config) -> Generator[APIClient, None, None]:
    """API 클라이언트 픽스처"""
    client = APIClient(api_config)
    yield client
    # 테스트 후 정리 작업
    client.close()

@pytest.fixture(scope="function")
def valid_post_data():
    """유효한 게시글 데이터"""
    return {
        "title": f"Test Post {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "body": "This is a test post created by automated testing.",
        "userId": TestConfig.VALID_USER_ID
    }

@pytest.fixture(scope="function")
def invalid_post_data():
    """무효한 게시글 데이터 (필수 필드 누락)"""
    return {
        "body": "Post without title field",
        "userId": TestConfig.VALID_USER_ID
        # title 필드 의도적으로 누락
    }

@pytest.fixture(scope="session")
def test_data():
    """테스트 데이터 로드"""
    test_data_path = os.path.join(
        os.path.dirname(__file__),
        "test_data",
        "test_posts_data.json"
    )

    # 테스트 데이터 파일이 없으면 기본값 생성
    if not os.path.exists(test_data_path):
        default_data = {
            "valid_posts": [
                {"id": 1, "expected_title": "sunt aut facere"},
                {"id": 2, "expected_title": "qui est esse"},
                {"id": 3, "expected_title": "ea molestias quasi"}
            ],
            "invalid_ids": [0, -1, 999, 1001, "abc", ""],
            "test_posts": [
                {
                    "title": "Test Post 1",
                    "body": "Test content 1",
                    "userId": 1
                },
                {
                    "title": "Test Post 2",
                    "body": "Test content 2",
                    "userId": 2
                }
            ]
        }

        # 디렉토리 생성 및 파일 저장
        os.makedirs(os.path.dirname(test_data_path), exist_ok=True)
        with open(test_data_path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=2, ensure_ascii=False)

    # 테스트 데이터 로드
    with open(test_data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# pytest 마커 정의
def pytest_configure(config):
    """커스텀 마커 등록"""
    config.addinivalue_line(
        "markers", "smoke: 기본 동작 확인용 스모크 테스트"
    )
    config.addinivalue_line(
        "markers", "functional: 기능 테스트"
    )
    config.addinivalue_line(
        "markers", "negative: 네거티브 테스트 (오류 상황)"
    )
    config.addinivalue_line(
        "markers", "performance: 성능 테스트"
    )

# 테스트 실행 전후 훅
@pytest.fixture(autouse=True)
def log_test_info(request):
    """각 테스트 실행 시 로그 출력"""
    test_name = request.node.name
    print(f"\n🧪 실행 중: {test_name}")
    yield
    print(f"✅ 완료: {test_name}")

# 실패한 테스트에 대한 추가 정보 수집
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """테스트 결과에 추가 정보 첨부"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # 실패한 테스트에 대한 추가 정보
        if hasattr(item, 'funcargs'):
            # API 응답이 있다면 로그에 추가
            if 'api_client' in item.funcargs:
                api_client = item.funcargs['api_client']
                if hasattr(api_client, 'last_response'):
                    rep.sections.append((
                        'Last API Response',
                        f"Status: {api_client.last_response.status_code}\n"
                        f"Response: {api_client.last_response.text}"
                    ))