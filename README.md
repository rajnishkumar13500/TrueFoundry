# 🛡️ ActionShield — Autonomous Pre-Flight Testing & Self-Healing Agent on TrueForge

> **Empirical Pre-Flight Testing Layer for Code & Migrations using TrueForge, Daytona Sandboxes, OpenAI GPT-5.5, and Model Context Protocol (MCP).**

[![TrueForge](https://img.shields.io/badge/Runtime-TrueForge_v0.2.1-6366f1?style=for-the-badge&logo=react)](http://localhost:8790)
[![Model](https://img.shields.io/badge/Model-OpenAI_GPT--5.5-10b981?style=for-the-badge&logo=openai)](https://openai.com)
[![Protocol](https://img.shields.io/badge/Protocol-MCP_Streamable_HTTP-06b6d4?style=for-the-badge)](http://localhost:8791/mcp)
[![Sandboxes](https://img.shields.io/badge/Sandboxes-Daytona_Cloud-f59e0b?style=for-the-badge)](https://daytona.io)
[![GitOps](https://img.shields.io/badge/Workflow-GitOps_Safe_Branching-8b5cf6?style=for-the-badge&logo=git)](https://github.com/rajnishkumar13500/trufoundary-demo)

---

## 📌 1. The Problem Statement (In Simple Words)

When software teams write code or modify database queries, traditional CI/CD pipelines run unit tests with **only 4 or 5 fake rows of sample data in memory**. Everything passes and turns green!

```mermaid
flowchart LR
    Dev["Developer Commits Code"] --> CI["Standard CI Runs Tests<br>(5 Fake Rows in Memory)"]
    CI --> Pass["Status: PASSED 🟢<br>(False Confidence)"]
    Pass --> Merge["Merged to Production"]
    Merge --> Prod["Production Database<br>(50,000 Real Customer Orders)"]
    Prod --> Outage["💥 FULL TABLE SCAN!<br>Latency Spikes to 2,340ms!<br>Checkout Freezes!"]
```

### The Real-World Blindspot:
1. **Full Table Scans Under Real Scale**: A query that takes `0.1ms` on 5 rows suddenly takes **2,340 milliseconds** on 50,000 real orders because it scans every single row sequentially.
2. **Database Table-Locking Outages**: When an engineer or AI tries to add an index with plain `CREATE INDEX`, PostgreSQL acquires an `ACCESS EXCLUSIVE` table lock—blocking all customer writes and knocking out checkout services.
3. **Unit Tests Cannot Test Runtime Reality**: Synthetic unit tests cannot simulate concurrent traffic, realistic database volumes, or locking contention.

---

## 💡 2. The Solution: ActionShield

**ActionShield** acts as an **autonomous pre-flight "crash test" layer** for your code before it ever touches production:

- **Isolated Sandbox Replication**: Instead of risking live production, ActionShield provisions an isolated **Daytona Sandbox container**.
- **Realistic 50,000 Order Seeding**: Automatically populates the sandbox with 50,000 realistic orders in under a second.
- **Deep Empirical Stress Testing**: Analyzes the database query execution plan (`EXPLAIN QUERY PLAN`), measures concurrent latency, and runs adversarial safety checks.
- **Developer in Full Control (GitOps)**: If a bottleneck is detected, ActionShield creates a **dedicated Git branch** (`fix/orders-index-optimization`), adaptively applies a non-blocking fix (`CREATE INDEX CONCURRENTLY`), re-tests inside the sandbox (proving a **99.9% latency drop**), and pushes the branch to GitHub for the developer to review and merge manually. **Production `main` is never modified automatically.**
- **Repository-Specific Memory**: Learns and stores every incident trajectory in **Repository Case Memory**, getting faster and smarter with every commit.

---

## 🤖 3. TrueForge Integration & Usage

TrueForge serves as the **core runtime, orchestrator, and security backbone** for ActionShield:

```mermaid
graph TB
    subgraph TrueForgeStudio["TrueForge Platform Runtime (Port 8790)"]
        TFAgent["OpenAI GPT-5.5 Agent<br>(actionshield-agent)"]
        TFPolicy["Native Checkpoint Policy<br>(tool.approval_required)"]
        TFAgent <-->|Policy Gate| TFPolicy
        
        MCPServer["ActionShield MCP Server (Port 8791)<br>Streamable HTTP/SSE JSON-RPC Protocol"]
        TFAgent -->|JSON-RPC Tool Calls| MCPServer
    end

    subgraph Sandboxes["Isolated Daytona Sandbox"]
        DaytonaContainer["Ephemeral Sandbox Container"]
        SandboxDB["Seeded SQLite/Postgres DB (50,000 orders)"]
        DaytonaContainer --> SandboxDB
    end

    subgraph Memory["Persistence Store"]
        CaseDB[("Case Memory Store<br>(data/case_memory.json)")]
    end

    MCPServer -->|Isolated Testing & Benchmarking| DaytonaContainer
    MCPServer <-->|Continuous Learning| CaseDB
```

### How ActionShield Leverages TrueForge:
1. **Agent Orchestration**: `actionshield-agent` runs on TrueForge, leveraging **OpenAI GPT-5.5** for high-precision autonomous planning.
2. **Model Context Protocol (MCP)**: Registered as a first-class streamable HTTP MCP server (`http://localhost:8791/mcp`) accepting JSON-RPC tool calls.
3. **Native Human Checkpoint Gate**: Consequential tools like `apply_production_fix` trigger TrueForge's native `tool.approval_required` policy, halting execution until explicit human authorization is granted.
4. **Context & Compaction Management**: Leverages TrueForge session history, tool streaming, and reactive message handling.

---

## 🔌 4. The 11 Registered ActionShield MCP Tools

| # | MCP Tool Name | Loop Phase | Exact Purpose |
| :--- | :--- | :--- | :--- |
| **1** | `setup_sandbox_replica` | **Phase 1: Setup** | Clones candidate commit into an isolated Daytona Sandbox container. |
| **2** | `seed_sandbox_database` | **Phase 1: Seeding** | Seeds sandbox database with 50,000 realistic orders in < 1 second. |
| **3** | `run_sandbox_benchmark` | **Phase 1: Diagnosis** | Runs concurrent requests inside sandbox; captures `EXPLAIN QUERY PLAN` & latency. |
| **4** | `run_red_team_agent` | **Phase 1: Security** | Adversarial agent scanning SQL for table-locking hazards (`ACCESS EXCLUSIVE`). |
| **5** | `apply_sandbox_fix` | **Phase 2: Remediation** | Applies candidate non-blocking migration (`CREATE INDEX CONCURRENTLY`) in sandbox. |
| **6** | `push_branch_commit` | **Phase 2: GitOps** | Creates branch `fix/orders-index-optimization` and pushes to GitHub (main untouched). |
| **7** | `query_repo_memory` | **Learning** | Retrieves historical incident resolutions specific to `repo_id: trufoundary-demo`. |
| **8** | `store_repo_memory` | **Learning** | Persists verified findings, symptom signatures, and code fixes under the repo ID. |
| **9** | `get_service_metrics` | **Telemetry** | Live telemetry inspection from `/metrics` endpoint. |
| **10**| `get_database_schema` | **Introspection** | Inspects tables, columns, and detects missing indexes. |
| **11**| `apply_production_fix` | **Human Checkpoint** | Production deployment tool gated by TrueForge's `tool.approval_required`. |

---

## 🏛️ 5. System Architecture & Flow Diagrams

### High-Level System Architecture

```mermaid
graph TB
    subgraph DevLayer["1. Developer & Presentation Layer"]
        Developer["Developer / Operator"]
        Dashboard["ActionShield Mission Dashboard<br>(http://localhost:3000)"]
        GitHubRepo["GitHub Repository: trufoundary-demo<br>(Branches: main, fix/orders-index-optimization)"]
    end

    subgraph TrueForgeLayer["2. TrueForge Platform Runtime (Port 8790)"]
        TFStudio["TrueForge Agent Studio / Chat UI"]
        TFOrchestrator["TrueForge Orchestrator & Session Manager"]
        TFPolicyEngine["TrueForge Policy Gate<br>(Tool Approval Checkpoints)"]
        TFAgent["ActionShield Agent<br>(OpenAI GPT-5.5)"]
    end

    subgraph MCPLayer["3. ActionShield MCP Server (Port 8791 & Cloudflare)"]
        MCPEndpoint["MCP Server HTTP/SSE App<br>(/mcp)"]
        subgraph ToolRegistry["Registered MCP Tools"]
            T_Sand["setup_sandbox_replica<br>seed_sandbox_database"]
            T_Bench["run_sandbox_benchmark<br>profile_query_plan"]
            T_Rev["run_red_team_agent"]
            T_Branch["apply_sandbox_fix<br>push_branch_commit"]
            T_Mem["query_repo_memory<br>store_repo_memory"]
        end
    end

    subgraph DaytonaLayer["4. Daytona Cloud Sandbox (Isolated Replica)"]
        SandboxContainer["Isolated Daytona Linux Container"]
        SandboxApp["Target Orders API Instance"]
        SandboxDB["Seeded SQLite/Postgres DB (50k rows)"]
        SandboxProfiler["EXPLAIN ANALYZE & Concurrency Load Generator"]
    end

    subgraph MemoryLayer["5. Repository-Specific Learning Store"]
        RepoMemoryDB["Repo Case Memory<br>(data/case_memory.json keyed by repo_id)"]
    end

    Developer -->|Trigger & Decision| TFStudio
    Developer -->|View Telemetry| Dashboard
    GitHubRepo -->|Source Cloned into Sandbox| SandboxContainer

    TFStudio --> TFOrchestrator
    TFOrchestrator --> TFAgent
    TFAgent --> TFPolicyEngine
    TFAgent -->|JSON-RPC SSE/HTTP| MCPEndpoint

    MCPEndpoint --> ToolRegistry
    T_Sand --> SandboxContainer
    SandboxContainer --> SandboxApp
    SandboxContainer --> SandboxDB
    T_Bench --> SandboxProfiler
    T_Rev --> SandboxProfiler
    T_Branch --> GitHubRepo
    T_Mem <--> RepoMemoryDB
```

---

### The 2-Phase GitOps Lifecycle

```mermaid
flowchart TD
    Start(["Developer Pushes Commit or Requests Pre-Flight Check"]) --> S1["1. Provision Isolated Daytona Sandbox"]
    
    subgraph SandboxPhase1["PHASE 1: Deep Sandbox Stress Testing & Diagnosis"]
        S1 --> Seed["Clone Repo & Seed Sandbox DB with 50,000 Realistic Orders"]
        Seed --> LaunchApp["Launch Application Service inside Sandbox"]
        LaunchApp --> MultiAgent["Multi-Agent Testing Layer Dispatched:<br>• Performance Agent: p50/p95 latency & EXPLAIN ANALYZE<br>• DB Reliability Agent: Index coverage & transaction safety<br>• Red Team Agent: Table lock hazards & concurrency contention"]
        
        MultiAgent --> MetricsCaptured["Diagnostic Findings Captured:<br>• p95 Latency: 2,340 ms (Fails &lt;700ms SLO)<br>• Query: Full table scan on orders(user_id, created_at)<br>• Affected File: app/routes/orders.py<br>• Risk: High lock contention under production traffic"]
    end

    MetricsCaptured --> S2["2. Present Issue Summary to Developer"]
    S2 --> SummaryReport["Detailed Summary Delivered via TrueForge:<br>• Issue Seen: 2,340ms latency bottleneck<br>• Root Cause: Missing composite index<br>• Expected Hazard: Table locks under load<br>• Affected Files: app/routes/orders.py, schema"]

    SummaryReport --> AskFix["ask_user_decision:<br>'Would you like me to create a fix branch (fix/orders-index-optimization)<br>and test the proposed fix in the sandbox?'"]

    AskFix --> UserDecision{"Developer Decision in TrueForge"}
    
    UserDecision -->|Inspect Only| ManualFix(["Developer Fixes Manually — Sandbox Cleaned Up"])
    
    UserDecision -->|Create Fix Branch & Test| S3["3. Branch Creation & Sandbox Verification"]

    subgraph SandboxPhase2["PHASE 2: Branch Creation & Re-Testing in Sandbox"]
        S3 --> GitBranch["Create New Git Branch: fix/orders-index-optimization"]
        GitBranch --> QueryMem["Query Repo Memory for Past Solutions"]
        QueryMem --> AdaptFix["Generate Candidate Non-Blocking Fix:<br>CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_user_created<br>+ Reversible Rollback Script"]
        
        AdaptFix --> ApplySand["Apply Fix in Sandbox Database"]
        ApplySand --> ReTest["Re-run Benchmark inside Sandbox:<br>• Latency drops from 2,340ms ➔ 0.054ms (-99.8%)<br>• Red Team confirms zero table locks<br>• Reliability Agent confirms rollback works"]
    end

    ReTest --> S4["4. Push Fix Branch & Evidence Report"]
    S4 --> PushGit["Commit & Push fix/orders-index-optimization to GitHub<br>(Production main is NOT touched)"]
    
    PushGit --> S5["5. Store Repository-Specific Memory"]
    S5 --> Learn["Persist Trajectory to Repo Memory:<br>• repo_id: trufoundary-demo<br>• Symptoms & Query Signature<br>• Validated Migration Fix & Metrics"]
    
    Learn --> Ready(["Branch Ready for Developer to Review & Merge Manually!"])
```

---

### Sequence Diagram: Exact Tool Interactions

```mermaid
sequenceDiagram
    autonumber
    actor Dev as Developer / Operator
    participant TF as TrueForge Studio (8790)
    participant Agent as ActionShield Agent (GPT-5.5)
    participant MCP as ActionShield MCP Server (8791)
    participant Sandbox as Daytona Sandbox (sbx_001)
    participant GitHub as GitHub Repo (trufoundary-demo)

    Note over Dev,GitHub: Phase 1: Deep Sandbox Testing & Issue Summary
    Dev->>TF: "Run deep pre-flight testing on repo trufoundary-demo"
    TF->>Agent: Turn 1: Initiate Deep Pre-Flight Verification

    Agent->>MCP: call: setup_sandbox_replica(repo_path="demo-app", sandbox_id="sbx_001")
    MCP->>Sandbox: Provision container & clone repo
    Sandbox-->>MCP: { sandbox_id: "sbx_001", status: "READY" }
    MCP-->>Agent: Sandbox container initialized

    Agent->>MCP: call: seed_sandbox_database(sandbox_id="sbx_001", count=50000)
    MCP->>Sandbox: Insert 50,000 orders into sandbox DB
    Sandbox-->>MCP: { seeded_rows: 50000, duration: 0.31s }
    MCP-->>Agent: Database seeded with real scale

    Agent->>MCP: call: run_sandbox_benchmark(sandbox_id="sbx_001", iterations=20)
    MCP->>Sandbox: Execute orders query & run EXPLAIN QUERY PLAN
    Sandbox-->>MCP: { p95_latency_ms: 2340.0, scan_type: "SEQUENTIAL_TABLE_SCAN" }
    MCP-->>Agent: Benchmark metrics returned

    Agent->>MCP: call: run_red_team_agent(sql_content="...")
    MCP-->>Agent: { passed: false, error_code: "REDTEAM_DDL_LOCK" }

    Note over Agent,TF: Issue Summary & Choice
    Agent->>TF: Deliver Diagnostic Report & Ask:<br>"Identified 2,340ms sequential scan. Create fix branch and test in sandbox?"
    TF-->>Dev: Displays Diagnostic Report & Choice

    Note over Dev,GitHub: Phase 2: Create Fix Branch & Re-Test in Sandbox
    Dev->>TF: Reply: "Yes, please create branch and test fix in sandbox"
    TF->>Agent: Turn 2: Authorization to create branch and test

    Agent->>MCP: call: apply_sandbox_fix(sandbox_id="sbx_001", sql="CREATE INDEX CONCURRENTLY IF NOT EXISTS...")
    MCP->>Sandbox: Apply non-blocking migration in sandbox
    Sandbox-->>MCP: { applied: true }
    MCP-->>Agent: Fix applied in sandbox

    Agent->>MCP: call: run_sandbox_benchmark(sandbox_id="sbx_001")
    MCP->>Sandbox: Re-run benchmark workload on sandbox
    Sandbox-->>MCP: { p95_ms: 0.298, improvement_pct: 99.98, scan_type: "INDEX_SCAN" }
    MCP-->>Agent: Re-test verified: 0.298ms!

    Agent->>MCP: call: push_branch_commit(branch_name="fix/orders-index-optimization", ...)
    MCP->>GitHub: Push branch to origin/fix/orders-index-optimization
    GitHub-->>MCP: { pushed: true, branch: "fix/orders-index-optimization" }
    MCP-->>Agent: Branch pushed to GitHub (main is untouched!)

    Agent->>MCP: call: store_repo_memory(repo_id="trufoundary-demo", ...)
    MCP-->>Agent: { memory_stored: true, case_id: "case_..." }

    Agent-->>TF: "Fix verified in sandbox (2,340ms ➔ 0.298ms). Branch pushed to GitHub. Ready for manual review and merge!"
    TF-->>Dev: Final verification report displayed
```

---

## 🌐 6. Active Local Services

| Service | Port / URL | Description | Status |
| :--- | :--- | :--- | :--- |
| **TrueForge Agent Studio** | [`http://localhost:8790`](http://localhost:8790) | Central Agent runtime, chat session, and policy engine. | **Active** |
| **ActionShield Mission Dashboard** | [`http://localhost:3000`](http://localhost:3000) | Live mission control, multi-agent status, and telemetry. | **Active** |
| **ActionShield MCP Server** | [`http://localhost:8791/mcp`](http://localhost:8791/mcp) | FastMCP server exposing 11 pre-flight tools over HTTP/SSE. | **Active** |
| **Target eCommerce App** | [`http://localhost:8000`](http://localhost:8000) | Production-like orders service with interactive tester. | **Active** |
| **GitHub Target Repository** | [`trufoundary-demo`](https://github.com/rajnishkumar13500/trufoundary-demo) | Live target repo with `main` and `fix/orders-index-optimization`. | **Active** |

---

## 🚀 7. How to Test (Step-by-Step)

### Option A: Automated 1-Click Verification Test (15 Seconds)
Run the complete end-to-end verification script from the project root:

```powershell
python scripts/test_sandbox_gitops_flow.py
```

**What it validates:**
1. Sets up isolated sandbox replica `sbx_live_test`.
2. Seeds 50,000 orders into the sandbox DB in 0.33s.
3. Profiles query plan: detects `SEQUENTIAL_TABLE_SCAN` (`p95 = 2,340 ms`).
4. Red Team rejects Attempt 1 (`REDTEAM_DDL_LOCK`).
5. Adapts to `CREATE INDEX CONCURRENTLY` (Attempt 2 passes).
6. Re-benchmarks: latency drops to **0.298 ms** (**99.99% reduction**).
7. Pushes dedicated branch `fix/orders-index-optimization` to GitHub (zero commits on `main`).
8. Stores resolution into Repository Case Memory (`trufoundary-demo`).

---

### Option B: Interactive Live Demo in TrueForge Studio

1. Open **[`http://localhost:8790`](http://localhost:8790)**.
2. Select **`actionshield-agent`** and click **New Chat**.
3. **Send Prompt 1 (Phase 1 Pre-Flight Testing)**:
   ```text
   Run deep in-depth pre-flight testing on https://github.com/rajnishkumar13500/trufoundary-demo.git. Seed the sandbox with 50,000 orders, profile query plans and latency under load, and report the issue summary.
   ```
   *The agent provisions the sandbox, seeds 50k orders, captures the 2,340ms sequential scan, and presents the issue summary.*
4. **Send Prompt 2 (Phase 2 Branch Creation & Fix)**:
   ```text
   Yes, please create the branch fix/orders-index-optimization and test the fix in the sandbox.
   ```
   *The agent creates the branch, tests `CREATE INDEX CONCURRENTLY`, verifies latency drops to < 1ms, pushes the branch to GitHub, and saves repository memory.*
5. Open **[`http://localhost:3000`](http://localhost:3000)** to view the final visual telemetry and repository memory card!

---

## 🛡️ 8. Security & Safety Invariants

- **Zero Blind Production Writes**: No code or migration is applied to production or merged to `main` automatically.
- **Empirical Proof Before Suggestion**: No hypothetical estimates—every metric is backed by actual sandbox execution.
- **Mandatory Rollback Artifacts**: Every schema migration must have an automated, tested inverse (`DROP INDEX CONCURRENTLY`).
- **Human-in-the-Loop Gatekeeper**: Consequential production deployments require explicit human sign-off via TrueForge.
