"""Pytest configuration and shared fixtures.

This module provides common fixtures for testing the OS-APOW application.
"""

import os
from collections.abc import Generator
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

# Set test environment variables before importing app modules
os.environ.setdefault("GITHUB_TOKEN", "test-token-for-testing")
os.environ.setdefault("GITHUB_ORG", "test-org")
os.environ.setdefault("GITHUB_REPO", "test-repo")
os.environ.setdefault("WEBHOOK_SECRET", "test-secret")


@pytest.fixture
def mock_settings() -> MagicMock:
    """Create a mock Settings instance for testing.

    Returns:
        A MagicMock configured with test settings.
    """
    settings = MagicMock()
    settings.github_token = "test-token"
    settings.github_org = "test-org"
    settings.github_repo = "test-repo"
    settings.github_repository = "test-org/test-repo"
    settings.webhook_secret = "test-secret"
    settings.redis_url = "redis://localhost:6379/0"
    settings.app_name = "OS-APOW"
    settings.app_version = "0.1.0"
    settings.debug = True
    settings.log_level = "DEBUG"
    settings.polling_interval_seconds = 60
    settings.heartbeat_interval_seconds = 300
    settings.task_timeout_seconds = 5700
    settings.stale_task_threshold_seconds = 900
    settings.worker_cpu_limit = 2.0
    settings.worker_memory_limit_mb = 4096
    return settings


@pytest.fixture
def mock_redis() -> AsyncMock:
    """Create a mock Redis client for testing.

    Returns:
        An AsyncMock configured for Redis operations.
    """
    redis = AsyncMock()
    redis.get = AsyncMock(return_value=None)
    redis.set = AsyncMock(return_value=True)
    redis.delete = AsyncMock(return_value=1)
    redis.exists = AsyncMock(return_value=0)
    return redis


@pytest.fixture
def sample_issue_payload() -> dict[str, Any]:
    """Create a sample GitHub issue event payload for testing.

    Returns:
        A dictionary containing a sample issue event payload.
    """
    return {
        "action": "opened",
        "issue": {
            "number": 42,
            "title": "Implement user authentication",
            "body": "Add OAuth2 login flow with proper token handling.",
            "labels": [
                {"name": "enhancement"},
                {"name": "auth"},
            ],
            "assignees": [],
            "created_at": "2026-03-21T10:00:00Z",
            "updated_at": "2026-03-21T10:00:00Z",
        },
        "repository": {
            "id": 123456,
            "name": "test-repo",
            "full_name": "test-org/test-repo",
            "owner": {
                "login": "test-org",
            },
        },
        "sender": {
            "login": "test-user",
            "type": "User",
        },
    }


@pytest.fixture
def sample_work_item_data() -> dict[str, Any]:
    """Create sample work item data for testing.

    Returns:
        A dictionary containing sample work item data.
    """
    return {
        "issue_number": 42,
        "title": "Implement user authentication",
        "body": "Add OAuth2 login flow with proper token handling.",
        "status": "agent:queued",
        "labels": ["enhancement", "auth"],
        "assignees": [],
        "sentinel_id": "sentinel-test-123",
        "created_at": "2026-03-21T10:00:00Z",
        "updated_at": "2026-03-21T10:00:00Z",
    }


@pytest.fixture
def mock_httpx_client() -> AsyncMock:
    """Create a mock HTTPX client for testing.

    Returns:
        An AsyncMock configured for HTTP operations.
    """
    client = AsyncMock()

    # Mock response for GitHub API calls
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json = MagicMock(return_value={})

    client.get = AsyncMock(return_value=mock_response)
    client.post = AsyncMock(return_value=mock_response)
    client.patch = AsyncMock(return_value=mock_response)
    client.delete = AsyncMock(return_value=mock_response)

    return client


@pytest.fixture(autouse=True)
def reset_settings_cache() -> Generator[None, None, None]:
    """Reset the settings cache before and after each test.

    This ensures test isolation when using the cached get_settings function.
    """
    from os_apow.config import get_settings

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
