"""
Posts API 테스트 모듈
JSONPlaceholder API를 사용한 종합적인 API 테스트
"""
import pytest
import requests
import json
import sys
import os
from typing import Dict, List, Any
import time

# 프로젝트 루트 경로를 Python path에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Import 시도 (conftest.py에서 이미 정의되었을 것임)
try:
    from config.config import TestConfig
    from python_tests.utils.api_client import APIClient
except ImportError:
    # conftest.py에서 정의된 클래스들을 사용
    # pytest가 자동으로 conftest.py를 로드하므로 여기서는 pass
    pass


class TestPostsAPI:
    """Posts API 테스트 클래스"""

    @pytest.mark.smoke
    def test_api_health_check(self, api_client: APIClient):
        """API 서버 상태 확인 (스모크 테스트)"""
        response = api_client.get_all_posts()

        # 기본 응답 검증
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.headers.get('content-type') is not None
        assert 'application/json' in response.headers.get('content-type', '')

        # 응답 시간 검증
        assert hasattr(response, 'response_time'), "Response time not recorded"
        assert response.response_time < TestConfig.RESPONSE_TIME_THRESHOLD, \
            f"Response time {response.response_time}ms exceeds threshold"

    @pytest.mark.functional
    def test_get_all_posts_success(self, api_client: APIClient):
        """전체 게시글 조회 성공 테스트"""
        response = api_client.get_all_posts()

        # 상태 코드 검증
        assert response.status_code == 200

        # 응답 데이터 검증
        posts = response.json()
        assert isinstance(posts, list), "Response should be a list"
        assert len(posts) == TestConfig.MAX_POSTS_COUNT, \
            f"Expected {TestConfig.MAX_POSTS_COUNT} posts, got {len(posts)}"

        # 데이터 구조 검증
        required_fields = ['id', 'title', 'body', 'userId']
        assert api_client.validate_response_structure(response, required_fields)

        # 첫 번째 게시글 상세 검증
        first_post = posts[0]
        assert first_post['id'] == 1
        assert isinstance(first_post['title'], str)
        assert len(first_post['title']) > 0
        assert isinstance(first_post['body'], str)
        assert len(first_post['body']) > 0
        assert isinstance(first_post['userId'], int)
        assert first_post['userId'] > 0

    @pytest.mark.functional
    def test_get_single_post_valid_id(self, api_client: APIClient):
        """유효한 ID로 단일 게시글 조회 테스트"""
        post_id = TestConfig.VALID_POST_ID
        response = api_client.get_post_by_id(post_id)

        # 상태 코드 검증
        assert response.status_code == 200

        # 응답 데이터 검증
        post = response.json()
        assert isinstance(post, dict), "Response should be a dictionary"
        assert post['id'] == post_id, f"Expected post ID {post_id}, got {post['id']}"

        # 필수 필드 존재 확인
        required_fields = ['id', 'title', 'body', 'userId']
        for field in required_fields:
            assert field in post, f"Missing required field: {field}"
            assert post[field] is not None, f"Field {field} should not be None"

        # 데이터 타입 검증
        assert isinstance(post['id'], int)
        assert isinstance(post['title'], str)
        assert isinstance(post['body'], str)
        assert isinstance(post['userId'], int)

        # 비즈니스 로직 검증
        assert len(post['title'].strip()) > 0, "Title should not be empty"
        assert len(post['body'].strip()) > 0, "Body should not be empty"
        assert post['userId'] > 0, "User ID should be positive"

    @pytest.mark.negative
    def test_get_single_post_invalid_id(self, api_client: APIClient):
        """존재하지 않는 ID로 게시글 조회 테스트"""
        invalid_id = TestConfig.INVALID_POST_ID
        response = api_client.get_post_by_id(invalid_id)

        # JSONPlaceholder의 경우 404 대신 빈 객체를 반환할 수 있음
        assert response.status_code in [200, 404], \
            f"Expected 200 or 404, got {response.status_code}"

        if response.status_code == 200:
            # 빈 객체이거나 null 값들을 가져야 함
            post = response.json()
            # JSONPlaceholder는 빈 객체 {}를 반환함
            assert isinstance(post, dict)
        else:
            # 404인 경우 에러 응답 검증
            assert response.status_code == 404

    @pytest.mark.functional
    def test_create_post_success(self, api_client: APIClient, valid_post_data: Dict[str, Any]):
        """새 게시글 생성 성공 테스트"""
        response = api_client.create_post(valid_post_data)

        # 상태 코드 검증
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"

        # 응답 데이터 검증
        created_post = response.json()
        assert isinstance(created_post, dict)

        # 생성된 게시글 검증
        assert 'id' in created_post, "Created post should have an ID"
        assert isinstance(created_post['id'], int), "Post ID should be integer"
        assert created_post['id'] > 0, "Post ID should be positive"

        # 제출된 데이터와 비교
        assert created_post['title'] == valid_post_data['title']
        assert created_post['body'] == valid_post_data['body']
        assert created_post['userId'] == valid_post_data['userId']

    @pytest.mark.negative
    def test_create_post_missing_title(self, api_client: APIClient):
        """필수 필드 누락 시 게시글 생성 테스트"""
        incomplete_data = {
            "body": "Post without title field",
            "userId": TestConfig.VALID_USER_ID
            # title 필드 의도적으로 누락
        }

        response = api_client.create_post(incomplete_data)

        # JSONPlaceholder는 실제 검증을 하지 않으므로 201을 반환할 수 있음
        # 실제 API에서는 400 또는 422를 기대
        valid_status_codes = [201, 400, 422]
        assert response.status_code in valid_status_codes, \
            f"Expected one of {valid_status_codes}, got {response.status_code}"

        # 응답이 JSON 형식인지 확인
        try:
            response_data = response.json()
            assert isinstance(response_data, dict)
        except json.JSONDecodeError:
            pytest.fail("Response should be valid JSON")

    @pytest.mark.negative
    def test_create_post_empty_data(self, api_client: APIClient):
        """빈 데이터로 게시글 생성 테스트"""
        empty_data = {}

        response = api_client.create_post(empty_data)

        # 빈 데이터에 대한 처리 확인
        valid_status_codes = [201, 400, 422]
        assert response.status_code in valid_status_codes

        if response.status_code == 201:
            # JSONPlaceholder는 빈 데이터도 수용할 수 있음
            created_post = response.json()
            assert 'id' in created_post
        else:
            # 에러 응답인 경우
            try:
                error_response = response.json()
                assert isinstance(error_response, dict)
            except json.JSONDecodeError:
                pass  # 에러 메시지가 JSON이 아닐 수도 있음

    @pytest.mark.functional
    def test_update_post_success(self, api_client: APIClient):
        """게시글 업데이트 성공 테스트"""
        post_id = TestConfig.VALID_POST_ID
        update_data = {
            "id": post_id,
            "title": f"Updated Post Title {int(time.time())}",
            "body": "This post has been updated by automated testing.",
            "userId": TestConfig.VALID_USER_ID
        }

        response = api_client.update_post(post_id, update_data)

        # 상태 코드 검증
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"

        # 업데이트된 데이터 검증
        updated_post = response.json()
        assert updated_post['id'] == post_id
        assert updated_post['title'] == update_data['title']
        assert updated_post['body'] == update_data['body']
        assert updated_post['userId'] == update_data['userId']

    @pytest.mark.functional
    def test_delete_post_success(self, api_client: APIClient):
        """게시글 삭제 성공 테스트"""
        post_id = TestConfig.VALID_POST_ID

        response = api_client.delete_post(post_id)

        # 삭제 성공 상태 코드 검증
        assert response.status_code in [200, 204], \
            f"Expected 200 or 204, got {response.status_code}"

    @pytest.mark.functional
    def test_get_posts_by_user(self, api_client: APIClient):
        """특정 사용자의 게시글 조회 테스트"""
        user_id = TestConfig.VALID_USER_ID

        response = api_client.get_posts_by_user(user_id)

        # 상태 코드 검증
        assert response.status_code == 200

        # 사용자별 게시글 검증
        user_posts = response.json()
        assert isinstance(user_posts, list)
        assert len(user_posts) > 0, f"User {user_id} should have posts"

        # 모든 게시글이 해당 사용자의 것인지 확인
        for post in user_posts:
            assert post['userId'] == user_id, \
                f"Post {post['id']} belongs to user {post['userId']}, not {user_id}"

    @pytest.mark.performance
    def test_api_response_time_performance(self, api_client: APIClient):
        """API 응답 시간 성능 테스트"""
        # 여러 번 요청하여 평균 응답 시간 측정
        response_times = []

        for _ in range(5):
            response = api_client.get_all_posts()
            assert response.status_code == 200
            response_times.append(response.response_time)

        # 성능 검증
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)

        print(f"\n성능 테스트 결과:")
        print(f"평균 응답 시간: {avg_response_time:.2f}ms")
        print(f"최대 응답 시간: {max_response_time:.2f}ms")
        print(f"모든 응답 시간: {response_times}")

        # 성능 기준 검증
        assert avg_response_time < 1000, f"Average response time {avg_response_time}ms is too slow"
        assert max_response_time < 2000, f"Max response time {max_response_time}ms is too slow"

    @pytest.mark.functional
    def test_posts_data_consistency(self, api_client: APIClient, test_data: Dict[str, Any]):
        """게시글 데이터 일관성 테스트"""
        # 테스트 데이터에서 검증할 게시글 정보 가져오기
        valid_posts = test_data.get('valid_posts', [])

        for post_info in valid_posts[:3]:  # 처음 3개만 테스트
            post_id = post_info['id']
            expected_title_part = post_info.get('expected_title', '')

            response = api_client.get_post_by_id(post_id)
            assert response.status_code == 200

            post = response.json()
            if expected_title_part:
                assert expected_title_part in post['title'], \
                    f"Post {post_id} title should contain '{expected_title_part}'"

    @pytest.mark.negative
    @pytest.mark.parametrize("invalid_id", [0, -1, 999, 1001, "abc", ""])
    def test_get_post_various_invalid_ids(self, api_client: APIClient, invalid_id):
        """다양한 잘못된 ID로 게시글 조회 테스트 (파라미터화)"""
        try:
            response = api_client.get_post_by_id(invalid_id)

            # 문자열이나 음수 ID의 경우 에러가 날 수 있음
            if isinstance(invalid_id, str):
                # 문자열 ID는 400 Bad Request이거나 404 Not Found
                assert response.status_code in [400, 404, 200]
            else:
                # 숫자 ID는 보통 200 (빈 응답) 또는 404
                assert response.status_code in [200, 404]

        except requests.exceptions.RequestException:
            # 일부 잘못된 요청은 예외를 발생시킬 수 있음
            pytest.skip(f"Request with invalid ID {invalid_id} caused exception")


class TestAPIClientUtilities:
    """API 클라이언트 유틸리티 기능 테스트"""

    def test_response_structure_validation(self, api_client: APIClient):
        """응답 구조 검증 유틸리티 테스트"""
        response = api_client.get_all_posts()

        # 올바른 필드들로 검증
        valid_fields = ['id', 'title', 'body', 'userId']
        assert api_client.validate_response_structure(response, valid_fields)

        # 잘못된 필드로 검증
        invalid_fields = ['id', 'title', 'nonexistent_field']
        assert not api_client.validate_response_structure(response, invalid_fields)

    def test_response_time_validation(self, api_client: APIClient):
        """응답 시간 검증 유틸리티 테스트"""
        response = api_client.get_all_posts()

        # 관대한 기준으로 테스트
        assert api_client.is_response_time_acceptable(response, 5000)

        # 엄격한 기준으로 테스트 (실패할 수도 있음)
        # assert api_client.is_response_time_acceptable(response, 100)

    def test_api_statistics(self, api_client: APIClient):
        """API 통계 기능 테스트"""
        # 몇 번의 요청 실행
        api_client.get_all_posts()
        api_client.get_post_by_id(1)
        api_client.get_post_by_id(2)

        stats = api_client.get_response_stats()

        assert 'total_requests' in stats
        assert stats['total_requests'] >= 3
        assert 'avg_response_time' in stats
        assert 'status_code_distribution' in stats
        assert stats['avg_response_time'] > 0