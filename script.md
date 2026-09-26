# 🎬 ActionShield 3-Minute Demo Video Script (Updated Flow)

**Total Duration**: 2 minutes 50 seconds (Under the 3-minute hard limit)  
**Speaking Pace**: Crisp & Moderate (~135 words per minute)  
**Tabs Prepared**:
1. **Tab 1**: TrueForge Agent Studio — [`http://localhost:8790`](http://localhost:8790) (or MCP Tool Config)
2. **Tab 2**: ActionShield Mission Dashboard — [`http://localhost:3000`](http://localhost:3000)
3. **Tab 3**: Target Orders App — [`http://localhost:8000`](http://localhost:8000)
4. **Tab 4**: GitHub Repository — [`https://github.com/rajnishkumar13500/trufoundary-demo`](https://github.com/rajnishkumar13500/trufoundary-demo)

---

## ⏱️ Video Breakdown

| Timestamp | Section | Visual Screen |
| :--- | :--- | :--- |
| **00:00 - 00:20** (20s) | **1. The Problem Statement** | Target App (`:8000`) or slide showing 2,340ms latency spike. |
| **00:20 - 00:40** (20s) | **2. The Solution: ActionShield** | Mission Dashboard (`:3000`) showing the 2-phase closed-loop architecture. |
| **00:40 - 01:15** (35s) | **3. TrueForge Agent & MCP Tools** | TrueForge Studio (`:8790`) showing registered ActionShield MCP tools. |
| **01:15 - 01:50** (35s) | **4. Phase 1 Demo: Deep Sandbox Testing** | Triggering TrueForge chat; agent seeds 50k orders & profiles query plan. |
| **01:50 - 02:25** (35s) | **5. Phase 2 Demo: Adaptive Fix & Branch** | Agent creates `fix/orders-index-optimization`, re-tests, latency drops to 0.29ms. |
| **02:25 - 02:50** (25s) | **6. Repository Memory & Developer Handover** | Case Memory card & GitHub branch. Wrap up and thank judges. |

---

## 🎙️ Scene-by-Scene Script

### 🎬 Part 1: The Problem Statement (00:00 – 00:20)
**On Screen**: Open Tab 3 ([`http://localhost:8000`](http://localhost:8000)). Click `⚡ Run Orders Query` — show the 2+ second latency.

> **Voiceover (Narrator)**:  
> *"When engineers or AI agents push code, CI unit tests pass with 5 fake rows in memory. But in production under 50,000 orders, disaster strikes: queries trigger full table scans, latency spikes above 2 seconds, and unindexed migrations lock tables. Unit tests cannot test runtime reality."*

---

### 🎬 Part 2: The Solution — ActionShield (00:20 – 00:40)
**On Screen**: Switch to Tab 2 ([`http://localhost:3000`](http://localhost:3000) — Mission Dashboard). Point out the isolated sandbox loop and multi-agent reviewers.

> **Voiceover (Narrator)**:  
> *"We built ActionShield on TrueForge: an autonomous pre-flight testing layer. Instead of risking production, ActionShield spins up an isolated Daytona sandbox replica, seeds it with 50,000 realistic orders, stress-tests the code under load, and adaptively heals bottlenecks on a dedicated Git branch."*

---

### 🎬 Part 3: TrueForge Agent & MCP Tools Showcase (00:40 – 01:15)
**On Screen**: Switch to Tab 1 ([`http://localhost:8790`](http://localhost:8790) — TrueForge Agent Studio). Show `actionshield-agent` and its registered MCP server tools.

> **Voiceover (Narrator)**:  
> *"Powering this is our ActionShield Agent on TrueForge, backed by 11 purpose-built MCP tools:  
> • `setup_sandbox_replica` and `seed_sandbox_database`: Clones the repo and seeds 50,000 orders in under a second.  
> • `run_sandbox_benchmark`: Measures true p95 latency and profiles query execution plans.  
> • `run_red_team_agent`: Scans migrations for production-breaking table locks.  
> • `push_branch_commit`: Safely branches and pushes to GitHub without touching main.  
> • And `query_repo_memory`: Retrieves historical incident patterns specific to this repository."*

---

### 🎬 Part 4: Phase 1 Demo — Deep Sandbox Testing & Output (01:15 – 01:50)
**On Screen**: In TrueForge Chat, send:  
`Run deep pre-flight testing on https://github.com/rajnishkumar13500/trufoundary-demo.git. Seed the sandbox with 50,000 orders and report what you find.`  
Point to the streaming tool executions and the final Pre-Flight Report.

> **Voiceover (Narrator)**:  
> *"Let's run a pre-flight test. In seconds, the agent provisions sandbox sbx_001, seeds 50,000 records, and runs EXPLAIN QUERY PLAN.  
>  
> Look at the report: It detected a sequential table scan on orders, measured a p95 latency of 2,340 milliseconds, and flagged high lock contention.  
>  
> Notice the developer is in control: Production is 100% untouched. The agent presents the issue summary and asks if we want to create a branch to test a fix."*

---

### 🎬 Part 5: Phase 2 Demo — GitOps Branching & Adaptive Fix (01:50 – 02:25)
**On Screen**: Send reply in TrueForge:  
`Yes, please create the branch fix/orders-index-optimization and test the fix in the sandbox.`  
Watch the agent create the branch, trigger the Red Team, adapt SQL, and re-benchmark.

> **Voiceover (Narrator)**:  
> *"We authorize the fix. Watch the closed-loop adaptation:  
> Attempt 1 tries a plain CREATE INDEX. Our Red Team agent immediately blocks it—warning that it takes an exclusive table lock!  
>  
> ActionShield adaptively rewrites the migration to CREATE INDEX CONCURRENTLY with a rollback script.  
>  
> It re-benchmarks inside the sandbox: the query plan flips to an Index Scan, and latency drops from 2,340 milliseconds to 0.29 milliseconds—a 99.9% improvement!"*

---

### 🎬 Part 6: Repository Memory & Developer Handover (02:25 – 02:50)
**On Screen**:  
1. Switch to Tab 4 ([GitHub Repository](https://github.com/rajnishkumar13500/trufoundary-demo/tree/fix/orders-index-optimization)): Show branch `fix/orders-index-optimization`. Point out `main` is clean.  
2. Switch to Tab 2 ([`http://localhost:3000`](http://localhost:3000)): Highlight the Repository Case Memory store.

> **Voiceover (Narrator)**:  
> *"ActionShield pushes the verified branch to GitHub for developers to review and merge manually. Main is never modified automatically.  
>  
> Crucially, it stores this trajectory in Repository-Specific Memory. As your codebase evolves across commits, ActionShield learns and recalls past solutions in milliseconds.  
>  
> That is ActionShield on TrueForge: Deep sandbox testing, adaptive healing, and continuous repository learning. Thank you!"*

---

## 🎯 Pacing Guidelines
- **0:00 – 0:40**: Problem & Solution (fast, punchy)
- **0:40 – 1:15**: TrueForge Agent & MCP Tools (clear tool highlights)
- **1:15 – 1:50**: Phase 1 Sandbox Testing (empirical report)
- **1:50 – 2:25**: Phase 2 Adaptive Branching & Fix (99.9% latency drop)
- **2:25 – 2:50**: Repo Memory & GitOps Handover (finish on 2:50)
