"""
테스트 헬퍼 함수들
"""
import json
import time
import random
import string
from typing import Dict, Any, List, Optional
from datetime import datetime
import requests


def generate_random_post_data(user_id: int = 1) -> Dict[str, Any]:
    """랜덤한 게시글 데이터 생성"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = ''.join(random.choices(string.ascii_lowercase, k=4))

    return {
        "title": f"Test Post {timestamp}_{random_suffix}",
        "body": f"This is automated test content created at {datetime.now().isoformat()}. "
                f"Random data: {''.join(random.choices(string.ascii_letters + string.digits, k=20))}",
        "userId": user_id
    }


def generate_invalid_post_data() -> List[Dict[str, Any]]:
    """다양한 잘못된 게시글 데이터 생성"""
    return [
        {},  # 빈 객체
        {"title": ""},  # 빈 제목
        {"title": "Valid Title"},  # body 누락
        {"body": "Valid Body"},  # title 누락
        {"title": "Valid Title", "body": "Valid Body"},  # userId 누락
        {"title": None, "body": "Valid Body", "userId": 1},  # null 제목
        {"title": "Valid Title", "body": None, "userId": 1},  # null 본문
        {"title": 123, "body": "Valid Body", "userId": 1},  # 잘못된 데이터 타입
        {"title": "Valid Title", "body": "Valid Body", "userId": "invalid"},  # 잘못된 userId
        {"title": "A" * 1000, "body": "Valid Body", "userId": 1},  # 너무 긴 제목
    ]


def validate_post_structure(post_data: Dict[str, Any], required_fields: List[str] = None) -> bool:
    """게시글 데이터 구조 검증"""
    if required_fields is None:
        required_fields = ['id', 'title', 'body', 'userId']

    if not isinstance(post_data, dict):
        return False

    for field in required_fields:
        if field not in post_data:
            return False
        if post_data[field] is None:
            return False

    return True


def validate_response_json(response: requests.Response) -> bool:
    """HTTP 응답이 유효한 JSON인지 확인"""
    try:
        response.json()
        return True
    except (json.JSONDecodeError, ValueError):
        return False


def measure_response_time(func, *args, **kwargs) -> tuple:
    """함수 실행 시간 측정"""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    response_time = (end_time - start_time) * 1000  # milliseconds

    return result, response_time


def create_test_report_data(test_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """테스트 결과를 리포트 형태로 정리"""
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results if result.get('status') == 'passed')
    failed_tests = total_tests - passed_tests

    total_time = sum(result.get('duration', 0) for result in test_results)
    avg_time = total_time / total_tests if total_tests > 0 else 0

    return {
        "summary": {
            "total": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "pass_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "total_duration": total_time,
            "avg_duration": avg_time
        },
        "details": test_results,
        "generated_at": datetime.now().isoformat()
    }


def assert_response_time(response: requests.Response, max_time_ms: int = 2000):
    """응답 시간 assertion"""
    if hasattr(response, 'response_time'):
        response_time = response.response_time
    else:
        response_time = 0  # 기본값

    assert response_time < max_time_ms, \
        f"Response time {response_time}ms exceeds maximum {max_time_ms}ms"


def assert_valid_json_response(response: requests.Response):
    """유효한 JSON 응답인지 assertion"""
    assert validate_response_json(response), \
        f"Response is not valid JSON: {response.text[:200]}..."


def assert_status_code(response: requests.Response, expected_codes: List[int]):
    """상태 코드 assertion (여러 코드 허용)"""
    if isinstance(expected_codes, int):
        expected_codes = [expected_codes]

    assert response.status_code in expected_codes, \
        f"Expected status code in {expected_codes}, got {response.status_code}"


def log_test_info(test_name: str, **kwargs):
    """테스트 정보 로깅"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] 🧪 {test_name}")

    for key, value in kwargs.items():
        print(f"  {key}: {value}")


def wait_between_requests(min_ms: int = 100, max_ms: int = 300):
    """요청 간 대기 (API 레이트 리밋 방지)"""
    wait_time = random.uniform(min_ms / 1000, max_ms / 1000)
    time.sleep(wait_time)


class TestDataManager:
    """테스트 데이터 관리 클래스"""

    def __init__(self):
        self.created_posts = []
        self.test_start_time = datetime.now()

    def add_created_post(self, post_id: int):
        """생성된 게시글 ID 추가"""
        self.created_posts.append({
            'id': post_id,
            'created_at': datetime.now().isoformat()
        })

    def get_created_posts(self) -> List[Dict[str, Any]]:
        """생성된 게시글 목록 반환"""
        return self.created_posts.copy()

    def cleanup_summary(self) -> Dict[str, Any]:
        """정리 작업 요약"""
        return {
            'test_duration': (datetime.now() - self.test_start_time).total_seconds(),
            'created_posts_count': len(self.created_posts),
            'cleanup_needed': len(self.created_posts) > 0
        }


# 데코레이터 함수들
def retry_on_failure(max_retries: int = 3, delay_ms: int = 1000):
    """실패 시 재시도 데코레이터"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(f"Attempt {attempt + 1} failed, retrying in {delay_ms}ms...")
                        time.sleep(delay_ms / 1000)
                    else:
                        print(f"All {max_retries + 1} attempts failed")

            raise last_exception

        return wrapper

    return decorator


def performance_test(threshold_ms: int = 1000):
    """성능 테스트 데코레이터"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            result, response_time = measure_response_time(func, *args, **kwargs)

            print(f"Performance: {func.__name__} took {response_time:.2f}ms")

            if response_time > threshold_ms:
                print(f"⚠️  Warning: Response time {response_time:.2f}ms exceeds threshold {threshold_ms}ms")

            return result

        return wrapper

    return decorator