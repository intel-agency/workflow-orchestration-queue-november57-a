# Technology Stack: OS-APOW (workflow-orchestration-queue)

**Project:** OS-APOW - Autonomous AI Development Orchestrator  
**Repository:** intel-agency/workflow-orchestration-queue-november57-a  
**Last Updated:** 2026-03-21

---

## 1. Core Language & Runtime

| Technology | Version | Rationale |
|------------|---------|-----------|
| **Python** | 3.12+ | Primary language for orchestrator, API, and all system logic. Chosen for excellent async support, robust text processing, and extensive ecosystem for LLM integration. |
| **PowerShell Core (pwsh)** | 7.x | Used for shell bridge scripts and GitHub authentication helpers. Cross-platform compatibility with Windows and Linux. |
| **Bash** | 5.x | Used for DevContainer orchestration scripts (`devcontainer-opencode.sh`). Ubiquitous in containerized environments. |

---

## 2. Web Framework & API Layer

| Technology | Version | Rationale |
|------------|---------|-----------|
| **FastAPI** | 0.115+ | High-performance async web framework for the webhook receiver ("The Ear"). Native Pydantic integration, automatic OpenAPI documentation, and excellent async support. |
| **Uvicorn** | 0.34+ | Lightning-fast ASGI server for serving FastAPI applications in production. |
| **Pydantic** | 2.x | Strict data validation and settings management. Used extensively for WorkItem schemas, configuration validation, and API request/response models. |
| **HTTPX** | 0.28+ | Fully asynchronous HTTP client for GitHub REST API calls. Replaces `requests` to avoid blocking the event loop. Connection pooling for efficiency. |

---

## 3. Package Management

| Technology | Version | Rationale |
|------------|---------|-----------|
| **uv** | 0.10+ | Rust-based Python package manager. Orders of magnitude faster than pip/poetry. Manages dependencies via `pyproject.toml` and generates deterministic `uv.lock` files. |

**Why uv over pip/poetry:**
- 10-100x faster dependency resolution
- Built-in virtual environment management
- Deterministic lockfile for reproducible builds
- Native support for `pyproject.toml`

---

## 4. Containerization & Infrastructure

| Technology | Version | Rationale |
|------------|---------|-----------|
| **Docker** | 24+ | Core containerization platform. Provides isolation for worker environments and reproducible deployments. |
| **DevContainers** | - | VS Code DevContainer specification for consistent development and execution environments. The AI worker runs in a DevContainer identical to a human developer's setup. |
| **Docker Compose** | 2.x | Multi-container orchestration. Used by `devcontainer-opencode.sh` for complex scenarios (e.g., app + database). |

**Container Configuration:**
- **Resource Constraints:** 2 CPUs, 4GB RAM per worker (prevents rogue agent DoS)
- **Network Isolation:** Dedicated Docker network, no access to host subnet
- **Ephemeral Credentials:** Secrets injected via environment variables, never persisted to disk

---

## 5. LLM Integration

| Technology | Version | Rationale |
|------------|---------|-----------|
| **opencode CLI** | 1.2+ | AI agent runtime. Runs specialized agents defined in `.opencode/agents/` with MCP server support. |
| **GLM-5** | (zai-coding-plan) | Primary LLM model via ZhipuAI. Used for code generation, planning, and task execution. |
| **MCP Servers** | - | Model Context Protocol servers for sequential thinking and memory/knowledge graph. |

---

## 6. Version Control & CI/CD

| Technology | Version | Rationale |
|------------|---------|-----------|
| **Git** | 2.40+ | Version control system. |
| **GitHub** | - | Primary platform for issue tracking, PR management, and webhook events. |
| **GitHub Actions** | - | CI/CD for validation, testing, and deployment workflows. |
| **GitHub CLI (gh)** | 2.x | Command-line interface for GitHub API operations. |

---

## 7. Development Tools

| Tool | Purpose |
|------|---------|
| **Ruff** | Fast Python linter and formatter (replaces flake8, isort, black) |
| **MyPy** | Static type checking for Python |
| **pytest** | Testing framework with async support |
| **pytest-asyncio** | Async test support |

---

## 8. Logging & Observability

| Technology | Version | Rationale |
|------------|---------|-----------|
| **Python logging** | stdlib | Structured logging via StreamHandler (stdout). Captured by Docker container runtime. |
| **Docker logs** | - | Container runtime log collection. No separate file logging (per simplification S-10). |

**Logging Strategy:**
- Stdout-only (no file handlers)
- Each log line includes unique SENTINEL_ID for tracing
- Credential scrubbing before posting to GitHub comments

---

## 9. Security Tools

| Technology | Purpose |
|------|---------|
| **HMAC SHA256** | Webhook signature verification (prevents spoofing) |
| **regex** | Credential pattern matching for secret scrubbing |
| **Docker network isolation** | Prevents lateral movement from worker containers |

---

## 10. Environment Variables (Simplified)

Per Simplification Report S-3, only **3 required environment variables**:

| Variable | Required | Description |
|----------|----------|-------------|
| `GITHUB_TOKEN` | Yes | GitHub App installation token or PAT |
| `GITHUB_ORG` | Yes | GitHub organization name |
| `GITHUB_REPO` | Yes | Target repository name |
| `SENTINEL_BOT_LOGIN` | Optional | Bot account login for assign-then-verify locking |
| `WEBHOOK_SECRET` | Phase 2 | GitHub App webhook secret for HMAC verification |

---

## 11. Project Structure

```
workflow-orchestration-queue/
├── pyproject.toml           # uv dependencies and metadata
├── uv.lock                  # Deterministic lockfile
├── src/
│   ├── orchestrator_sentinel.py  # Sentinel (Brain)
│   ├── notifier_service.py       # Notifier (Ear) - Phase 2
│   ├── models/
│   │   └── work_item.py          # Unified data model
│   └── queue/
│       └── github_queue.py       # GitHub-backed queue (ITaskQueue)
├── scripts/
│   ├── devcontainer-opencode.sh  # Shell bridge to worker
│   ├── gh-auth.ps1               # GitHub auth helper
│   └── update-remote-indices.ps1 # Vector index sync
├── local_ai_instruction_modules/ # Markdown workflow logic
├── .devcontainer/                # DevContainer configs
└── docs/                         # Architecture & planning docs
```

---

## 12. Dependency Summary

```toml
# pyproject.toml dependencies
[project]
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.34.0",
    "pydantic>=2.0.0",
    "httpx>=0.28.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "ruff>=0.9.0",
    "mypy>=1.0.0",
]
```

---

## References

- **Architecture Guide:** `plan_docs/OS-APOW Architecture Guide v3.2.md`
- **Development Plan:** `plan_docs/OS-APOW Development Plan v4.2.md`
- **Implementation Spec:** `plan_docs/OS-APOW Implementation Specification v1.2.md`
- **Simplification Report:** `plan_docs/OS-APOW Simplification Report v1.md`
