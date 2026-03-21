# Workflow Execution Plan: Project Setup

**Generated:** 2026-03-21
**Workflow:** project-setup
**Repository:** intel-agency/workflow-orchestration-queue-november57-a
**Project:** OS-APOW (workflow-orchestration-queue) - Autonomous AI Development Orchestrator

---

## 1. Overview

| Field | Value |
|-------|-------|
| **Workflow Name** | project-setup |
| **Workflow File** | `local_ai_instruction_modules/ai-workflow-assignments/dynamic-workflows/project-setup.md` |
| **Total Assignments** | 6 main + 3 event assignments |
| **Purpose** | Initialize the repository, create application plan, establish project structure, and document the project for future development |

### High-Level Summary

This workflow transforms a seeded repository containing plan documents into a fully-initialized development project. It creates the application plan from the existing specifications, establishes project scaffolding, sets up development tooling, and creates comprehensive documentation for AI coding agents.

---

## 2. Project Context Summary

### Project Overview

**workflow-orchestration-queue (OS-APOW)** is a headless agentic orchestration platform that transforms GitHub Issues into "Execution Orders" autonomously fulfilled by specialized AI agents. It eliminates the human-in-the-loop dependency of traditional AI coding tools.

### Four-Pillar Architecture

1. **The Ear (Work Event Notifier):** FastAPI webhook receiver for secure event ingestion
2. **The State (Work Queue):** GitHub Issues as state management ("Markdown as a Database")
3. **The Brain (Sentinel Orchestrator):** Background polling service managing worker lifecycles
4. **The Hands (Opencode Worker):** DevContainer-based AI worker execution layer

### Technology Stack

| Category | Technology |
|----------|------------|
| **Language** | Python 3.12+ |
| **Web Framework** | FastAPI + Uvicorn |
| **Validation** | Pydantic |
| **HTTP Client** | HTTPX (async) |
| **Package Manager** | uv (Rust-based) |
| **Containerization** | Docker + DevContainers |
| **Shell Scripts** | PowerShell Core (pwsh) / Bash |

### Key Architectural Decisions (ADRs)

- **ADR 07:** Shell-Bridge Execution via `./scripts/devcontainer-opencode.sh`
- **ADR 08:** Polling-First Resiliency (webhooks as optimization)
- **ADR 09:** Provider-Agnostic Interface Layer (`ITaskQueue` ABC)

### Development Phases

| Phase | Description |
|-------|-------------|
| **Phase 0** | Seeding & Bootstrapping (manual) |
| **Phase 1** | The Sentinel (MVP) - Polling & Shell-Bridge |
| **Phase 2** | The Ear - Webhook Automation |
| **Phase 3** | Deep Orchestration & Self-Healing |

### Known Risks (from Plan Review)

1. **Race conditions in task claiming** - Assign-then-verify pattern needed
2. **No heartbeat implementation** - Long-running tasks appear hung
3. **Model divergence between components** - Unified `src/models/work_item.py` needed
4. **No jittered exponential backoff** - Rate limiting vulnerability

### Repository Structure (Existing)

```
/
├── plan_docs/                    # Seeded planning documents
│   ├── OS-APOW Architecture Guide v3.2.md
│   ├── OS-APOW Development Plan v4.2.md
│   ├── OS-APOW Implementation Specification v1.2.md
│   ├── OS-APOW Plan Review.md
│   └── OS-APOW Simplification Report v1.md
├── src/                          # Reference implementations
│   ├── orchestrator_sentinel.py
│   └── notifier_service.py
├── scripts/                      # Shell bridge scripts
├── .devcontainer/                # DevContainer configs
├── .github/                      # Workflows and labels
└── local_ai_instruction_modules/ # Instruction modules
```

---

## 3. Assignment Execution Plan

### 3.1 Event: pre-script-begin

---

#### Assignment: `create-workflow-plan`
**Title:** Create Workflow Plan

| Field | Content |
|-------|---------|
| **Goal** | Create a comprehensive workflow execution plan documenting all assignments, their dependencies, and project-specific context |
| **Key Acceptance Criteria** | • Dynamic workflow fully read and all assignments traced<br>• All `plan_docs/` files read and summarized<br>• Workflow execution plan covers every assignment in order<br>• Plan presented to stakeholder and approved<br>• `plan_docs/workflow-plan.md` committed and pushed |
| **Project-Specific Notes** | This is the current assignment. The plan docs are comprehensive and contain reference implementations. Key focus areas: unified data model, assign-then-verify locking, heartbeat implementation. |
| **Prerequisites** | None (first assignment) |
| **Dependencies** | None |
| **Risks / Challenges** | None - this is a planning-only assignment |
| **Events** | None |

---

### 3.2 Main Script Assignments

---

#### Assignment: `init-existing-repository`
**Title:** Initiate Existing Repository

| Field | Content |
|-------|---------|
| **Goal** | Initialize the repository with proper settings, labels, and project structure |
| **Key Acceptance Criteria** | • PR and new branch created (must be first)<br>• GitHub Project created for issue tracking<br>• Project linked to repository<br>• Labels imported from `.github/.labels.json`<br>• Filenames changed to match project name |
| **Project-Specific Notes** | Repository already exists. Focus on: creating the `dynamic-workflow-project-setup` branch, importing labels, and renaming workspace files. The GitHub Project creation is a **manual step** per the assignment. |
| **Prerequisites** | GitHub authentication with `repo`, `project`, `read:project`, `read:user`, `user:email` scopes |
| **Dependencies** | None |
| **Risks / Challenges** | • GitHub Project creation requires manual execution after devcontainer image is built<br>• Must verify `gh auth status` before proceeding<br>• Run `./scripts/test-github-permissions.ps1` to verify permissions |
| **Events** | None |

---

#### Assignment: `create-app-plan`
**Title:** Create Application Plan

| Field | Content |
|-------|---------|
| **Goal** | Create a comprehensive application plan documented as a GitHub Issue using the template |
| **Key Acceptance Criteria** | • Application template analyzed<br>• Plan documented in issue using Appendix A template<br>• Milestones created and issues linked<br>• Issue added to GitHub Project<br>• `implementation:ready` label applied |
| **Project-Specific Notes** | Plan docs are extensive (Architecture Guide, Development Plan, Implementation Spec, Plan Review, Simplification Report). The plan should synthesize these into a single actionable issue with phases matching the Development Plan (Phase 0-3). Reference implementations exist in `src/` for guidance. |
| **Prerequisites** | GitHub Project created and linked |
| **Dependencies** | `init-existing-repository` (for project structure and labels) |
| **Risks / Challenges** | • Extensive documentation may lead to information overload<br>• Must balance comprehensive planning with actionable scope<br>• Plan Review identifies gaps that should be addressed in the plan |
| **Events** | `pre-assignment-begin` → `gather-context`<br>`on-assignment-failure` → `recover-from-error`<br>`post-assignment-complete` → `report-progress` |

---

#### Assignment: `create-project-structure`
**Title:** Create Project Structure

| Field | Content |
|-------|---------|
| **Goal** | Create actual project scaffolding: solution structure, Docker configs, CI/CD foundation, documentation |
| **Key Acceptance Criteria** | • Solution/project structure created<br>• Dockerfile and docker-compose.yml created<br>• CI/CD pipeline structure established<br>• Documentation structure created<br>• Repository summary document created |
| **Project-Specific Notes** | Python/uv stack. Key files needed: `pyproject.toml`, `uv.lock`, `Dockerfile`, `docker-compose.yml`. Follow the Implementation Spec's project structure. The Simplification Report recommends: 3 env vars only, single-repo polling, `stop` reset mode, stdout-only logging. |
| **Prerequisites** | Application plan approved and documented |
| **Dependencies** | `create-app-plan` (for tech stack and architecture decisions) |
| **Risks / Challenges** | • Must ensure `COPY src/ ./src/` before `uv pip install -e .` in Dockerfile<br>• Healthcheck must use Python stdlib (no curl in base image)<br>• Avoid over-engineering per Simplification Report |
| **Events** | None |

---

#### Assignment: `create-repository-summary`
**Title:** Create Repository Summary

| Field | Content |
|-------|---------|
| **Goal** | Create `.ai-repository-summary.md` at repository root with build/test commands and project context |
| **Key Acceptance Criteria** | • `.ai-repository-summary.md` exists at root<br>• Contains project overview<br>• Contains validated build/test commands<br>• Contains project layout description |
| **Project-Specific Notes** | Must validate all commands by running them. Document the shell bridge (`devcontainer-opencode.sh`), uv commands, and validation scripts. Target audience: AI coding agents working in this repository. |
| **Prerequisites** | Project structure created |
| **Dependencies** | `create-project-structure` (for commands to validate) |
| **Risks / Challenges** | • Commands must be validated by actual execution<br>• Must be concise (2 pages max) but comprehensive |
| **Events** | None |

---

#### Assignment: `create-agents-md-file`
**Title:** Create AGENTS.md File

| Field | Content |
|-------|---------|
| **Goal** | Create `AGENTS.md` at repository root following the open agents.md specification |
| **Key Acceptance Criteria** | • `AGENTS.md` exists at root<br>• Contains setup/build/test commands<br>• Contains project structure<br>• Contains code style conventions<br>• Commands validated by running |
| **Project-Specific Notes** | Complements README.md (human-focused) and `.ai-repository-summary.md`. Follow the [agents.md](https://agents.md/) format. Cross-reference with existing docs to avoid duplication. |
| **Prerequisites** | Project structure created, repository summary exists |
| **Dependencies** | `create-repository-summary` (for consistency) |
| **Risks / Challenges** | • Must not duplicate README.md content<br>• Commands must be validated<br>• Keep concise for agent consumption |
| **Events** | None |

---

#### Assignment: `debrief-and-document`
**Title:** Debrief and Document Learnings

| Field | Content |
|-------|---------|
| **Goal** | Create comprehensive debriefing report capturing learnings, issues, and recommendations |
| **Key Acceptance Criteria** | • Detailed report created using template<br>• All deviations documented<br>• Report reviewed and approved<br>• Execution trace saved at `debrief-and-document/trace.md` |
| **Project-Specific Notes** | Capture any issues with the extensive plan docs, Simplification Report recommendations, and Plan Review findings. Document what worked and what needs improvement for future workflow executions. |
| **Prerequisites** | All main assignments complete |
| **Dependencies** | All previous main assignments |
| **Risks / Challenges** | • Must capture all deviations from assignments<br>• Execution trace must be comprehensive |
| **Events** | None |

---

### 3.3 Event: post-assignment-complete

---

#### Assignment: `validate-assignment-completion`
**Title:** Validate Assignment Completion

| Field | Content |
|-------|---------|
| **Goal** | Validate that each completed assignment meets all acceptance criteria |
| **Key Acceptance Criteria** | • All required files exist<br>• All verification commands pass<br>• Validation report created<br>• Pass/fail status determined |
| **Project-Specific Notes** | Must delegate to independent `qa-test-engineer` agent. For Python projects: `uv sync`, `uv run pytest`, linting. For GitHub operations: query live state to verify issues/PRs exist. |
| **Prerequisites** | An assignment has just completed |
| **Dependencies** | Triggered after each main assignment |
| **Risks / Challenges** | • Must be executed by independent QA agent<br>• GitHub state must be verified via live queries |
| **Events** | None |

---

#### Assignment: `report-progress`
**Title:** Report Progress

| Field | Content |
|-------|---------|
| **Goal** | Generate progress reports after each workflow step completes |
| **Key Acceptance Criteria** | • Structured progress report generated<br>• Step outputs captured<br>• Workflow state checkpointed |
| **Project-Specific Notes** | Provides visibility into long-running workflow. Creates checkpoints for recovery from interruptions. |
| **Prerequisites** | Workflow step completed successfully |
| **Dependencies** | Triggered after each main assignment |
| **Risks / Challenges** | None significant |
| **Events** | None |

---

## 4. Sequencing Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    EVENT: pre-script-begin                          │
│  ┌─────────────────────┐                                            │
│  │ create-workflow-plan │  ◄── CURRENT ASSIGNMENT                   │
│  └─────────────────────┘                                            │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    MAIN SCRIPT ASSIGNMENTS                          │
│                                                                     │
│  ┌───────────────────────────┐                                      │
│  │ init-existing-repository   │ ──► Create branch, import labels   │
│  └───────────────────────────┘                                      │
│              │                                                      │
│              ▼                                                      │
│  ┌───────────────────────────┐                                      │
│  │ create-app-plan           │ ──► Analyze docs, create issue      │
│  └───────────────────────────┘                                      │
│              │                                                      │
│              ▼                                                      │
│  ┌───────────────────────────┐                                      │
│  │ create-project-structure  │ ──► Scaffold Python project         │
│  └───────────────────────────┘                                      │
│              │                                                      │
│              ▼                                                      │
│  ┌───────────────────────────┐                                      │
│  │ create-repository-summary │ ──► Create .ai-repository-summary.md│
│  └───────────────────────────┘                                      │
│              │                                                      │
│              ▼                                                      │
│  ┌───────────────────────────┐                                      │
│  │ create-agents-md-file     │ ──► Create AGENTS.md                │
│  └───────────────────────────┘                                      │
│              │                                                      │
│              ▼                                                      │
│  ┌───────────────────────────┐                                      │
│  │ debrief-and-document      │ ──► Create debrief report           │
│  └───────────────────────────┘                                      │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│              EVENT: post-assignment-complete                        │
│                                                                     │
│  (Runs after each main assignment)                                  │
│                                                                     │
│  ┌─────────────────────────────┐ │ ┌────────────────────┐           │
│  │ validate-assignment-completion│ │ │ report-progress    │           │
│  └─────────────────────────────┘ │ └────────────────────┘           │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 5. Open Questions

| # | Question | Context | Resolution Needed Before |
|---|----------|---------|--------------------------|
| 1 | **GitHub Project Creation** | The `init-existing-repository` assignment notes that GitHub Project creation cannot be done reliably during automated orchestration. Should this be deferred to manual execution, or should we attempt it programmatically? | `init-existing-repository` |
| 2 | **Scope for Phase 1** | The plan docs describe Phases 0-3, but should `create-app-plan` create issues for all phases or focus only on Phase 1 (The Sentinel MVP)? | `create-app-plan` |
| 3 | **Reference Implementation Handling** | Reference implementations exist in `src/` (orchestrator_sentinel.py, notifier_service.py). Should `create-project-structure` preserve these or rebuild from scratch following the plan? | `create-project-structure` |
| 4 | **Plan Review Gaps** | The Plan Review identifies several issues (race conditions, no heartbeat, no backoff, model divergence). Should the application plan explicitly address these as Phase 1 requirements? | `create-app-plan` |

---

## 6. Stakeholder Approval

**Approval Status:** ⏳ Pending Review

> **Does this workflow execution plan look correct? Are there any changes needed, or do you approve it?**

---

## 7. Commit Record

| Date | Commit | Message |
|------|--------|---------|
| 2026-03-21 | - | docs: add workflow execution plan for project-setup |

---

## Appendix A: Assignment Trace Log

| Assignment | Resolution Path | Summary |
|------------|-----------------|---------|
| project-setup (workflow) | Remote: `nam20485/agent-instructions` | Defines 6 main assignments + events |
| create-workflow-plan | Remote: `nam20485/agent-instructions` | Creates workflow execution plan |
| init-existing-repository | Remote: `nam20485/agent-instructions` | Initializes repo with labels and project |
| create-app-plan | Remote: `nam20485/agent-instructions` | Creates application plan as GitHub Issue |
| create-project-structure | Remote: `nam20485/agent-instructions` | Scaffolds project structure |
| create-repository-summary | Remote: `nam20485/agent-instructions` | Creates .ai-repository-summary.md |
| create-agents-md-file | Remote: `nam20485/agent-instructions` | Creates AGENTS.md |
| debrief-and-document | Remote: `nam20485/agent-instructions` | Creates debrief report |
| validate-assignment-completion | Remote: `nam20485/agent-instructions` | Validates assignment completion |
| report-progress | Remote: `nam20485/agent-instructions` | Reports progress after each step |

---

## Appendix B: Plan Documents Summary

| Document | Key Content |
|----------|-------------|
| **Architecture Guide v3.2** | 4-pillar architecture, ADRs 07-09, data flow, security model, self-bootstrapping lifecycle |
| **Development Plan v4.2** | Phase 0-3 roadmap, user stories, implementation directions, risk assessment, cross-cutting concerns |
| **Implementation Specification v1.2** | Features, test cases, logging, containerization, project structure, deliverables |
| **Plan Review** | Strengths (S-1 to S-7), Issues (I-1 to I-10), Recommendations (R-1 to R-9) |
| **Simplification Report v1** | YAGNI items, consolidation opportunities, implemented simplifications |
