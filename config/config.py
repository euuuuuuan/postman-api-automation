"""
API 테스트 환경 설정
"""
import os
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class APIConfig:
    """API 테스트 설정 클래스"""
    base_url: str
    timeout: int
    retry_count: int
    headers: Dict[str, str]


class TestConfig:
    """테스트 환경 설정"""

    # 기본 API 설정
    JSONPLACEHOLDER_API = APIConfig(
        base_url="https://jsonplaceholder.typicode.com",
        timeout=10,
        retry_count=3,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "QA-API-Test-Suite/1.0"
        }
    )

    # 테스트 데이터
    VALID_POST_ID = 1
    INVALID_POST_ID = 999
    VALID_USER_ID = 1

    # 테스트 실행 설정
    RESPONSE_TIME_THRESHOLD = 2000  # milliseconds
    MAX_POSTS_COUNT = 100

    # 리포트 설정
    REPORT_DIR = os.path.join(os.getcwd(), "python-tests", "reports")

    # 환경별 설정
    @classmethod
    def get_config_by_env(cls, env: str = "test") -> APIConfig:
        """환경에 따른 설정 반환"""
        configs = {
            "test": cls.JSONPLACEHOLDER_API,
            "dev": cls.JSONPLACEHOLDER_API,  # 추후 확장 가능
            "staging": cls.JSONPLACEHOLDER_API  # 추후 확장 가능
        }
        return configs.get(env, cls.JSONPLACEHOLDER_API)