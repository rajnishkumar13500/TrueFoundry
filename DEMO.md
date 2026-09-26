# 🛡️ ActionShield — Hackathon Jury Demo Guide & UI Verification

This document provides:
1. **How UI Updates & Code Changes Reflect** across all components.
2. **A 5-Minute Step-by-Step Jury Presentation Script** (what to click, what to say, and what to highlight).
3. **Cheat Sheet & Fast Recovery Commands**.

---

## 🖥️ Live Service Surfaces & URLs

Before starting your presentation, ensure these 3 browser tabs are open:

| Service | URL | Purpose in Demo |
| :--- | :--- | :--- |
| **Demo eCommerce App** | [`http://localhost:8000`](http://localhost:8000) | Live target application with high-volume orders & intentional slow query. Has an interactive button to test latency before & after. |
| **TrueForge Agent Studio** | [`http://localhost:8790`](http://localhost:8790) | The core hackathon agent runtime. Where OpenAI GPT-5.5 reasons, calls MCP tools, asks questions, and enforces Human Approval checkpoints. |
| **ActionShield Mission Dashboard** | [`http://localhost:3000`](http://localhost:3000) | Visual mission control showing the 7-node autonomous loop (*Remember ➔ Reason ➔ Act ➔ Observe ➔ Critique ➔ Human Approval ➔ Store*). |

---

## 🔍 How to Verify Code Changes & UI Updates

When code is changed (either by the agent or manually), here is how the reflection works:

### 1. In the Demo App (`http://localhost:8000`)
- **Interactive Button**: Click `⚡ Run Orders Query (user_id=1)`.
  - **Before Fix**: Latency is displayed in orange/red (hundreds of milliseconds to seconds, sequential table scan).
  - **After Fix (Index Added)**: Latency badge turns **green** (`< 1 ms`, index scan via `idx_orders_user_created`).
- **Swagger Docs**: Available at [`http://localhost:8000/docs`](http://localhost:8000/docs) to inspect raw `/orders` and `/metrics` JSON.
- **Hot-Reloading**: The FastAPI server runs with hot reload. Any change pushed to `demo-app/app/` takes effect immediately.

### 2. In TrueForge Studio (`http://localhost:8790`)
- **Real-Time Streaming**: TrueForge streams thought tokens, tool invocations, and responses live.
- **Interactive Question**: When the agent calls `ask_user_question`, a modal/dialogue appears asking the operator to confirm before creating the sandbox branch.
- **Human Approval Checkpoint**: When the agent attempts `apply_production_fix`, TrueForge halts execution with `tool.approval_required` and displays an **Approve / Deny** prompt. The action cannot proceed until the human clicks Approve.

### 3. In Daytona Cloud Sandbox
- **Zero Production Risk**: Changes are **not** made directly to production. The agent clones the repository into an isolated Daytona sandbox container, creates a Git branch (`fix/orders-index-optimization`), and runs benchmarks inside the sandbox.
- **Empirical Evidence**: The agent will only proceed if the sandbox tests pass and latency drops by > 80% without table locking.

### 4. In ActionShield Dashboard (`http://localhost:3000`)
- Visualizes the entire incident lifecycle, the Triumvirate Reviewers (Performance, Database Safety, Red Team), and the updated Case Memory entry.

---

## 🎬 5-Minute Jury Demo Script

Follow these exact steps in front of the jury:

### Step 1: Hook the Jury & Show the Problem (45 Seconds)
1. **Open Tab 1**: [`http://localhost:8000`](http://localhost:8000) (Demo Orders App).
2. **Action**: Click the button `⚡ Run Orders Query (user_id=1)`.
3. **What happens**: The query takes time, and the latency counter displays high latency.
4. **What to say**:
   > *"Good morning judges. Most AI coding agents today are hallucination-prone: if you ask an agent to fix production, it might run a destructive DDL migration that locks tables, causes outages, or breaks schemas. 
   > Here is our production eCommerce orders service. As you can see, querying orders for user #1 is slow due to a database bottleneck. Let's see how ActionShield solves this using TrueForge, Daytona sandboxes, and empirical self-validation."*

---

### Step 2: Open TrueForge & Trigger ActionShield (45 Seconds)
1. **Open Tab 2**: [`http://localhost:8790`](http://localhost:8790) (TrueForge Agent Studio).
2. **Action**: Select the agent `actionshield-agent` and click **New Chat** (or open the prepared demo session).
3. **Prompt to send**:
   ```text
   Diagnose the orders query latency in https://github.com/rajnishkumar13500/trufoundary-demo.git, show me the baseline metrics, and ask for my confirmation before creating a sandbox branch.
   ```
4. **What happens**:
   - The agent consults **Case Memory** (`query_case_memory`).
   - The agent runs baseline benchmarks (`benchmark_repository`).
   - The agent stops and calls `ask_user_question`, presenting the baseline metrics:
     - `Baseline p95 Latency: 2,340 ms`
     - `Bottleneck: Sequential table scan on 50,000 orders`
     - `Hypothesis: Composite index required on orders(user_id, created_at DESC)`
5. **What to say**:
   > *"Notice that ActionShield does not blindly execute code. It leverages TrueForge's native human-in-the-loop capabilities to diagnose first, present empirical baseline metrics, and ask for operator consent."*

---

### Step 3: Interactive Confirmation & Daytona Sandbox Creation (1 Minute)
1. **Action**: In TrueForge, reply:
   ```text
   Yes, please create the sandbox branch, test the fix, and run the reviewers.
   ```
2. **What happens**:
   - ActionShield calls `create_sandbox_environment` to provision a clean Daytona sandbox.
   - It creates a dedicated branch: `fix/orders-index-optimization`.
   - It generates the migration fix and runs the **Triumvirate Reviewers**.

---

### Step 4: The 'Aha!' Moment — Adaptive Replanning (1.5 Minutes)
*(This is the key differentiator that will impress the jury!)*

1. **Watch TrueForge Screen**:
   - **Attempt 1 Fails Safely**: The agent tries to apply `CREATE INDEX idx_orders_user_created ON orders(...)`.
   - The **Red Team Reviewer** flags it:
     ```json
     {
       "passed": false,
       "criticism": "CRITICAL: Plain CREATE INDEX takes an ACCESS EXCLUSIVE table lock on production PostgreSQL. Must use CREATE INDEX CONCURRENTLY."
     }
     ```
   - **Adaptive Replanning**: ActionShield **does not crash or hallucinate**. Instead, it ingests the Red Team critique and adapts the migration to use `CREATE INDEX CONCURRENTLY` and generates a reversible rollback migration `002_rollback.sql`.
   - **Attempt 2 Passes**: Re-benchmarked inside Daytona sandbox:
     - `Old Latency: 2,340 ms`
     - `New Latency: 0.054 ms (99.9% improvement!)`
     - `Zero Table Locks, Zero Regressions`
2. **What to say**:
   > *"Here is the 'Aha!' moment of ActionShield: closed-loop adaptive replanning. In Attempt 1, the agent proposed an index that would lock production tables. Our deterministic Red Team policy engine rejected it. 
   > Instead of failing, the agent learned from the critique, adapted the SQL to run CONCURRENTLY, validated it inside the Daytona sandbox, and verified a 99.9% latency improvement empirically."*

---

### Step 5: TrueForge Human Checkpoint & Production Deployment (45 Seconds)
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

### Step 6: Verify the Result in the Live UI (30 Seconds)
1. **Switch to Tab 1**: [`http://localhost:8000`](http://localhost:8000) (Demo Orders App).
2. **Action**: Click `⚡ Run Orders Query (user_id=1)` again.
3. **Result**: The latency badge immediately flashes **green** (`0.05 ms` to `< 1 ms`), proving the fix is live!
4. **Switch to Tab 3**: [`http://localhost:3000`](http://localhost:3000) (Mission Dashboard).
5. **Point out**: Show the 7-node visualizer completed and the Case Memory updated.
6. **Closing Line**:
   > *"That is ActionShield on TrueForge: Memory suggests, Sandboxes verify, Evidence decides, and Humans remain in control. Thank you, judges!"*

---

## 🛠️ Fast Troubleshooting & Terminal Commands

If any service needs to be checked or restarted:

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

### Restart Demo App manually (if needed):
```powershell
cd d:\TrueFoundry\demo-app
python -m uvicorn app.main:app --port 8000 --reload
```

### Run Automated Headless Verification (Zero UI Demo):
```powershell
cd d:\TrueFoundry
python scripts/test_end_to_end_flow.py
```
*(This runs the complete 7-step loop in Python in 15 seconds, printing each reviewer's verdict and the latency reduction.)*
