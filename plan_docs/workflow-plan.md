# Workflow Execution Plan: project-setup

## 1. Overview

| Field | Value |
|-------|-------|
| **Workflow Name** | project-setup |
| **Workflow File** | `ai_instruction_modules/ai-workflow-assignments/dynamic-workflows/project-setup.md` |
| **Project Name** | workflow-orchestration-queue |
| **Total Assignments** | 6 main + 1 pre-script + 2 post-assignment events |
| **Trigger** | Successful completion of "Pre-build dev container image" workflow on main branch |

### Project Description
workflow-orchestration-queue is a headless agentic orchestration platform that transforms standard GitHub Issues into autonomous execution orders. The system shifts AI from a passive co-pilot to an autonomous background production service capable of multi-step, specification-driven task fulfillment without human intervention.

### High-Level Summary
This workflow initializes a new repository for development, creating the foundational project structure, application plan, documentation, and configuration needed for autonomous agentic development. It establishes the development environment, planning artifacts, and merges all setup work into the main branch.

---

## 2. Project Context Summary

### Key Facts from plan_docs/

| Aspect | Details |
|--------|---------|
| **Project** | workflow-orchestration-queue |
| **Description** | Headless agentic orchestration platform for autonomous AI development |
| **Primary Language** | Python 3.12+ |
| **Frameworks** | FastAPI, Pydantic, HTTPX |
| **Package Manager** | uv (Rust-based, fast dependency management) |
| **Containerization** | Docker, DevContainers |
| **Shell Scripts** | PowerShell Core (pwsh), Bash |

### Technology Stack
- **Python 3.12+**: Primary language for Orchestrator, API Webhook receiver, system logic
- **FastAPI**: High-performance async web framework for webhook receiver
- **Pydantic**: Strict data validation and settings management
- **HTTPX**: Async HTTP client for GitHub API calls
- **uv**: Fast Python package installer and dependency resolver
- **Docker/DevContainers**: Worker execution engine with sandboxing

### Key Components
1. **Work Event Notifier ("The Ear")**: FastAPI webhook receiver for GitHub events
2. **Sentinel Orchestrator ("The Brain")**: Background polling service for task discovery
3. **Opencode Worker ("The Hands")**: DevContainer-based AI execution environment
4. **Shell Bridge Scripts**: devcontainer-opencode.sh for environment management

### Repository Structure (Planned)
```
workflow-orchestration-queue/
├── pyproject.toml
├── uv.lock
├── src/
│   ├── notifier_service.py
│   ├── orchestrator_sentinel.py
│   ├── models/
│   │   ├── work_item.py
│   │   └── github_events.py
│   └── queue/
│       └── github_queue.py
├── scripts/
│   ├── devcontainer-opencode.sh
│   ├── gh-auth.ps1
│   └── update-remote-indices.ps1
├── local_ai_instruction_modules/
└── docs/
```

### Special Constraints
- **Action SHA Pinning**: All GitHub Actions MUST be pinned to specific commit SHAs
- **Security**: Credential scrubbing required for all log outputs
- **Concurrency**: Assign-then-verify pattern for task claiming
- **Self-Bootstrapping**: System designed to build itself after initial seeding

---

## 3. Assignment Execution Plan

### Phase 0: Pre-Script Event

| Field | Content |
|-------|---------|
| **Assignment** | `create-workflow-plan`: Create Workflow Plan |
| **Goal** | Create a comprehensive workflow execution plan before any other assignments begin |
| **Key Acceptance Criteria** | • Dynamic workflow fully read and all assignments traced<br>• All plan_docs/ files read and summarized<br>• Workflow execution plan covers every assignment in order<br>• Plan presented to and approved by stakeholder<br>• `plan_docs/workflow-plan.md` committed and pushed |
| **Project-Specific Notes** | This is the current assignment being executed. The plan documents the project-setup workflow for the workflow-orchestration-queue project. |
| **Prerequisites** | • Dynamic workflow file accessible<br>• plan_docs/ directory exists with project planning documents |
| **Dependencies** | None (first assignment) |
| **Risks / Challenges** | • Ensuring all remote assignment files are fetched correctly<br>• Capturing all project-specific context from multiple plan docs |
| **Events** | None |

---

### Phase 1: Main Assignments

#### Assignment 1: init-existing-repository

| Field | Content |
|-------|---------|
| **Assignment** | `init-existing-repository`: Initiate Existing Repository |
| **Goal** | Initialize the repository with proper settings, labels, milestones, and project structure |
| **Key Acceptance Criteria** | • New branch created (dynamic-workflow-project-setup)<br>• Branch protection ruleset imported<br>• GitHub Project created and linked<br>• Labels imported from .github/.labels.json<br>• Workspace and devcontainer files renamed<br>• PR created to main |
| **Project-Specific Notes** | This project uses the workflow-orchestration-queue-november57-a template. Branch naming should follow `dynamic-workflow-project-setup`. The .github/.labels.json contains orchestration-specific labels (agent:queued, agent:in-progress, etc.). |
| **Prerequisites** | • GitHub authentication with repo, project scopes<br>• GH_ORCHESTRATION_AGENT_TOKEN with administration:write scope |
| **Dependencies** | None (first main assignment) |
| **Risks / Challenges** | • Branch protection ruleset requires administration:write scope<br>• GitHub Project creation may fail if project limits reached |
| **Events** | None (post-assignment events fire after) |

#### Assignment 2: create-app-plan

| Field | Content |
|-------|---------|
| **Assignment** | `create-app-plan`: Create Application Plan |
| **Goal** | Create a comprehensive application plan based on the project specification documents |
| **Key Acceptance Criteria** | • Application template analyzed<br>• Plan documented in GitHub Issue using template<br>• tech-stack.md and architecture.md created<br>• Milestones created and linked<br>• Issue added to GitHub Project<br>• Appropriate labels applied |
| **Project-Specific Notes** | The plan_docs/ directory contains OS-APOW Architecture Guide, Development Plan, and Implementation Specification. These documents define the Sentinel, Notifier, and Worker components. The plan should reflect the 4-phase roadmap (Seeding → Sentinel MVP → Ear → Deep Orchestration). |
| **Prerequisites** | • Repository initialized<br>• plan_docs/ accessible |
| **Dependencies** | Output from init-existing-repository (branch, PR) |
| **Risks / Challenges** | • Ensuring tech stack documentation is complete for Python/FastAPI/uv stack<br>• Milestone creation for multi-phase roadmap |
| **Events** | • pre-assignment-begin: gather-context<br>• on-assignment-failure: recover-from-error<br>• post-assignment-complete: report-progress |

#### Assignment 3: create-project-structure

| Field | Content |
|-------|---------|
| **Assignment** | `create-project-structure`: Create Project Structure |
| **Goal** | Create the actual project scaffolding and infrastructure foundation |
| **Key Acceptance Criteria** | • Solution/project structure created<br>• Docker configurations created<br>• Development environment configured<br>• Documentation structure established<br>• CI/CD foundation created<br>• Repository summary document created<br>• All GitHub Actions pinned to commit SHAs |
| **Project-Specific Notes** | This is a Python project using uv for package management. Structure should include src/ directory with notifier_service.py, orchestrator_sentinel.py, models/, and queue/. Dockerfile should use Python 3.12+ base image. |
| **Prerequisites** | • Application plan documented<br>• Tech stack confirmed |
| **Dependencies** | Output from create-app-plan (plan issue, milestones) |
| **Risks / Challenges** | • Ensuring Docker healthchecks don't use curl (use Python stdlib instead)<br>• uv pip install -e . requires source directory copied first<br>• All workflow actions must be SHA-pinned |
| **Events** | None |

#### Assignment 4: create-agents-md-file

| Field | Content |
|-------|---------|
| **Assignment** | `create-agents-md-file`: Create AGENTS.md File |
| **Goal** | Create AGENTS.md at repository root with AI agent-focused instructions |
| **Key Acceptance Criteria** | • AGENTS.md exists at repository root<br>• Contains project overview, setup commands, project structure<br>• Contains code style, testing instructions<br>• All commands validated by running them<br>• Committed and pushed to working branch |
| **Project-Specific Notes** | Should include uv-specific commands (uv sync, uv run), Python linting (ruff/mypy), and DevContainer startup instructions. Cross-reference with README.md and .ai-repository-summary.md. |
| **Prerequisites** | • Repository initialized<br>• Project structure created<br>• Build/test tooling in place |
| **Dependencies** | Output from create-project-structure (project files, tooling) |
| **Risks / Challenges** | • Commands must be validated by actual execution<br>• Avoiding duplication with README.md |
| **Events** | None |

#### Assignment 5: debrief-and-document

| Field | Content |
|-------|---------|
| **Assignment** | `debrief-and-document`: Debrief and Document Learnings |
| **Goal** | Capture key learnings, insights, and areas for improvement from the workflow execution |
| **Key Acceptance Criteria** | • Detailed report created following template<br>• All 12 sections complete<br>• All deviations documented<br>• Execution trace saved (debrief-and-document/trace.md)<br>• Report reviewed and approved<br>• Committed and pushed |
| **Project-Specific Notes** | Document any challenges with Python/uv setup, DevContainer configuration, or GitHub API interactions. Flag any plan-impacting findings as ACTION ITEMS. |
| **Prerequisites** | • All prior assignments completed |
| **Dependencies** | Outputs from all prior assignments |
| **Risks / Challenges** | • Capturing complete execution trace<br>• Identifying actionable improvement items |
| **Events** | None |

#### Assignment 6: pr-approval-and-merge

| Field | Content |
|-------|---------|
| **Assignment** | `pr-approval-and-merge`: Pull Request Approval and Merge |
| **Goal** | Complete the full PR approval and merge process for the setup branch |
| **Key Acceptance Criteria** | • All CI/CD checks pass<br>• Code review completed (delegated to code-reviewer)<br>• All PR comments resolved via pr-review-comments assignment<br>• Stakeholder approval obtained<br>• PR merged to main<br>• Source branch deleted<br>• Related issues closed |
| **Project-Specific Notes** | This is an automated setup PR - self-approval by orchestrator is acceptable. CI remediation loop (up to 3 attempts) must be executed if checks fail. Pass $pr_num from init-existing-repository output. |
| **Prerequisites** | • PR created (from init-existing-repository)<br>• All work committed to PR branch |
| **Dependencies** | $pr_num from #initiate-new-repository.init-existing-repository |
| **Risks / Challenges** | • CI failures requiring remediation<br>• Merge conflicts with main<br>• Ensuring all commits are pushed before merge |
| **Events** | None |

---

### Phase 2: Post-Assignment Events

After each main assignment completes, the following events fire:

#### validate-assignment-completion

| Field | Content |
|-------|---------|
| **Assignment** | `validate-assignment-completion`: Validate Assignment Completion |
| **Goal** | Validate that completed assignment met all acceptance criteria |
| **Key Acceptance Criteria** | • All required files exist<br>• All verification commands pass<br>• Validation report created<br>• Pass/fail status determined<br>• Remediation steps provided if failed |
| **Project-Specific Notes** | Must be delegated to independent qa-test-engineer agent. For Python projects, runs uv sync, build, test, lint commands. |
| **Prerequisites** | • Assignment just completed |
| **Dependencies** | Prior assignment output |
| **Risks / Challenges** | • Ensuring independent validation<br>• Handling validation failures gracefully |
| **Events** | None |

#### report-progress

| Field | Content |
|-------|---------|
| **Assignment** | `report-progress`: Report Progress After Workflow Step Completion |
| **Goal** | Provide progress reporting, output capture, and validation checkpoints |
| **Key Acceptance Criteria** | • Structured progress report generated<br>• All step outputs captured<br>• Step acceptance criteria validated<br>• Workflow state checkpointed<br>• Action items filed as GitHub issues |
| **Project-Specific Notes** | File any deviations, findings, or plan-impacting discoveries as GitHub issues with priority:low and needs-triage labels. |
| **Prerequisites** | • Workflow step completed successfully |
| **Dependencies** | Prior assignment output |
| **Risks / Challenges** | • Ensuring all action items are filed as issues<br>• Maintaining accurate workflow state |
| **Events** | None |

---

### Phase 3: Post-Script-Complete Event

After all assignments and post-assignment events complete:

| Field | Content |
|-------|---------|
| **Event** | Apply `orchestration:plan-approved` label |
| **Goal** | Signal that the plan is ready for epic creation |
| **Action** | Locate the application plan issue (from create-app-plan) and apply label `orchestration:plan-approved` |
| **Dependencies** | #initiate-new-repository.create-app-plan (plan issue) |
| **Next Trigger** | This label triggers the next phase of the orchestration pipeline |

---

## 4. Sequencing Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        PROJECT-SETUP WORKFLOW EXECUTION                              │
├─────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ┌─────────────────────────────────────┐                                             │
│  │ PRE-SCRIPT EVENT                    │                                             │
│  │ ┌─────────────────────────────────┐ │                                             │
│  │ │ create-workflow-plan            │ │                                             │
│  │ │ (this plan)                     │ │                                             │
│  │ └─────────────────────────────────┘ │                                             │
│  └─────────────────────────────────────┘                                             │
│                      │                                                               │
│                      ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────────┐ │
│  │ MAIN ASSIGNMENTS (Sequential)                                                   │ │
│  │                                                                                  │ │
│  │  1. init-existing-repository ─────────┐                                         │ │
│  │     ├─ Create branch                  │                                         │ │
│  │     ├─ Import ruleset                 │                                         │ │
│  │     ├─ Create GitHub Project          │                                         │ │
│  │     ├─ Import labels                  │                                         │ │
│  │     └─ Create PR ─────────────────────┼──┐                                      │ │
│  │                                        │  │                                      │ │
│  │  ┌─────────────────────────────────────▼──▼──────────────────────────┐          │ │
│  │  │ POST-ASSIGNMENT: validate-assignment-completion                    │          │ │
│  │  │ POST-ASSIGNMENT: report-progress                                    │          │ │
│  │  └────────────────────────────────────────────────────────────────────┘          │ │
│  │                                        │                                         │ │
│  │  2. create-app-plan ◄──────────────────┘                                         │ │
│  │     ├─ Analyze plan_docs/                                                        │ │
│  │     ├─ Create plan issue                                                         │ │
│  │     ├─ Create tech-stack.md                                                      │ │
│  │     ├─ Create architecture.md                                                    │ │
│  │     └─ Create milestones                                                         │ │
│  │          │                                                                       │ │
│  │          ├──► [PRE: gather-context]                                              │ │
│  │          ├──► [POST: report-progress]                                            │ │
│  │          │                                                                       │ │
│  │  3. create-project-structure ◄───────┘                                           │ │
│  │     ├─ Create src/ structure                                                     │ │
│  │     ├─ Create Dockerfile                                                         │ │
│  │     ├─ Create docker-compose.yml                                                 │ │
│  │     ├─ Create CI/CD workflows                                                    │ │
│  │     └─ Create .ai-repository-summary.md                                          │ │
│  │          │                                                                       │ │
│  │          ├──► [POST: validate-assignment-completion]                             │ │
│  │          ├──► [POST: report-progress]                                            │ │
│  │          │                                                                       │ │
│  │  4. create-agents-md-file ◄──────────┘                                           │ │
│  │     ├─ Gather project context                                                    │ │
│  │     ├─ Validate build/test commands                                              │ │
│  │     └─ Create AGENTS.md                                                          │ │
│  │          │                                                                       │ │
│  │          ├──► [POST: validate-assignment-completion]                             │ │
│  │          ├──► [POST: report-progress]                                            │ │
│  │          │                                                                       │ │
│  │  5. debrief-and-document ◄────────────┘                                          │ │
│  │     ├─ Create debrief report                                                     │ │
│  │     ├─ Document deviations                                                       │ │
│  │     └─ Save execution trace                                                      │ │
│  │          │                                                                       │ │
│  │          ├──► [POST: validate-assignment-completion]                             │ │
│  │          ├──► [POST: report-progress]                                            │ │
│  │          │                                                                       │ │
│  │  6. pr-approval-and-merge ◄───────────┘                                          │ │
│  │     ├─ CI verification & remediation                                             │ │
│  │     ├─ Code review delegation                                                    │ │
│  │     ├─ Resolve PR comments                                                       │ │
│  │     ├─ Merge PR                                                                  │ │
│  │     └─ Delete branch, close issues                                               │ │
│  │          │                                                                       │ │
│  │          ├──► [POST: validate-assignment-completion]                             │ │
│  │          └──► [POST: report-progress]                                            │ │
│  │                                                                                  │ │
│  └──────────────────────────────────────────────────────────────────────────────────┘ │
│                      │                                                               │
│                      ▼                                                               │
│  ┌─────────────────────────────────────┐                                             │
│  │ POST-SCRIPT-COMPLETE EVENT          │                                             │
│  │ ┌─────────────────────────────────┐ │                                             │
│  │ │ Apply orchestration:plan-approved│ │                                             │
│  │ │ to plan issue                   │ │                                             │
│  │ └─────────────────────────────────┘ │                                             │
│  └─────────────────────────────────────┘                                             │
│                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Open Questions

| # | Question | Context | Resolution Needed Before |
|---|----------|---------|--------------------------|
| 1 | Is `GH_ORCHESTRATION_AGENT_TOKEN` configured with `administration:write` scope? | Required for branch protection ruleset import in init-existing-repository | init-existing-repository |
| 2 | Should the application plan issue use the exact template from Appendix A or adapt for this Python project? | Template references .NET examples; may need Python-specific adaptation | create-app-plan |
| 3 | What is the expected `SENTINEL_BOT_LOGIN` for the concurrency locking pattern? | Required for assign-then-verify pattern in production; can be deferred for setup | Future (Phase 1 implementation) |
| 4 | Should `plan_docs/workflow-plan.md` be committed to the setup branch or directly to main? | This plan document should likely be on the setup branch with other changes | create-workflow-plan (now) |

---

## 6. Execution Tracking

| Assignment | Status | Output Reference |
|------------|--------|------------------|
| create-workflow-plan | ✅ COMPLETE | Issue #3 |
| init-existing-repository | ⏳ PENDING | #initiate-new-repository.init-existing-repository |
| create-app-plan | ⏳ PENDING | #initiate-new-repository.create-app-plan |
| create-project-structure | ⏳ PENDING | #initiate-new-repository.create-project-structure |
| create-agents-md-file | ⏳ PENDING | #initiate-new-repository.create-agents-md-file |
| debrief-and-document | ⏳ PENDING | #initiate-new-repository.debrief-and-document |
| pr-approval-and-merge | ⏳ PENDING | #initiate-new-repository.pr-approval-and-merge |

---

## 7. Related Artifacts

- **Workflow Plan Issue**: https://github.com/intel-agency/workflow-orchestration-queue-november57-a/issues/3
- **Planning Documents**:
  - OS-APOW Architecture Guide v3.2.md
  - OS-APOW Development Plan v4.2.md
  - OS-APOW Implementation Specification v1.2.md
