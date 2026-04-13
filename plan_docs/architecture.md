# System Architecture: OS-APOW (workflow-orchestration-queue)

**Project:** OS-APOW - Autonomous AI Development Orchestrator  
**Repository:** intel-agency/workflow-orchestration-queue-november57-a  
**Last Updated:** 2026-03-21

---

## 1. Executive Summary

OS-APOW (workflow-orchestration-queue) represents a paradigm shift from **Interactive AI Coding** to **Headless Agentic Orchestration**. Traditional AI developer tools require a human-in-the-loop to navigate files, provide context, and trigger executions. OS-APOW replaces this manual overhead with a persistent, event-driven infrastructure that transforms GitHub Issues into "Execution Orders" autonomously fulfilled by specialized AI agents.

The system is **Self-Bootstrapping**: once initialized, it uses its own orchestration capabilities to refine and extend its components.

---

## 2. Four-Pillar Architecture

The system is strictly decoupled across four conceptual pillars, each handling a distinct domain:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              OS-APOW Architecture                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐             │
│    │   THE EAR    │────▶│  THE STATE   │────▶│  THE BRAIN   │             │
│    │   (Notifier) │     │  (Work Queue)│     │  (Sentinel)  │             │
│    │   FastAPI    │     │ GitHub Issues│     │   Polling    │             │
│    └──────────────┘     └──────────────┘     └──────────────┘             │
│           │                    │                    │                       │
│           │                    │                    │                       │
│           │                    │                    ▼                       │
│           │                    │           ┌──────────────┐               │
│           │                    │           │  THE HANDS   │               │
│           │                    │           │   (Worker)   │               │
│           │                    │           │  DevContainer│               │
│           │                    │           │   + LLM      │               │
│           │                    │           └──────────────┘               │
│           │                    │                    │                       │
│           ▼                    ▼                    ▼                       │
│    ┌──────────────────────────────────────────────────────────┐           │
│    │                    GitHub REST API                        │           │
│    │         (Issues, Labels, Comments, PRs)                   │           │
│    └──────────────────────────────────────────────────────────┘           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.1 The Ear (Work Event Notifier)

**Technology:** Python 3.12, FastAPI, Pydantic, HMAC verification

**Role:** The system's primary gateway for external stimuli and asynchronous triggers.

**Responsibilities:**
- **Secure Webhook Ingestion:** Exposes `/webhooks/github` endpoint for GitHub events
- **Cryptographic Verification:** Validates X-Hub-Signature-256 HMAC to prevent spoofing
- **Intelligent Event Triage:** Parses issue bodies/labels and maps to WorkItem objects
- **Queue Initialization:** Applies `agent:queued` label to trigger Sentinel processing

**Phase:** Phase 2 (after MVP Sentinel is operational)

---

### 2.2 The State (Work Queue)

**Technology:** GitHub Issues, Labels, Milestones

**Philosophy:** "Markdown as a Database" - GitHub Issues serve as the persistence layer, providing:
- World-class audit logs
- Transparent versioning of requirements
- Built-in UI for human supervision
- Real-time intervention via commenting

**State Machine (Label Logic):**

```
┌───────────────────────────────────────────────────────────────────────┐
│                        Task State Machine                              │
├───────────────────────────────────────────────────────────────────────┤
│                                                                        │
│   [User creates issue]                                                 │
│          │                                                             │
│          ▼                                                             │
│   ┌─────────────┐      ┌──────────────────┐      ┌─────────────┐     │
│   │ agent:      │      │ agent:           │      │ agent:      │     │
│   │ queued      │─────▶│ in-progress      │─────▶│ success     │     │
│   └─────────────┘      └──────────────────┘      └─────────────┘     │
│          │                     │                       ▲              │
│          │                     │                       │              │
│          │                     ▼                       │              │
│          │              ┌─────────────┐                │              │
│          │              │ agent:      │                │              │
│          │              │ error       │────────────────┘              │
│          │              └─────────────┘                │              │
│          │                     │                       │              │
│          │                     ▼                       │              │
│          │              ┌─────────────┐                │              │
│          │              │ agent:      │                │              │
│          │              │ infra-      │                │              │
│          │              │ failure     │────────────────┘              │
│          │              └─────────────┘                               │
│          │                                                            │
│          │    ┌─────────────┐                                         │
│          └───▶│ agent:      │ (stale task recovery)                  │
│               │ reconciling │                                         │
│               └─────────────┘                                         │
│                                                                        │
└───────────────────────────────────────────────────────────────────────┘
```

**Label Definitions:**

| Label | Meaning |
|-------|---------|
| `agent:queued` | Task validated, awaiting Sentinel pickup |
| `agent:in-progress` | Sentinel has claimed and is executing |
| `agent:reconciling` | Stale task being recovered (no updates for 15+ min) |
| `agent:success` | Terminal success state (PR created, tests passed) |
| `agent:error` | Technical/execution failure |
| `agent:infra-failure` | Infrastructure failure (timeout, OOM, container crash) |
| `agent:stalled-budget` | Budget/token limit exceeded |

---

### 2.3 The Brain (Sentinel Orchestrator)

**Technology:** Python async, HTTPX, Shell scripts

**Role:** Persistent supervisor managing worker lifecycles and mapping intent to execution.

**Lifecycle:**

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Sentinel Polling Loop                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────────┐                                                  │
│   │   START      │                                                  │
│   └──────┬───────┘                                                  │
│          │                                                           │
│          ▼                                                           │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────┐       │
│   │   POLL       │────▶│  FIND        │────▶│  CLAIM       │       │
│   │   (60s)      │     │  QUEUED      │     │  (assign-    │       │
│   │              │     │  TASKS       │     │  then-verify)│       │
│   └──────────────┘     └──────────────┘     └──────────────┘       │
│          │                                           │               │
│          │ 403/429                                   │               │
│          ▼                                           ▼               │
│   ┌──────────────┐                           ┌──────────────┐       │
│   │  BACKOFF     │                           │  PROCESS     │       │
│   │  (jittered   │                           │  TASK        │       │
│   │  exponential)│                           │              │       │
│   └──────────────┘                           └──────────────┘       │
│          │                                           │               │
│          │                                           ▼               │
│          │                                   ┌──────────────┐       │
│          │                                   │  UPDATE      │       │
│          │                                   │  STATUS      │       │
│          │                                   │  (success/   │       │
│          │                                   │   error)     │       │
│          │                                   └──────────────┘       │
│          │                                           │               │
│          └───────────────────────────────────────────┘               │
│                          (loop)                                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Key Features:**
- **Polling-First:** Resilient against server downtime; reconciles on restart
- **Jittered Exponential Backoff:** Handles rate limits (403/429) gracefully
- **Assign-then-Verify Locking:** Prevents race conditions between Sentinels
- **Heartbeat System:** Posts status every 5 minutes during long tasks
- **Graceful Shutdown:** SIGTERM/SIGINT handling prevents orphaned tasks

---

### 2.4 The Hands (Opencode Worker)

**Technology:** opencode CLI, DevContainer, LLM (GLM-5)

**Role:** Execution layer where actual coding happens.

**Environment:**
- Isolated Docker DevContainer
- Bit-for-bit identical to human developer environment
- Volume mounts for repository access
- Ephemeral credentials (never persisted)

**Execution Flow:**

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Worker Execution Flow                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   Sentinel triggers:  ./scripts/devcontainer-opencode.sh prompt     │
│                                                                      │
│   ┌──────────────┐                                                  │
│   │  DEVCONTAINER│  ◀── Isolated environment                        │
│   │  UP          │      (2 CPUs, 4GB RAM limit)                     │
│   └──────┬───────┘                                                  │
│          │                                                           │
│          ▼                                                           │
│   ┌──────────────┐                                                  │
│   │  OPENCODE    │  ◀── LLM Agent starts                            │
│   │  SERVER      │      Reads instruction modules                   │
│   │  START       │                                                  │
│   └──────┬───────┘                                                  │
│          │                                                           │
│          ▼                                                           │
│   ┌──────────────┐                                                  │
│   │  WORKFLOW    │  ◀── Execute markdown-based                      │
│   │  EXECUTION   │      instruction modules                         │
│   │              │      (create-app-plan.md, perform-task.md, etc.) │
│   └──────┬───────┘                                                  │
│          │                                                           │
│          ▼                                                           │
│   ┌──────────────┐                                                  │
│   │  VALIDATE    │  ◀── Run tests, lint, type checks                │
│   │  & COMMIT    │      Commit changes, create PR                   │
│   └──────────────┘                                                  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Flow (Happy Path)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           OS-APOW Data Flow                                   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  1. STIMULUS                                                                 │
│     User opens GitHub Issue using application-plan.md template               │
│     │                                                                         │
│     ▼                                                                         │
│  2. NOTIFICATION (Phase 2)                                                   │
│     GitHub Webhook → Notifier (FastAPI)                                      │
│     │   - Verify HMAC signature                                              │
│     │   - Parse issue body/labels                                            │
│     │   - Create WorkItem manifest                                           │
│     ▼                                                                         │
│  3. QUEUE INITIALIZATION                                                     │
│     Apply `agent:queued` label via GitHub API                                │
│     │                                                                         │
│     ▼                                                                         │
│  4. DISCOVERY (Sentinel Polling)                                             │
│     Sentinel detects queued issue (60s interval)                             │
│     │   - Assign-then-verify locking                                         │
│     │   - Update label to `agent:in-progress`                                │
│     ▼                                                                         │
│  5. ENVIRONMENT SYNC                                                         │
│     Sentinel runs git clone/pull to managed workspace                        │
│     │                                                                         │
│     ▼                                                                         │
│  6. EXECUTION                                                                │
│     Sentinel → devcontainer-opencode.sh up → start → prompt                  │
│     │   - Worker executes instruction module                                  │
│     │   - Heartbeat comments posted every 5 min                              │
│     ▼                                                                         │
│  7. FINALIZATION                                                             │
│     Worker creates PR, Sentinel detects exit code                            │
│     │   - Exit 0: Apply `agent:success`                                      │
│     │   - Exit non-0: Apply `agent:error` with logs                          │
│     ▼                                                                         │
│  8. CLEANUP                                                                  │
│     Sentinel stops worker container (prevents state bleed)                   │
│                                                                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Integration Points

### 4.1 GitHub REST API Integration

| Endpoint | Purpose |
|----------|---------|
| `GET /repos/{owner}/{repo}/issues` | Fetch queued tasks |
| `POST /repos/{owner}/{repo}/issues/{number}/labels` | Update task status |
| `POST /repos/{owner}/{repo}/issues/{number}/assignees` | Distributed locking |
| `POST /repos/{owner}/{repo}/issues/{number}/comments` | Progress updates, heartbeats |
| `POST /repos/{owner}/{repo}/pulls` | Create PRs (worker) |

### 4.2 Shell Bridge Interface

The Sentinel interacts with the worker exclusively via `./scripts/devcontainer-opencode.sh`:

| Command | Purpose | Timeout |
|---------|---------|---------|
| `up` | Provision Docker network and volumes | 300s |
| `start` | Launch opencode-server in container | 120s |
| `prompt "{instruction}"` | Execute agent workflow | 5700s (95 min) |
| `stop` | Stop container (preserve for fast restart) | 60s |

### 4.3 Instruction Modules

Markdown-based workflow logic in `/local_ai_instruction_modules/`:

| Module | Purpose |
|--------|---------|
| `create-app-plan.md` | Generate application implementation plan |
| `perform-task.md` | Standard feature implementation |
| `recover-from-error.md` | Bug fix and error recovery |

---

## 5. Security Architecture

### 5.1 Network Isolation

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Network Topology                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────┐        ┌─────────────────────────────────────┐   │
│   │   HOST      │        │        DOCKER NETWORK               │   │
│   │   (Sentinel)│        │   ┌───────────────────────────┐     │   │
│   │             │        │   │      WORKER               │     │   │
│   │  ✗ No access│───────▶│   │      CONTAINER            │     │   │
│   │    to worker│        │   │                           │     │   │
│   │             │        │   │  ✗ No host subnet access  │     │   │
│   └─────────────┘        │   │  ✗ No peer container access│    │   │
│                          │   │  ✓ Internet for packages  │     │   │
│                          │   └───────────────────────────┘     │   │
│                          └─────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 5.2 Credential Management

| Principle | Implementation |
|-----------|----------------|
| **Least Privilege** | Tokens scoped to specific repository operations |
| **Ephemeral** | Credentials injected via env vars, destroyed on container exit |
| **Never Persisted** | No secrets written to disk in worker container |
| **Scrubbed** | All public output filtered through `scrub_secrets()` |

### 5.3 Credential Scrubbing Patterns

The `scrub_secrets()` utility strips:
- GitHub PATs: `ghp_*`, `ghs_*`, `gho_*`, `github_pat_*`
- Bearer tokens
- API keys: `sk-*`
- ZhipuAI keys

---

## 6. Architectural Decision Records (ADRs)

### ADR 07: Standardized Shell-Bridge Execution

**Decision:** Sentinel interacts with worker exclusively via `./scripts/devcontainer-opencode.sh`.

**Rationale:** Existing shell scripts handle complex Docker logic (volume mounting, SSH-agent forwarding, port mapping). Reimplementing in Python would cause "Configuration Drift" between agent and developer environments.

**Consequence:** Python remains focused on logic/state; Shell handles "Heavy Lifting" of container orchestration.

---

### ADR 08: Polling-First Resiliency Model

**Decision:** Sentinel uses polling as primary discovery; webhooks are optimization.

**Rationale:** Webhooks are "Fire and Forget" — if server is down during event, it's lost. Polling ensures state reconciliation on every restart.

**Consequence:** System is inherently self-healing and resilient against downtime.

---

### ADR 09: Provider-Agnostic Interface Layer

**Decision:** All queue interactions abstracted behind `ITaskQueue` interface (Strategy Pattern).

**Rationale:** Enables future provider swapping (Linear, Jira, SQL queue) without rewriting orchestrator logic.

**Consequence:** `src/queue/github_queue.py` implements interface; both Sentinel and Notifier use same abstraction.

---

## 7. Self-Bootstrapping Lifecycle

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Self-Bootstrapping Stages                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Stage 0 (Seeding)                                                  │
│  ├─ Developer manually clones template repo                         │
│  └─ Adds plan documents to /docs                                    │
│                                                                      │
│  Stage 1 (Manual Launch)                                            │
│  └─ Developer runs devcontainer-opencode.sh up                      │
│                                                                      │
│  Stage 2 (Project Setup)                                            │
│  ├─ Developer runs project-setup workflow                           │
│  └─ Agent indexes repo, configures environment                      │
│                                                                      │
│  Stage 3 (Handover)                                                 │
│  ├─ Developer starts sentinel.py on host                            │
│  └─ From this point: HUMAN INTERACTS ONLY VIA GITHUB ISSUES        │
│                                                                      │
│  Stage 4 (Autonomous Evolution)                                     │
│  └─ System builds its own Phase 2 and Phase 3 features              │
│     by picking up its own task tickets                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 8. Component Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         OS-APOW Component Diagram                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌────────────────────────────────────────────────────────────────────┐    │
│   │                         GITHUB PLATFORM                             │    │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │    │
│   │  │   Issues     │  │   Labels     │  │  Webhooks    │             │    │
│   │  │   (State)    │  │  (Status)    │  │  (Events)    │             │    │
│   │  └──────────────┘  └──────────────┘  └──────────────┘             │    │
│   └────────────────────────────────────────────────────────────────────┘    │
│          │                   │                    ▲                          │
│          │ REST API          │ REST API           │ Webhook                 │
│          ▼                   ▼                    │                          │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                  │
│   │  SENTINEL   │     │   QUEUE     │     │  NOTIFIER   │                  │
│   │  (Brain)    │────▶│  GitHubQueue│◀────│   (Ear)     │                  │
│   │             │     │             │     │             │                  │
│   │ - Poll 60s  │     │ - ITaskQueue│     │ - FastAPI   │                  │
│   │ - Claim     │     │ - CRUD ops  │     │ - HMAC      │                  │
│   │ - Heartbeat │     │ - Locking   │     │ - Triage    │                  │
│   └─────────────┘     └─────────────┘     └─────────────┘                  │
│          │                                                                 │
│          │ Shell Bridge                                                    │
│          ▼                                                                 │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    WORKER CONTAINER (Hands)                          │  │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │  │
│   │  │  opencode    │  │  LLM Agent   │  │  Git/CLI     │              │  │
│   │  │  CLI         │  │  (GLM-5)     │  │  Tools       │              │  │
│   │  └──────────────┘  └──────────────┘  └──────────────┘              │  │
│   │                                                                      │  │
│   │  ┌──────────────────────────────────────────────────────────────┐   │  │
│   │  │         Instruction Modules (Markdown-based logic)            │   │  │
│   │  │  create-app-plan.md | perform-task.md | recover-from-error.md │   │  │
│   │  └──────────────────────────────────────────────────────────────┘   │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 9. Error Handling & Recovery

| Error Type | Detection | Recovery |
|------------|-----------|----------|
| **Rate Limit (403/429)** | HTTP status check | Jittered exponential backoff |
| **Race Condition** | Assign-then-verify failure | Skip task, try next |
| **Container Crash** | Non-zero exit from `up`/`start` | Label `agent:infra-failure`, post logs |
| **Agent Error** | Non-zero exit from `prompt` | Label `agent:error`, post sanitized stderr |
| **Timeout** | `asyncio.wait_for()` timeout | Kill process, label `agent:infra-failure` |
| **Stale Task** | No heartbeat for 15+ min | Move to `agent:reconciling`, reassign |

---

## References

- **Architecture Guide:** `plan_docs/OS-APOW Architecture Guide v3.2.md`
- **Development Plan:** `plan_docs/OS-APOW Development Plan v4.2.md`
- **Implementation Spec:** `plan_docs/OS-APOW Implementation Specification v1.2.md`
- **Plan Review:** `plan_docs/OS-APOW Plan Review.md`
- **Simplification Report:** `plan_docs/OS-APOW Simplification Report v1.md`
- **Tech Stack:** `plan_docs/tech-stack.md`
