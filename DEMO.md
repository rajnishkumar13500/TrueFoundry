# 🛡️ ActionShield — Hackathon Jury Demo Guide & GitOps Verification

### 🎯 The Core Mission & GitOps Philosophy
ActionShield is a **Deep Pre-Flight Production Testing Layer**:
- **The Problem**: Unit tests in CI pass with a few rows in memory, but completely miss full table scans on 50,000 orders and table-locking DDL hazards (`ACCESS EXCLUSIVE` locks).
- **Phase 1 (Deep Sandbox Testing)**: ActionShield pulls the repository into an isolated Daytona Sandbox container, seeds it with 50,000 realistic orders, runs query plan profiling (`EXPLAIN ANALYZE`), runs Red Team checks, and presents a **detailed Issue Summary** to the developer (Affected files, query plan, latency).
- **Phase 2 (Safe Branching & Re-testing)**: When the developer asks to fix the issue, ActionShield creates a **new Git branch (`fix/orders-index-optimization`)**, applies the non-blocking fix, **re-tests inside the sandbox**, and pushes the branch to GitHub.
- **Developer in Full Control**: ActionShield **never forces a merge to `main`**. The developer receives the evidence report and can inspect the branch and merge manually whenever they are ready!
- **Continuous Learning**: ActionShield stores the verified lesson in **Repository-Specific Case Memory**, so future commits benefit from past discoveries.

---

## 🖥️ Live Service Surfaces & URLs

Before starting your presentation, ensure these 3 browser tabs are open:

| Service | URL | Purpose in Demo |
| :--- | :--- | :--- |
| **Demo eCommerce App** | [`http://localhost:8000`](http://localhost:8000) | Live target application. Shows orders and has an interactive button to test live latency. |
| **TrueForge Agent Studio** | [`http://localhost:8790`](http://localhost:8790) | The core hackathon agent runtime. Where OpenAI GPT-5.5 reasons, calls MCP tools, presents the issue summary, and asks for developer decisions. |
| **ActionShield Mission Dashboard** | [`http://localhost:3000`](http://localhost:3000) | Visual mission control showing the multi-agent testing layer, sandbox benchmark metrics, reviewer verdicts, and Case Memory. |

---

## 🎬 5-Minute Jury Demo Script

Follow these exact steps in front of the jury:

### Step 1: Hook the Jury with the Real-World Developer Dilemma (45 Seconds)
1. **Open Tab 1**: [`http://localhost:8000`](http://localhost:8000) (Demo Orders App).
2. **Action**: Click the button `⚡ Run Orders Query (user_id=1)`.
3. **What happens**: The query takes time, and the latency counter displays high latency (> 2,000ms).
4. **What to say**:
   > *"Good morning judges. Consider what happens when an engineer pushes a commit that adds a new query or modifies an SQL schema. Standard CI runs unit tests with a handful of rows in memory, says 'All Tests Passed', and merges it.*
   > *Then in production with 50,000 orders, checkout freezes because the query does a full sequential scan taking 2,340ms, and an unindexed column creates lock contention.*
   > *That is why we built ActionShield: an autonomous production pre-flight testing layer on TrueForge."*

---

### Step 2: Trigger Phase 1 — Deep Sandbox Testing & Issue Summary (1 Minute)
1. **Open Tab 2**: [`http://localhost:8790`](http://localhost:8790) (TrueForge Agent Studio).
2. **Action**: Select the agent `actionshield-agent` and click **New Chat** (or open the prepared demo session).
3. **Prompt to send**:
   ```text
   Run deep in-depth pre-flight testing on https://github.com/rajnishkumar13500/trufoundary-demo.git. Seed the sandbox with 50,000 orders, profile query plans and latency under load, and report the issue summary.
   ```
4. **What happens in TrueForge**:
   - The agent sets up the isolated Daytona sandbox and seeds the database with 50,000 orders.
   - It runs load testing and query plan profiling inside the sandbox.
   - It runs the **Red Team Agent** to inspect lock contention.
   - It presents the **Detailed Issue Summary**:
     - **Issue Seen**: `p95 Latency = 2,340 ms` (Sequential table scan on 50,000 rows).
     - **Expected Failure**: High database contention under concurrent user traffic.
     - **Affected Files**: `app/routes/orders.py`, `orders` table.
     - **Suggested Fix**: Non-blocking composite index on `orders(user_id, created_at DESC)`.
     - **Interactive Prompt**: *"Would you like me to create a fix branch (fix/orders-index-optimization) and test the proposed solution in the sandbox?"*
5. **What to say**:
   > *"Notice that ActionShield tests everything deeply inside the sandbox replica first. It gives the engineer an exact diagnosis: the affected file, the exact query plan, and the expected failure mode under production load."*

---

### Step 3: Trigger Phase 2 — Create Fix Branch & Re-Test in Sandbox (1.5 Minutes)
1. **Action**: In TrueForge, reply:
   ```text
   Yes, please create the branch fix/orders-index-optimization and test the fix in the sandbox.
   ```
2. **Watch TrueForge Screen**:
   - The agent creates a dedicated branch: `fix/orders-index-optimization`.
   - It consults **Repository Memory** for matching historical solutions.
   - **Attempt 1 Fails Safely**: The Red Team agent flags standard `CREATE INDEX` as a table-locking hazard (`ACCESS EXCLUSIVE`).
   - **Adaptive Replanning**: ActionShield adapts the SQL to `CREATE INDEX CONCURRENTLY` and generates a reversible rollback script.
   - **Attempt 2 Passes in Sandbox**:
     - `Old Latency: 2,340 ms`
     - `New Latency: 0.054 ms (99.8% improvement!)`
     - `Reviewers: Performance PASS, Reliability PASS, Red Team PASS`
3. **What to say**:
   > *"Here is the 'Aha!' moment of ActionShield: closed-loop adaptive replanning. In Attempt 1, the agent proposed an index that would lock tables. The Red Team caught it. The agent adapted to use CONCURRENTLY, re-tested inside the sandbox, and proved a 99.8% latency reduction with zero table locks."*

---

### Step 4: Push Fix Branch to GitHub & Store Repo Memory (45 Seconds)
1. **Watch TrueForge Screen**:
   - The agent commits the verified migration to `fix/orders-index-optimization` and pushes the branch to GitHub.
   - **Production `main` is NOT modified automatically**: The developer receives the branch link and evidence package to review and merge manually!
   - The agent stores the incident pattern and verified solution in **Repository-Specific Memory** (`repo_id: trufoundary-demo`).
2. **What to say**:
   > *"Notice our GitOps safety guarantee: ActionShield does not blindly force changes onto main. It creates a clean, verified branch on GitHub with an evidence package so the developer can review and merge manually. It also memorizes this lesson specifically for this repository, making future runs instant."*

---

### Step 5: Verify the Result (30 Seconds)
1. **Switch to Tab 3**: [`http://localhost:3000`](http://localhost:3000) (Mission Dashboard).
2. **Point out**: Show the multi-agent testing cards, the 99.8% latency drop, and the updated Repository Case Memory store.
3. **Closing Line**:
   > *"That is ActionShield on TrueForge: Deep sandbox testing before code can hurt production, autonomous branch creation, and continuous repository learning with developers always in control. Thank you, judges!"*

---

## 🛠️ Fast Troubleshooting & Terminal Commands

### Check Status of all Services:
```powershell
# 1. Check Demo App (port 8000)
curl http://localhost:8000/health

# 2. Check ActionShield MCP Server (port 8791)
curl http://localhost:8791/health

# 3. Check Dashboard (port 3000)
curl http://localhost:3000/

# 4. Check TrueForge (port 8790)
curl http://localhost:8790/api/v1/health
```
