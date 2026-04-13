"""FastAPI application entry point for OS-APOW.

This module provides the main FastAPI application instance and lifecycle management.
"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from os_apow.config import get_settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan context manager.

    Handles startup and shutdown events for the FastAPI application.
    """
    settings = get_settings()

    # Startup
    logger.info(
        "Starting %s v%s",
        settings.app_name,
        settings.app_version,
    )
    logger.info("GitHub repository: %s", settings.github_repository)
    logger.info("Log level: %s", settings.log_level)

    yield

    # Shutdown
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Autonomous AI Development Orchestrator - Headless Agentic Orchestration",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        debug=settings.debug,
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, str]:
        """Health check endpoint for monitoring and load balancers."""
        return {"status": "healthy", "version": settings.app_version}

    # Root endpoint
    @app.get("/", tags=["root"])
    async def root() -> dict[str, str]:
        """Root endpoint with basic application information."""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "status": "running",
        }

    return app


# Create the application instance
app = create_app()


def main() -> None:
    """Main entry point for running the application with Uvicorn."""
    import uvicorn

    settings = get_settings()

    uvicorn.run(
        "os_apow.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
