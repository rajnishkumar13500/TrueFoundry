# 🛡️ ActionShield — Hackathon Jury Demo Guide & UI Verification

### 🎯 The Core Mission ("The Moto")
ActionShield is **NOT just a blind auto-fix bot**. Its core mission is **Deep In-Depth Empirical Testing of Commits/PRs in Closed Sandbox Environments**:
- **The Blindspot in Standard CI**: When an engineer or AI agent commits new code or alters SQL, unit tests pass because the syntax is valid. But unit tests test with 5 rows in memory. They **never catch** full table scans on 50,000 rows, latency explosions (2,340ms), or table-locking DDL hazards (`ACCESS EXCLUSIVE` locks).
- **Phase 1 (Deep Sandbox Pre-Flight Gate)**: ActionShield automatically takes the newly committed code into an isolated Daytona Sandbox container, runs realistic high-volume benchmarks, profiles query execution plans (`EXPLAIN ANALYZE`), runs Red Team adversarial scans, and reports the exact empirical findings to the engineer.
- **Phase 2 (Autonomous Closed-Loop Remediation)**: If the engineer asks ActionShield to resolve the issue, the agent synthesizes an adapted, non-blocking fix inside the sandbox, proves a 99.8% improvement, generates a rollback script, and pauses at the TrueForge Human Checkpoint for operator authorization before anything touches production!

---

## 🖥️ Live Service Surfaces & URLs

Before starting your presentation, ensure these 3 browser tabs are open:

| Service | URL | Purpose in Demo |
| :--- | :--- | :--- |
| **Demo eCommerce App** | [`http://localhost:8000`](http://localhost:8000) | Live target application. Shows orders and has an interactive button to test live latency before & after. |
| **TrueForge Agent Studio** | [`http://localhost:8790`](http://localhost:8790) | The core hackathon agent runtime. Where OpenAI GPT-5.5 reasons, calls MCP tools, reports diagnostic metrics, and enforces Human Approval checkpoints. |
| **ActionShield Mission Dashboard** | [`http://localhost:3000`](http://localhost:3000) | Visual mission control showing the 2-phase architecture, live metrics comparison, reviewer verdicts, and Case Memory. |

---

## 🎬 5-Minute Jury Demo Script

Follow these exact steps in front of the jury:

### Step 1: Hook the Jury with the Real-World Problem (45 Seconds)
1. **Open Tab 1**: [`http://localhost:8000`](http://localhost:8000) (Demo Orders App).
2. **Action**: Click the button `⚡ Run Orders Query (user_id=1)`.
3. **What happens**: The query takes time, and the latency counter displays high latency (> 2,000ms).
4. **What to say**:
   > *"Good morning judges. Consider what happens when an engineer or AI agent pushes a commit that adds a new query or modifies SQL in production. Standard CI runs unit tests with a handful of rows, says 'All Tests Passed', and merges it.*
   > *Then production crashes because the query does a full sequential table scan on 50,000 orders, taking over 2 seconds per request. Unit tests cannot test how code ACTUALLY behaves in real runtime under load. That is why we built ActionShield on TrueForge."*

---

### Step 2: Trigger Phase 1 — Deep Sandbox Testing of the Commit (1 Minute)
1. **Open Tab 2**: [`http://localhost:8790`](http://localhost:8790) (TrueForge Agent Studio).
2. **Action**: Select the agent `actionshield-agent` and click **New Chat** (or open the prepared demo session).
3. **Prompt to send**:
   ```text
   Validate the latest commit on https://github.com/rajnishkumar13500/trufoundary-demo.git. Run deep in-depth testing in an isolated Daytona sandbox, profile query plans and latency, and report what you find.
   ```
4. **What happens in TrueForge**:
   - The agent calls `create_sandbox_environment` to clone the candidate commit into an isolated Daytona container.
   - The agent calls `benchmark_repository` to stress-test the query under 50,000 orders.
   - The agent calls `profile_query_execution` (`EXPLAIN ANALYZE`) and uncovers the sequential table scan.
   - The agent runs `run_red_team_reviewer` to check for table lock hazards.
   - The agent stops and calls `ask_user_question`, presenting the **Empirical Diagnostic Report**:
     - `p95 Latency: 2,340 ms (Fails < 700ms SLO)`
     - `Query Plan: Full sequential scan on 50,000 rows`
     - `Red Team Flag: Unindexed column under high concurrency`
     - `Prompt: "Would you like me to test a self-healing composite index fix in the sandbox?"`
5. **What to say**:
   > *"Notice our core philosophy: ActionShield is first and foremost a deep pre-flight empirical gatekeeper. In an isolated Daytona sandbox, it evaluated how the committed code actually runs in reality, found the hidden latency explosion and table scan, and reported empirical evidence back to the operator."*

---

### Step 3: Trigger Phase 2 — Autonomous Self-Healing & Adaptive Replanning (1.5 Minutes)
1. **Action**: In TrueForge, reply:
   ```text
   Yes, please test and validate the fix in the sandbox.
   ```
2. **Watch TrueForge Screen**:
   - The agent consults **Case Memory** (`query_case_memory`).
   - **Attempt 1 Fails Safely**: The agent tries a standard `CREATE INDEX`. The Red Team Reviewer flags it:
     ```json
     {
       "passed": false,
       "criticism": "CRITICAL: Standard CREATE INDEX acquires an ACCESS EXCLUSIVE lock on production tables. Must use CREATE INDEX CONCURRENTLY."
     }
     ```
   - **Adaptive Replanning**: ActionShield adapts the SQL to `CREATE INDEX CONCURRENTLY` and generates a reversible rollback migration (`generate_rollback_script`).
   - **Attempt 2 Passes**: Re-benchmarked inside Daytona sandbox:
     - `Old Latency: 2,340 ms`
     - `New Latency: 0.054 ms (99.8% improvement!)`
     - `Reviewers: Performance PASS, Reliability PASS, Red Team PASS`
3. **What to say**:
   > *"Here is the 'Aha!' moment of ActionShield: closed-loop adaptive replanning. In Attempt 1, the agent proposed an index that would lock production tables. Our deterministic Red Team policy engine rejected it. 
   > Instead of failing, the agent learned from the critique, adapted the SQL to run CONCURRENTLY, validated it inside the Daytona sandbox, and verified a 99.8% latency improvement empirically."*

---

### Step 4: TrueForge Human Checkpoint & Production Deployment (45 Seconds)
1. **Watch TrueForge Screen**:
   - TrueForge encounters `apply_production_fix`.
   - Because `apply_production_fix` is marked with `require_approval_for_tools`, TrueForge halts the run and prompts for **Operator Approval**.
2. **Action**: Click **Approve** in the TrueForge UI.
3. **What happens**:
   - The fix is committed and merged to `main` on GitHub.
   - The incident is permanently stored in **Case Memory** (`store_case_memory`) so future incidents resolve in sub-seconds.
4. **What to say**:
   > *"TrueForge's native policy engine guarantees that no consequential production write happens without explicit human sign-off. We approve the fix, and it deploys."*

---

### Step 5: Verify the Result in the Live UI (30 Seconds)
1. **Switch to Tab 1**: [`http://localhost:8000`](http://localhost:8000) (Demo Orders App).
2. **Action**: Click `⚡ Run Orders Query (user_id=1)` again.
3. **Result**: The latency badge immediately flashes **green** (`0.05 ms` to `< 1 ms`), proving the fix is live!
4. **Switch to Tab 3**: [`http://localhost:3000`](http://localhost:3000) (Mission Dashboard).
5. **Point out**: Show the 2-phase visualizer completed, the 99.8% latency drop, and the Case Memory updated.
6. **Closing Line**:
   > *"That is ActionShield on TrueForge: Code is tested deeply in closed sandboxes before it can break production, verified empirically with zero hallucinations, and kept under strict human control. Thank you, judges!"*

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

### Run Automated Headless Verification (Zero UI Demo):
```powershell
cd d:\TrueFoundry
python scripts/test_end_to_end_flow.py
```
