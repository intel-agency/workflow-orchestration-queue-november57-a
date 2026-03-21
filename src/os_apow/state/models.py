"""Pydantic models for state management.

This module defines the data models for the work queue and state transitions.
"""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class TaskStatus(StrEnum):
    """Task status labels for the state machine.

    These correspond to GitHub labels with the 'agent:' prefix.
    """

    QUEUED = "agent:queued"
    IN_PROGRESS = "agent:in-progress"
    RECONCILING = "agent:reconciling"
    SUCCESS = "agent:success"
    ERROR = "agent:error"
    INFRA_FAILURE = "agent:infra-failure"
    STALLED_BUDGET = "agent:stalled-budget"

    @classmethod
    def terminal_states(cls) -> frozenset["TaskStatus"]:
        """Return the set of terminal states that indicate task completion."""
        return frozenset(
            {
                cls.SUCCESS,
                cls.ERROR,
                cls.INFRA_FAILURE,
                cls.STALLED_BUDGET,
            }
        )

    @classmethod
    def active_states(cls) -> frozenset["TaskStatus"]:
        """Return the set of active states that indicate task is being processed."""
        return frozenset(
            {
                cls.QUEUED,
                cls.IN_PROGRESS,
                cls.RECONCILING,
            }
        )


class WorkItem(BaseModel):
    """Unified data model for work items in the queue.

    This model represents a task derived from a GitHub Issue,
    following the "Markdown as a Database" philosophy.
    """

    issue_number: int = Field(..., description="GitHub issue number", ge=1)
    title: str = Field(..., description="Task title from issue", min_length=1)
    body: str | None = Field(default=None, description="Task description from issue body")
    status: TaskStatus = Field(
        default=TaskStatus.QUEUED,
        description="Current task status",
    )
    labels: list[str] = Field(
        default_factory=list,
        description="GitHub labels on the issue",
    )
    assignees: list[str] = Field(
        default_factory=list,
        description="GitHub usernames assigned to the issue",
    )
    sentinel_id: str | None = Field(
        default=None,
        description="Unique identifier for tracing across logs",
    )
    created_at: str | None = Field(
        default=None,
        description="ISO 8601 timestamp of issue creation",
    )
    updated_at: str | None = Field(
        default=None,
        description="ISO 8601 timestamp of last update",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata extracted from issue body",
    )

    model_config = {
        "use_enum_values": True,
        "json_schema_extra": {
            "examples": [
                {
                    "issue_number": 42,
                    "title": "Implement user authentication",
                    "body": "Add OAuth2 login flow...",
                    "status": "agent:queued",
                    "labels": ["enhancement", "auth"],
                    "assignees": ["bot-account"],
                    "sentinel_id": "sentinel-abc123",
                },
            ],
        },
    }


class WorkItemCreate(BaseModel):
    """Model for creating a new work item.

    Used when ingesting a new issue from the webhook.
    """

    issue_number: int = Field(..., description="GitHub issue number", ge=1)
    title: str = Field(..., description="Task title from issue", min_length=1)
    body: str | None = Field(default=None, description="Task description from issue body")
    labels: list[str] = Field(
        default_factory=list,
        description="GitHub labels on the issue",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata extracted from issue body",
    )

    def to_work_item(self) -> WorkItem:
        """Convert to a WorkItem instance with default status."""
        return WorkItem(
            issue_number=self.issue_number,
            title=self.title,
            body=self.body,
            labels=self.labels,
            metadata=self.metadata,
        )


class GitHubEvent(BaseModel):
    """Model for GitHub webhook event payload.

    Captures relevant fields from GitHub webhook events.
    """

    action: str = Field(..., description="Event action type")
    issue: dict[str, Any] | None = Field(default=None, description="Issue payload")
    repository: dict[str, Any] = Field(..., description="Repository payload")
    sender: dict[str, Any] = Field(..., description="User who triggered the event")

    @property
    def issue_number(self) -> int | None:
        """Extract issue number from payload if present."""
        if self.issue and "number" in self.issue:
            return int(self.issue["number"])
        return None

    @property
    def repository_name(self) -> str:
        """Extract repository full name."""
        name = self.repository.get("full_name")
        return str(name) if name is not None else ""

    @property
    def sender_login(self) -> str:
        """Extract sender login."""
        login = self.sender.get("login")
        return str(login) if login is not None else ""
