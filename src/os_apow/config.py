"""Application configuration using Pydantic Settings.

This module provides centralized configuration management for OS-APOW,
following the Simplification Report's principle of minimal required environment variables.
"""

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    Required environment variables per Simplification Report S-3:
    - GITHUB_TOKEN: GitHub App installation token or PAT
    - GITHUB_ORG: GitHub organization name
    - GITHUB_REPO: Target repository name

    Optional variables:
    - SENTINEL_BOT_LOGIN: Bot account login for assign-then-verify locking
    - WEBHOOK_SECRET: GitHub App webhook secret for HMAC verification (Phase 2)
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Required GitHub configuration
    github_token: str = Field(..., description="GitHub App installation token or PAT")
    github_org: str = Field(..., description="GitHub organization name")
    github_repo: str = Field(..., description="Target repository name")

    # Optional configuration
    sentinel_bot_login: str | None = Field(
        default=None,
        description="Bot account login for assign-then-verify locking",
    )
    webhook_secret: str | None = Field(
        default=None,
        description="GitHub App webhook secret for HMAC verification",
    )

    # Redis configuration
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL",
    )

    # Application configuration
    app_name: str = Field(default="OS-APOW", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")

    # Sentinel configuration
    polling_interval_seconds: int = Field(
        default=60,
        description="Interval between polling cycles in seconds",
        ge=10,
        le=300,
    )
    heartbeat_interval_seconds: int = Field(
        default=300,
        description="Interval between heartbeat comments in seconds",
        ge=60,
        le=900,
    )
    task_timeout_seconds: int = Field(
        default=5700,  # 95 minutes
        description="Maximum task execution time in seconds",
        ge=300,
        le=14400,
    )
    stale_task_threshold_seconds: int = Field(
        default=900,  # 15 minutes
        description="Time threshold for marking tasks as stale",
        ge=300,
        le=3600,
    )

    # Worker configuration
    worker_cpu_limit: float = Field(
        default=2.0,
        description="CPU limit for worker containers",
    )
    worker_memory_limit_mb: int = Field(
        default=4096,
        description="Memory limit for worker containers in MB",
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is a valid Python logging level."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return v_upper

    @property
    def github_repository(self) -> str:
        """Return the full GitHub repository path (owner/repo)."""
        return f"{self.github_org}/{self.github_repo}"


@lru_cache
def get_settings() -> Settings:
    """Get cached application settings.

    This function returns a cached instance of Settings to avoid
    repeated environment variable parsing.

    Returns:
        Settings: The application settings instance.
    """
    return Settings()
