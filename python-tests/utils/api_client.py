"""
API 클라이언트 유틸리티 클래스
"""
import json
import logging
import time
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 로거 설정
logger = logging.getLogger(__name__)


class APIClient:
    """API 테스트를 위한 클라이언트 클래스"""

    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.last_response = None
        self.response_history = []

        # 재시도 설정
        retry_strategy = Retry(
            total=config.retry_count,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # 기본 헤더 설정
        self.session.headers.update(config.headers)

    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """HTTP 요청 실행"""
        url = f"{self.config.base_url}{endpoint}"

        # 요청 시작 시간 기록
        start_time = time.time()

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.config.timeout,
                **kwargs
            )

            # 응답 시간 계산
            response_time = (time.time() - start_time) * 1000  # milliseconds

            # 응답 정보 저장
            self.last_response = response
            self.response_history.append({
                'method': method,
                'url': url,
                'status_code': response.status_code,
                'response_time': response_time,
                'timestamp': time.time()
            })

            # 응답 시간을 response 객체에 추가
            response.response_time = response_time

            logger.info(f"{method} {url} - {response.status_code} ({response_time:.2f}ms)")

            return response

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {method} {url} - {str(e)}")
            raise

    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """GET 요청"""
        return self._make_request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict] = None,
             json_data: Optional[Dict] = None) -> requests.Response:
        """POST 요청"""
        kwargs = {}
        if data:
            kwargs['data'] = data
        if json_data:
            kwargs['json'] = json_data

        return self._make_request("POST", endpoint, **kwargs)

    def put(self, endpoint: str, data: Optional[Dict] = None,
            json_data: Optional[Dict] = None) -> requests.Response:
        """PUT 요청"""
        kwargs = {}
        if data:
            kwargs['data'] = data
        if json_data:
            kwargs['json'] = json_data

        return self._make_request("PUT", endpoint, **kwargs)

    def delete(self, endpoint: str) -> requests.Response:
        """DELETE 요청"""
        return self._make_request("DELETE", endpoint)

    def get_all_posts(self) -> requests.Response:
        """모든 게시글 조회"""
        return self.get("/posts")

    def get_post_by_id(self, post_id: int) -> requests.Response:
        """ID로 게시글 조회"""
        return self.get(f"/posts/{post_id}")

    def create_post(self, post_data: Dict[str, Any]) -> requests.Response:
        """새 게시글 생성"""
        return self.post("/posts", json_data=post_data)

    def update_post(self, post_id: int, post_data: Dict[str, Any]) -> requests.Response:
        """게시글 업데이트"""
        return self.put(f"/posts/{post_id}", json_data=post_data)

    def delete_post(self, post_id: int) -> requests.Response:
        """게시글 삭제"""
        return self.delete(f"/posts/{post_id}")

    def get_posts_by_user(self, user_id: int) -> requests.Response:
        """사용자별 게시글 조회"""
        return self.get("/posts", params={"userId": user_id})

    def validate_response_structure(self, response: requests.Response,
                                    expected_fields: List[str]) -> bool:
        """응답 구조 검증"""
        try:
            json_data = response.json()

            if isinstance(json_data, list):
                # 배열인 경우 첫 번째 항목 검증
                if len(json_data) > 0:
                    item = json_data[0]
                    return all(field in item for field in expected_fields)
                return True  # 빈 배열은 valid

            elif isinstance(json_data, dict):
                # 객체인 경우 직접 검증
                return all(field in json_data for field in expected_fields)

            return False

        except (json.JSONDecodeError, KeyError):
            return False

    def is_response_time_acceptable(self, response: requests.Response,
                                    threshold_ms: int = None) -> bool:
        """응답 시간 검증"""
        threshold = threshold_ms or self.config.timeout * 1000
        return hasattr(response, 'response_time') and response.response_time < threshold

    def get_response_stats(self) -> Dict[str, Any]:
        """응답 통계 정보 반환"""
        if not self.response_history:
            return {}

        response_times = [r['response_time'] for r in self.response_history]
        status_codes = [r['status_code'] for r in self.response_history]

        return {
            'total_requests': len(self.response_history),
            'avg_response_time': sum(response_times) / len(response_times),
            'max_response_time': max(response_times),
            'min_response_time': min(response_times),
            'status_code_distribution': {
                code: status_codes.count(code) for code in set(status_codes)
            }
        }

    def close(self):
        """세션 정리"""
        if self.session:
            self.session.close()
            logger.info("API Client session closed")