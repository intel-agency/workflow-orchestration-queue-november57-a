# OS-APOW - Autonomous AI Development Orchestrator

[![CI](https://github.com/intel-agency/workflow-orchestration-queue-november57-a/actions/workflows/ci.yml/badge.svg)](https://github.com/intel-agency/workflow-orchestration-queue-november57-a/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://docs.astral.sh/ruff/)

**OS-APOW** (workflow-orchestration-queue) represents a paradigm shift from **Interactive AI Coding** to **Headless Agentic Orchestration**. It transforms GitHub Issues into "Execution Orders" autonomously fulfilled by specialized AI agents.

## Overview

Traditional AI developer tools require a human-in-the-loop to navigate files, provide context, and trigger executions. OS-APOW replaces this manual overhead with a persistent, event-driven infrastructure that:

- **Listens** for GitHub events via webhooks (The Ear)
- **Manages** state through GitHub Issues as a database (The State)
- **Orchestrates** task execution and worker lifecycles (The Brain)
- **Executes** code generation via isolated DevContainers (The Hands)

## Architecture

OS-APOW implements a **Four-Pillar Architecture**:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   THE EAR    │────▶│  THE STATE   │────▶│  THE BRAIN   │
│   (Notifier) │     │  (Work Queue)│     │  (Sentinel)  │
│   FastAPI    │     │ GitHub Issues│     │   Polling    │
└──────────────┘     └──────────────┘     └──────────────┘
                                                │
                                                ▼
                                       ┌──────────────┐
                                       │  THE HANDS   │
                                       │   (Worker)   │
                                       │  DevContainer│
                                       └──────────────┘
```

### Components

| Pillar | Technology | Role |
|--------|------------|------|
| **The Ear** | FastAPI, Pydantic, HMAC | Webhook receiver for GitHub events |
| **The State** | GitHub Issues, Labels | Persistence layer and state machine |
| **The Brain** | Python async, HTTPX | Sentinel orchestrator managing workers |
| **The Hands** | opencode CLI, DevContainer | Isolated execution environment |

## Quick Start

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- uv package manager
- GitHub Personal Access Token with `repo` scope

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/intel-agency/workflow-orchestration-queue-november57-a.git
   cd workflow-orchestration-queue-november57-a
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your GitHub credentials
   ```

4. **Run the application:**
   ```bash
   # Development mode with hot reload
   uv run uvicorn os_apow.main:app --reload

   # Or with Docker Compose
   docker compose up -d
   ```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/os_apow --cov-report=term-missing
```

### Code Quality

```bash
# Lint and format
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# Type checking
uv run mypy src/
```

## Project Structure

```
workflow-orchestration-queue/
├── src/
│   └── os_apow/
│       ├── __init__.py
│       ├── main.py              # FastAPI entry point
│       ├── config.py            # Pydantic settings
│       ├── ear/                 # Webhook receiver (The Ear)
│       │   ├── __init__.py
│       │   ├── routes.py        # FastAPI routes
│       │   └── hmac.py          # HMAC verification
│       ├── state/               # State management (The State)
│       │   ├── __init__.py
│       │   └── models.py        # Pydantic models
│       ├── brain/               # GitHub integration (The Brain)
│       │   └── __init__.py
│       └── hands/               # Execution layer (The Hands)
│           └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_main.py
├── docs/                        # Documentation
├── plan_docs/                   # Architecture and planning docs
├── pyproject.toml               # Project configuration
├── Dockerfile                   # Multi-stage Python build
├── docker-compose.yml           # Service orchestration
└── .env.example                 # Environment template
```

## Configuration

### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `GITHUB_TOKEN` | GitHub App installation token or PAT |
| `GITHUB_ORG` | GitHub organization name |
| `GITHUB_REPO` | Target repository name |

### Optional Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WEBHOOK_SECRET` | - | GitHub webhook secret for HMAC verification |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection URL |
| `LOG_LEVEL` | `INFO` | Logging level |
| `DEBUG` | `false` | Enable debug mode |
| `POLLING_INTERVAL_SECONDS` | `60` | Sentinel polling interval |
| `TASK_TIMEOUT_SECONDS` | `5700` | Maximum task execution time |

## Task State Machine

Tasks progress through defined states represented by GitHub labels:

```
[agent:queued] → [agent:in-progress] → [agent:success]
                        ↓
                 [agent:error]
                        ↓
               [agent:infra-failure]
```

| Label | Meaning |
|-------|---------|
| `agent:queued` | Task validated, awaiting Sentinel pickup |
| `agent:in-progress` | Sentinel has claimed and is executing |
| `agent:success` | Terminal success state |
| `agent:error` | Technical/execution failure |
| `agent:infra-failure` | Infrastructure failure (timeout, OOM) |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Root endpoint with app info |
| `/health` | GET | Health check for monitoring |
| `/docs` | GET | OpenAPI documentation |
| `/webhooks/github` | POST | GitHub webhook receiver |

## Security

- **HMAC Verification**: All webhooks verified with SHA-256 signatures
- **Network Isolation**: Worker containers run in isolated Docker networks
- **Ephemeral Credentials**: Secrets injected via environment, never persisted
- **Credential Scrubbing**: All public output filtered for sensitive data

## Development

### Adding New Features

1. Create a feature branch from `main`
2. Implement changes with tests
3. Run linting, type checking, and tests
4. Submit a pull request

### Docker Development

```bash
# Build and run with hot reload
docker compose --profile dev up app-dev

# Run production build
docker compose up app
```

## Documentation

- [Architecture Guide](plan_docs/architecture.md) - Detailed system architecture
- [Tech Stack](plan_docs/tech-stack.md) - Technology decisions and rationale
- [Development Plan](plan_docs/OS-APOW%20Development%20Plan%20v4.2.md) - Implementation roadmap

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

---

Built with ❤️ by Intel Agency
