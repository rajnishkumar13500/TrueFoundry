# 🎬 ActionShield 3-Minute Demo Video Script (TrueForge-Focused)

**Total Duration**: 2 minutes 50 seconds (Under the 3:00 minute hard limit)  
**Primary Screen**: **TrueForge Agent Studio ([`http://localhost:8790`](http://localhost:8790))** for 85% of the video  
**Final Screen**: **ActionShield Mission Dashboard ([`http://localhost:3000`](http://localhost:3000))** for the final 25 seconds  
*(Note: No need to show `localhost:8000`. We verbally mention the demo repository).*

---

## ⏱️ Video Breakdown

| Timestamp | Section | Active Screen | Focus |
| :--- | :--- | :--- | :--- |
| **00:00 - 00:20** (20s) | **1. The Problem Statement** | TrueForge Studio (`:8790`) | Explain CI unit test blindspot under 50,000 orders. |
| **00:20 - 00:35** (15s) | **2. The Solution: ActionShield** | TrueForge Studio (`:8790`) | Introduce ActionShield as pre-flight sandbox layer. |
| **00:35 - 01:15** (40s) | **3. TrueForge Agent & MCP Tools Showcase** | TrueForge Studio (`:8790`) | **Deep-dive on the ActionShield MCP tools & architecture.** |
| **01:15 - 01:50** (35s) | **4. Phase 1 Demo: Deep Sandbox Testing** | TrueForge Chat (`:8790`) | Real-time run: seeds 50k orders, query profiling, issue report. |
| **01:50 - 02:25** (35s) | **5. Phase 2 Demo: GitOps Branch & Sandbox Fix** | TrueForge Chat (`:8790`) | Red Team block ➔ Adaptive index ➔ 0.29ms latency drop. |
| **02:25 - 02:50** (25s) | **6. Final Visual Result & Repo Memory** | **Mission Dashboard (`:3000`)** | **Switch to `:3000` to show visual metrics & Case Memory.** |

---

## 🎙️ Scene-by-Scene Script

### 🎬 Part 1: The Problem Statement (00:00 – 00:20)
**On Screen**: TrueForge Agent Studio ([`http://localhost:8790`](http://localhost:8790)) on screen.

> **Voiceover (Narrator)**:  
> *"When engineers or AI agents push code changes, standard CI unit tests pass with five fake rows in memory. But in production under fifty thousand customer orders, queries trigger full table scans, latency spikes above two seconds, and unindexed migrations lock tables. Unit tests simply cannot test runtime reality."*

---

### 🎬 Part 2: The Solution — ActionShield (00:20 – 00:35)
**On Screen**: TrueForge Agent Studio ([`http://localhost:8790`](http://localhost:8790)). Point to `actionshield-agent`.

> **Voiceover (Narrator)**:  
> *"That's why we built ActionShield on TrueForge. Using a production-like eCommerce orders repository, ActionShield acts as an autonomous pre-flight testing layer that replicates the repo in an isolated sandbox, seeds real production data, stress-tests queries, and adaptively heals bottlenecks on a safe Git branch."*

---

### 🎬 Part 3: TrueForge Agent & MCP Tools Showcase (00:35 – 01:15)
**On Screen**: TrueForge Agent Studio ([`http://localhost:8790`](http://localhost:8790)). Open the agent settings/tools panel showing the registered `actionshield-mcp` tools. Hover over the tools as you mention them.

> **Voiceover (Narrator)**:  
> *"Here in TrueForge, our ActionShield agent is powered by eleven specialized MCP tools we built for this hackathon:  
> • `setup_sandbox_replica` and `seed_sandbox_database`: Provisions an isolated sandbox container and seeds 50,000 realistic orders in under a second.  
> • `run_sandbox_benchmark`: Runs concurrent load and executes EXPLAIN QUERY PLAN to analyze real database query access patterns.  
> • `run_red_team_agent`: An adversarial safety agent that scans migrations for table-locking hazards like ACCESS EXCLUSIVE locks.  
> • `push_branch_commit`: Enforces GitOps safety—creating a dedicated branch on GitHub so main is never modified automatically.  
> • And `query_repo_memory`: Stores and retrieves historical incident resolutions specific to this repository."*

---

### 🎬 Part 4: Phase 1 Demo — Deep Sandbox Testing & Output (01:15 – 01:50)
**On Screen**: TrueForge Chat. Send prompt:  
`Run deep pre-flight testing on https://github.com/rajnishkumar13500/trufoundary-demo.git. Seed the sandbox with 50,000 orders and report what you find.`  
Point to the streaming tool calls and the final report.

> **Voiceover (Narrator)**:  
> *"Let's see it in action. In seconds, the agent provisions sandbox sbx_001, seeds 50,000 orders, and profiles the query execution plan.  
>  
> Look at the report: It uncovered a sequential table scan on orders, measured a p95 latency of 2,340 milliseconds, and flagged high lock contention.  
>  
> Production is completely untouched. The agent presents the developer with the exact affected files, query plan, and asks if we want to create a branch to test a fix."*

---

### 🎬 Part 5: Phase 2 Demo — GitOps Branching & Adaptive Fix (01:50 – 02:25)
**On Screen**: In TrueForge Chat, send reply:  
`Yes, please create the branch fix/orders-index-optimization and test the fix in the sandbox.`  
Watch the agent create the branch, trigger the Red Team reviewer, adapt the migration, and re-benchmark.

> **Voiceover (Narrator)**:  
> *"We authorize the fix. Watch the closed-loop adaptation:  
> Attempt 1 tries a plain CREATE INDEX. Our Red Team agent immediately blocks it—warning that it takes an exclusive table lock!  
>  
> ActionShield adaptively rewrites the migration to CREATE INDEX CONCURRENTLY with an automated rollback script.  
>  
> It re-benchmarks inside the sandbox: the query plan flips to an Index Scan, and latency drops from 2,340 milliseconds down to 0.29 milliseconds—a 99.9% improvement with zero table locks!"*

---

### 🎬 Part 6: Final Visual Result & Repository Memory (02:25 – 02:50)
**On Screen**: **Switch to Tab 2 ([`http://localhost:3000`](http://localhost:3000) — Mission Dashboard)**. Point to the glowing before/after latency comparison (2,340ms ➔ 0.054ms), the Reviewer badges, and the Repository Memory card.

> **Voiceover (Narrator)**:  
> *"And here is the final visual result on our ActionShield Mission Dashboard:  
> You can see the 99.8% verified latency drop, all reviewer sign-offs, and the verified branch pushed to GitHub for manual developer review.  
>  
> Crucially, it stores this lesson in Repository Case Memory—so future commits to this repository benefit from past discoveries.  
>  
> That is ActionShield on TrueForge: Deep sandbox testing, adaptive healing, and continuous repository learning. Thank you!"*

---

## 🎯 Recording Pacing Cheatsheet
- **0:00 – 0:35**: Problem & Solution (TrueForge screen)
- **0:35 – 01:15**: **Expanded MCP Tools Showcase** (TrueForge tools panel)
- **01:15 – 01:50**: Phase 1 Deep Sandbox Testing (TrueForge chat report)
- **01:50 – 02:25**: Phase 2 GitOps Branch & Fix (TrueForge chat)
- **02:25 – 02:50**: **Switch to `:3000` Dashboard for final visual punchline!**
