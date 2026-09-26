# ActionShield --- Project Specification & Build Plan

> **TrueForge-powered self-validating autonomous engineering agent**
>
> **Memory suggests. Simulation verifies. Evidence decides.**

## 1. Mission

Build ActionShield as a production-quality hackathon prototype using
**TrueForge as the real agent runtime**.

The agent must demonstrate:

**REMEMBER → REASON → ACT → OBSERVE → CRITIQUE → ADAPT → RE-ACT → VERIFY
→ REMEMBER**

The agent must reach a real software repository, make a real change, run
the changed system in an isolated sandbox, observe actual evidence, have
specialized agents critique it, adapt when necessary, stop for human
approval before consequential execution, verify the result, and store
the experience.

This is intentionally not a generic chatbot, static dashboard, or fake
multi-agent voting demo.

## 2. Hackathon Context

The official "Agents That Act" hackathon emphasizes:

1.  The agent reaches something real through tools/MCP.
2.  Code written by the agent actually runs in an isolated sandbox.
3.  The agent pauses for human approval before consequential or
    irreversible actions.

Official hackathon: https://www.truefoundry.com/es/truefoundry-hackathon

TrueForge is the runtime layer providing MCP tools, sandbox execution,
approvals, subagents, sessions, context management, and related agent
infrastructure.

TrueForge: https://github.com/truefoundry/trueforge

## 3. Product

### ActionShield --- Self-Validating Autonomous Engineering Agent

Example user request:

> "The Orders API latency is too high. Investigate and fix it."

The agent should:

1.  Investigate current metrics.
2.  Inspect logs.
3.  Inspect the repository.
4.  Inspect database/schema.
5.  Retrieve relevant historical cases.
6.  Create an Action Contract.
7.  Create an isolated Git branch/workspace.
8.  Modify real code or schema.
9.  Inspect the real Git diff.
10. Run the modified application in a TrueForge sandbox.
11. Run tests and load/integration tests.
12. Collect actual metrics, logs, tests, and state diff.
13. Ask specialized reviewers to critique the change.
14. Run deterministic policy checks.
15. Reject unsafe/failed changes.
16. Adapt the implementation.
17. Re-run the changed system.
18. Repeat up to a safe retry limit.
19. Stop at a human approval checkpoint.
20. Execute in a controlled production-like environment.
21. Verify the result.
22. Store the complete incident as case memory.

## 4. Critical Design Decision

**Do not build a fake simulator that simply returns hardcoded values.**

Instead, create a small real application:

-   FastAPI
-   PostgreSQL
-   Docker Compose
-   pytest
-   load testing
-   metrics/logging
-   Git repository

The sandbox is the safe simulation/validation environment because it
runs a real miniature production-like system.

Example real problem:

``` sql
SELECT *
FROM orders
WHERE user_id = ?
ORDER BY created_at DESC;
```

The database intentionally lacks an appropriate index.

The agent investigates and may create:

``` sql
CREATE INDEX idx_orders_user_created
ON orders(user_id, created_at DESC);
```

The modified application is then actually run and measured.

Never implement:

``` text
if action == "add_index":
    return success
```

The result must come from execution.

## 5. Architecture

``` text
USER / INCIDENT
       |
       v
TRUEFORGE MAIN AGENT
       |
       +---- Historical Case Memory
       |
       +---- Action Contract
       |
       v
ACTIONSHIELD MCP
       |
       +---- Git / Repository
       +---- Application
       +---- PostgreSQL
       +---- Metrics
       +---- Logs
       +---- Tests
       +---- Safety
       |
       v
TRUEFORGE SANDBOX
       |
       v
REAL DEMO APPLICATION
       |
       +---- API
       +---- PostgreSQL
       +---- Tests
       +---- Load Generator
       +---- Metrics
       |
       v
EVIDENCE
       |
       +---- Git Diff
       +---- Metrics
       +---- Logs
       +---- Test Results
       +---- State Diff
       |
       v
REVIEWERS
       |
       +---- Performance
       +---- Reliability / DB
       +---- Security
       +---- Red Team
       |
       v
DETERMINISTIC POLICY ENGINE
       |
       v
JUDGE
    /       \
  FAIL      PASS
   |          |
   v          v
ADAPT     HUMAN APPROVAL
   |          |
   +---->     v
        CONTROLLED EXECUTION
               |
               v
          VERIFICATION
               |
               v
          CASE MEMORY
               |
               +----> FUTURE INCIDENT
```

## 6. Demo Application

Start small.

Repository:

``` text
actionshield-demo/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routes/
│   │   ├── users.py
│   │   ├── products.py
│   │   └── orders.py
│   └── services/
├── migrations/
├── tests/
├── scripts/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

Suggested endpoints:

``` text
GET /health
GET /metrics
GET /orders
GET /orders/{id}
POST /orders
GET /products
```

Database tables:

``` text
users
products
orders
order_items
```

## 7. First Engineering Incident

Use:

> "The Orders API is too slow."

Create a genuine performance issue, such as an inefficient query/index
configuration.

The agent should discover the cause instead of being told the answer.

The baseline must be reproducible:

``` text
slow API
  ↓
database investigation
  ↓
code/schema change
  ↓
faster API
```

## 8. Observability

Minimum metrics:

-   request count
-   request latency
-   p50 latency
-   p95 latency
-   error rate
-   DB query latency
-   throughput
-   CPU/memory if practical

Minimum endpoints:

``` text
GET /health
GET /metrics
```

Use structured logs with:

``` text
request_id
route
status_code
latency_ms
db_query_ms
timestamp
```

Prometheus may be added later if it materially improves the demo. Do not
add unnecessary infrastructure initially.

## 9. Load Testing

The system must produce reproducible before/after evidence.

Example:

``` text
BEFORE
Orders p95: 2400 ms
DB query:    1900 ms
Errors:      0.3%
```

After the agent changes the system:

``` text
AFTER
Orders p95: 480 ms
DB query:    180 ms
Errors:      0.2%
```

These values must come from actual execution.

Never fabricate metrics in the UI or agent response.

## 10. Git Workflow

The agent should work on an isolated branch:

``` text
main
  |
  +-- agent/incident-001
```

Capture:

``` bash
git status
git diff
```

The Git diff is part of the evidence.

Example:

``` diff
+ CREATE INDEX idx_orders_user_created
+ ON orders(user_id, created_at DESC);
```

The agent must not silently modify unrelated files.

## 11. Action Contract

Before modifying the system, create an Action Contract.

Example:

``` json
{
  "goal": "Reduce Orders API p95 latency below 700ms",
  "proposed_change": "Add an appropriate database index",
  "allowed_scope": ["database migration"],
  "constraints": [
    "No data loss",
    "Tests must pass",
    "Error rate < 1%",
    "No unrelated file changes",
    "Migration must be reversible"
  ],
  "success_criteria": [
    "p95 latency < 700ms",
    "tests pass",
    "error rate < 1%",
    "database remains healthy",
    "scope matches declared change"
  ],
  "rollback_strategy": "Remove the newly created index"
}
```

## 12. ActionShield MCP

MCP is the controlled interface between TrueForge and the engineering
environment.

Start with a small tool set.

### Repository

``` text
get_repo_status()
get_git_diff()
create_branch()
read_file()
search_code()
```

### Investigation

``` text
get_service_metrics()
get_service_logs()
get_database_schema()
get_deployment_state()
```

### Execution

``` text
run_tests()
run_load_test()
run_migration()
```

### Safety

``` text
get_action_diff()
validate_change()
rollback()
```

### Memory

``` text
search_historical_cases()
store_incident_case()
```

Code modifications may be performed using TrueForge sandbox/file
capabilities when that is cleaner. Avoid duplicating tools
unnecessarily.

## 13. TrueForge

TrueForge must be central, not decorative.

Use it for:

-   main agent runtime
-   MCP tool calls
-   sandbox execution
-   specialized subagents
-   human checkpoints
-   persistent sessions
-   context management
-   iterative reasoning/replanning

Documentation:

https://github.com/truefoundry/trueforge/tree/main/docs

Introduction:

https://github.com/truefoundry/trueforge/blob/main/docs/introduction.mdx

Quickstart:

https://github.com/truefoundry/trueforge/blob/main/docs/quickstart.mdx

MCP:

https://github.com/truefoundry/trueforge/blob/main/docs/mcp-servers.mdx

Sandbox:

https://github.com/truefoundry/trueforge/blob/main/docs/sandbox.mdx

Sessions:

https://github.com/truefoundry/trueforge/blob/main/docs/sessions.mdx

Harness capabilities:

https://github.com/truefoundry/trueforge/blob/main/docs/harness-capabilities.mdx

Skills:

https://github.com/truefoundry/trueforge/blob/main/docs/skills.mdx

## 14. TrueForge Sandbox Setup

Current TrueForge documentation supports sandbox-as-a-tool and currently
documents Daytona as the supported sandbox provider.

Daytona:

https://www.daytona.io/

Daytona docs:

https://www.daytona.io/docs/

Setup:

1.  Create a Daytona API key with the permissions currently required by
    Daytona/TrueForge.
2.  In TrueForge open:
    `Settings → Sandbox providers → Daytona → Configure`
3.  Enter the key.
4.  Save.
5.  Confirm Daytona is connected.
6.  In Build Agent → Runtime Config, enable Sandbox.

Verify exact current Daytona permissions from the dashboard/docs instead
of hardcoding assumptions.

## 15. First Sandbox Milestone

Before building MCP, prove that TrueForge can run the project.

Prompt the TrueForge agent:

``` text
Clone the ActionShield demo repository into the sandbox.

Inspect the repository.

Start the Docker Compose environment.

Verify that the API and PostgreSQL services are running.

Run the existing test suite.

Do not modify anything.

Report the actual commands executed and their actual results.
```

Expected:

``` text
TrueForge
  ↓
Sandbox
  ↓
git clone
  ↓
docker compose up
  ↓
API
  ↓
PostgreSQL
  ↓
tests
```

Do not proceed until this works.

## 16. MCP Connection

TrueForge MCP documentation:

https://github.com/truefoundry/trueforge/blob/main/docs/mcp-servers.mdx

Current UI flow:

``` text
Settings
  ↓
Connectors
  ↓
Add MCP Server
  ↓
Register ActionShield MCP
  ↓
Build Agent
  ↓
Select MCP Tools
```

Use the actual MCP URL/transport produced by the ActionShield server and
verify connectivity from the TrueForge environment.

Never invent an MCP endpoint.

## 17. Main Agent Workflow

The main agent should execute:

``` text
1. Understand incident
2. Retrieve historical cases
3. Investigate current system
4. Create Action Contract
5. Create isolated branch/workspace
6. Inspect code/database
7. Propose change
8. Apply change
9. Inspect Git diff
10. Run tests
11. Run application
12. Run load/integration tests
13. Collect evidence
14. Run reviewers
15. Run deterministic policies
16. Judge
17. If FAIL:
      explain
      replan
      modify
      retest
18. If PASS:
      human approval
19. Controlled execution
20. Verify
21. Store case
```

Maximum attempts: 3.

Never weaken constraints simply to make an action pass.

## 18. Reviewer Agents

Start with three.

### Performance

Checks:

-   latency
-   throughput
-   CPU
-   DB performance
-   regressions

Consumes:

-   Git diff
-   before metrics
-   after metrics
-   load test
-   query information

### Reliability / Database

Checks:

-   migration safety
-   data integrity
-   availability
-   resource risks
-   rollback

### Red Team

Explicitly challenges the proposed change.

Questions:

``` text
What can break?
What assumptions might be wrong?
Could this behave differently at production scale?
Could the migration lock or damage data?
Did the agent change more than it declared?
```

Add Security and Diagnosis reviewers later if time allows.

## 19. Evidence

Each attempt should create a structured evidence object.

Example:

``` json
{
  "execution_id": "exec_001",
  "git_commit": "abc123",
  "git_diff": "...",
  "before": {
    "p95_latency_ms": 2400,
    "db_query_ms": 1900,
    "error_rate": 0.3
  },
  "after": {
    "p95_latency_ms": 480,
    "db_query_ms": 180,
    "error_rate": 0.2
  },
  "tests": {
    "unit": "pass",
    "integration": "pass",
    "load": "pass"
  },
  "logs": [],
  "state_diff": {},
  "reviewers": [],
  "policy": {},
  "status": "passed"
}
```

## 20. Intent vs Reality

Agent declares:

``` text
I will modify only the database migration.
```

Actual diff:

``` text
migrations/001_add_index.sql  changed
app/orders.py                 changed
.env                          changed
```

Policy result:

``` text
ACTION SCOPE VIOLATION
```

The attempt must fail.

## 21. Deterministic Policy Engine

LLMs explain and reason. Code enforces hard constraints.

Example:

``` python
if tests_failed:
    reject()

if error_rate >= max_error_rate:
    reject()

if latency_target_not_met:
    reject()

if changed_files_outside_scope:
    reject()

if destructive_migration_detected:
    reject()

if rollback_unavailable:
    reject()
```

## 22. Adaptive Replanning

The first plan should be allowed to fail.

Example:

``` text
Attempt 1
Unsafe migration strategy
       ↓
Tests PASS
Performance PASS
Red Team FAIL
       ↓
Judge REJECT
       ↓
Agent adapts
       ↓
Attempt 2
Safer migration
       ↓
Tests PASS
Performance PASS
Reliability PASS
Red Team PASS
       ↓
Judge PASS
```

The important feature is not "the agent guessed correctly".

The important feature is:

**the agent observed consequences, understood the failure, and changed
its plan.**

## 23. Human Approval

After sandbox validation:

``` text
ACTION READY FOR APPROVAL

Goal:
Reduce Orders API latency

Validated change:
...

Evidence:
✓ Tests
✓ Performance
✓ Reliability
✓ Security
✓ Scope
✓ Rollback

[ APPROVE ]
[ REJECT ]
```

Use TrueForge's real human checkpoint/approval mechanism.

No unrestricted production deployment in the MVP.

## 24. Controlled Production Simulation

After approval:

``` text
sandbox validation
       ↓
human approval
       ↓
controlled production-like environment
       ↓
apply validated change
       ↓
observe
       ↓
verify
```

Do not connect the demo to real production infrastructure.

## 25. Case Memory

Store completed incidents.

Example:

``` json
{
  "case_id": "case_001",
  "incident": "Orders API latency spike",
  "symptoms": [
    "p95 latency > 2s",
    "high DB query latency"
  ],
  "initial_plan": "...",
  "failed_attempts": [],
  "review_findings": [],
  "successful_plan": "...",
  "evidence": {},
  "final_status": "validated"
}
```

Future incident:

``` text
search_historical_cases()
```

Historical memory is a hypothesis source, not truth.

Always verify the current system.

## 26. Case Retrieval

MVP options:

### Option A --- structured/hybrid search

Match:

-   incident type
-   service
-   endpoint
-   symptoms
-   database table
-   keywords

### Option B --- embeddings

Use only if it is quick and materially useful.

Do not introduce a vector database just to make the architecture look
sophisticated.

## 27. Repository Structure

``` text
ActionShield/
├── README.md
├── PROJECT.md
├── ARCHITECTURE.md
├── docker-compose.yml
├── .env.example
├── demo-app/
│   ├── app/
│   ├── migrations/
│   ├── tests/
│   ├── scripts/
│   ├── Dockerfile
│   └── requirements.txt
├── mcp/
│   ├── server.py
│   ├── tools/
│   │   ├── git.py
│   │   ├── metrics.py
│   │   ├── database.py
│   │   ├── testing.py
│   │   ├── safety.py
│   │   └── memory.py
│   └── models/
├── core/
│   ├── contracts.py
│   ├── evidence.py
│   ├── policy_engine.py
│   ├── intent_reality.py
│   ├── case_memory.py
│   └── replanning.py
├── agents/
│   ├── main.md
│   ├── performance.md
│   ├── reliability.md
│   └── red_team.md
├── frontend/
└── tests/
```

Adjust based on the actual TrueForge integration.

## 28. Build Order

### Phase 1 --- Demo application

Build:

-   FastAPI
-   PostgreSQL
-   Docker Compose
-   schema
-   Orders API
-   tests
-   metrics
-   intentionally slow query
-   load test

Success:

``` text
slow → change → fast
```

### Phase 2 --- Git

Implement:

-   repository
-   agent branch
-   diff
-   rollback

### Phase 3 --- TrueForge sandbox

Configure Daytona and verify the application runs inside the sandbox.

### Phase 4 --- MCP

Implement investigation, Git, testing, metrics, safety, and memory
tools.

### Phase 5 --- TrueForge integration

Connect MCP to TrueForge and build the real agent workflow.

### Phase 6 --- Action Contract + Policy

Implement:

-   constraints
-   scope
-   success criteria
-   deterministic policy
-   Intent vs Reality

### Phase 7 --- Reviewers

Implement:

-   Performance
-   Reliability/DB
-   Red Team

### Phase 8 --- Adaptive loop

Implement:

``` text
FAIL → explain → replan → modify → test → observe → review → PASS
```

### Phase 9 --- Approval

Add the TrueForge human checkpoint.

### Phase 10 --- Memory

Implement case storage and retrieval.

### Phase 11 --- UI

Only after the backend loop is reliable.

## 29. Final Demo

Five-minute flow:

``` text
00:00  User: Orders API is slow
00:20  Agent investigates
00:50  Root cause identified
01:20  Action Contract
01:40  Git branch + code/schema change
02:00  Git diff
02:15  TrueForge sandbox
02:45  Reviewers
03:00  First plan rejected
03:30  Agent adapts
03:50  Sandbox again
04:10  Judge validates
04:20  Human approval
04:40  Controlled execution + verification
04:50  Case stored
```

## 30. MVP Do NOT Build

Do not build:

-   full Kubernetes simulator
-   real AWS production deployment
-   complex distributed infrastructure
-   ML risk prediction
-   fine-tuned LLM
-   dozens of agents
-   multiple unrelated domains
-   complicated vector infrastructure
-   unrestricted host shell access
-   automatic destructive production actions
-   giant dashboard before backend works

## 31. Acceptance Criteria

A judge should be able to see:

-   TrueForge receives the incident.
-   TrueForge reaches real MCP tools.
-   Agent investigates a real repository.
-   Agent reads actual metrics.
-   Agent creates an Action Contract.
-   Agent modifies a real Git repository.
-   Real Git diff is produced.
-   Changed project runs in TrueForge sandbox.
-   Tests execute.
-   Load/integration tests execute.
-   Actual metrics/logs are collected.
-   Specialized agents review actual evidence.
-   Red Team challenges the change.
-   Deterministic policy checks enforce constraints.
-   First plan can fail.
-   Agent adapts.
-   Second plan is tested.
-   Human checkpoint appears.
-   Controlled execution happens only after approval.
-   Result is verified.
-   Incident is stored.
-   Future incident can retrieve the case.

## 32. Official Resources

### TrueForge

GitHub: https://github.com/truefoundry/trueforge

Docs: https://github.com/truefoundry/trueforge/tree/main/docs

Introduction:
https://github.com/truefoundry/trueforge/blob/main/docs/introduction.mdx

Quickstart:
https://github.com/truefoundry/trueforge/blob/main/docs/quickstart.mdx

MCP:
https://github.com/truefoundry/trueforge/blob/main/docs/mcp-servers.mdx

Sandbox:
https://github.com/truefoundry/trueforge/blob/main/docs/sandbox.mdx

Sessions:
https://github.com/truefoundry/trueforge/blob/main/docs/sessions.mdx

Harness capabilities:
https://github.com/truefoundry/trueforge/blob/main/docs/harness-capabilities.mdx

Skills:
https://github.com/truefoundry/trueforge/blob/main/docs/skills.mdx

### Hackathon

https://www.truefoundry.com/es/truefoundry-hackathon

### MCP

https://modelcontextprotocol.io/

https://modelcontextprotocol.io/specification

### Daytona

https://www.daytona.io/

https://www.daytona.io/docs/

## 33. Antigravity Instructions

Before coding:

1.  Inspect the repository.
2.  Inspect the installed/current TrueForge version.
3.  Inspect current TrueForge APIs/docs.
4.  Inspect MCP capabilities.
5.  Inspect sandbox configuration.
6.  Do not invent TrueForge APIs.
7.  Do not fabricate tool results.
8.  Do not hardcode the final demo outcome into the UI.

Work iteratively.

First build and verify the demo application.

Then verify Git.

Then verify TrueForge sandbox.

Then build MCP.

Then connect MCP to TrueForge.

Then build the agent loop.

Then reviewers/policy.

Then memory.

Then UI.

## 34. FIRST TASK --- START HERE

Do not implement the entire project immediately.

Build only:

``` text
FastAPI
+
PostgreSQL
+
Docker Compose
+
Orders API
+
Tests
+
Metrics
+
Intentional performance problem
+
Git repository
```

The first milestone is:

``` text
docker compose up
       ↓
API works
       ↓
PostgreSQL works
       ↓
/health works
       ↓
/orders works
       ↓
/metrics works
       ↓
tests pass
       ↓
Git repository exists
```

Then verify the baseline performance problem.

Only after this works should ActionShield be allowed to modify it.

## 35. Final Product Definition

ActionShield is:

> **A TrueForge-powered autonomous engineering agent that reaches a real
> software system through MCP, modifies a real codebase, runs the change
> in an isolated sandbox, observes actual application and database
> behavior, has specialized agents challenge the change, enforces
> deterministic safety policies, adapts when the change fails, pauses
> for human approval before consequential execution, verifies the
> outcome, and stores validated experience for future incidents.**

The differentiator is not:

> "We have many AI agents."

It is:

> **"The agent changes the world, observes what actually happened,
> learns from failure, and changes its plan."**

**Memory suggests. Simulation verifies. Evidence decides.**
