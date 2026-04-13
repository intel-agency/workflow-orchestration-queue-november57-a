"""Tests for the main FastAPI application.

This module tests the FastAPI app creation, endpoints, and lifecycle.
"""

from fastapi.testclient import TestClient

from os_apow.main import app, create_app


class TestAppCreation:
    """Tests for application creation and configuration."""

    def test_create_app_returns_fastapi_instance(self) -> None:
        """Test that create_app returns a FastAPI instance."""
        from fastapi import FastAPI

        test_app = create_app()
        assert isinstance(test_app, FastAPI)

    def test_app_has_correct_title(self) -> None:
        """Test that the app has the correct title."""
        assert app.title == "OS-APOW"

    def test_app_has_version(self) -> None:
        """Test that the app has a version."""
        assert app.version is not None
        assert len(app.version) > 0


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_check_returns_healthy(self) -> None:
        """Test that the health endpoint returns healthy status."""
        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

    def test_health_check_has_version(self) -> None:
        """Test that the health endpoint includes version."""
        client = TestClient(app)
        response = client.get("/health")

        data = response.json()
        assert data["version"] == "0.1.0"


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_returns_app_info(self) -> None:
        """Test that the root endpoint returns app information."""
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "OS-APOW"
        assert data["status"] == "running"
        assert "version" in data


class TestOpenAPI:
    """Tests for OpenAPI documentation."""

    def test_openapi_docs_available(self) -> None:
        """Test that OpenAPI docs are available."""
        client = TestClient(app)
        response = client.get("/docs")

        assert response.status_code == 200

    def test_openapi_json_available(self) -> None:
        """Test that OpenAPI JSON spec is available."""
        client = TestClient(app)
        response = client.get("/openapi.json")

        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
