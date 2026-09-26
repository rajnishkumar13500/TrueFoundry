# 🎬 ActionShield 3-Minute Demo Video Script

**Target Duration**: 2 minutes 45 seconds (Safe margin under the 3:00 minute limit)  
**Speaking Pace**: Moderate (~130 words per minute, clear and confident)  
**Tabs Prepared Before Recording**:
1. **Tab 1**: Target Orders App — [`http://localhost:8000`](http://localhost:8000)
2. **Tab 2**: TrueForge Agent Studio — [`http://localhost:8790`](http://localhost:8790)
3. **Tab 3**: ActionShield Mission Dashboard — [`http://localhost:3000`](http://localhost:3000)
4. **Tab 4**: GitHub Repository — [`https://github.com/rajnishkumar13500/trufoundary-demo`](https://github.com/rajnishkumar13500/trufoundary-demo)

---

## ⏱️ Video Timeline Summary

| Timestamp | Section | Key Screen Action |
| :--- | :--- | :--- |
| **00:00 - 00:35** (35s) | **Act 1: The Blindspot in CI/CD** | Show slow query on `:8000` (2,340 ms). |
| **00:35 - 01:20** (45s) | **Act 2: Phase 1 — Deep Sandbox Testing** | Trigger TrueForge `:8790`. Agent seeds 50k orders & profiles query plan. |
| **01:20 - 02:10** (50s) | **Act 3: Phase 2 — GitOps Branch & Sandbox Fix** | Red Team catches lock ➔ adapts to CONCURRENTLY ➔ latency drops to 0.29ms. |
| **02:10 - 02:45** (35s) | **Act 4: Developer Handover & Continuous Learning** | Show GitHub branch `fix/orders-index-optimization`, Dashboard `:3000`, & wrap up. |

---

## 🎙️ Scene-by-Scene Recording Script

### 🎬 ACT 1: The Blindspot in CI/CD (00:00 – 00:35)

**On Screen**: Switch to Tab 1 ([`http://localhost:8000`](http://localhost:8000)). Click the button **`⚡ Run Orders Query (user_id=1)`**. Watch the spinner run for over 2 seconds before showing the high latency counter.

> **Voiceover (Narrator)**:  
> *"When developers or AI agents push code changes, standard CI/CD runs unit tests with a handful of rows in memory. Everything turns green, and it gets approved.*  
>  
> *But in production with fifty thousand customer orders—disaster strikes. As you see here on our live orders service, querying orders for user #1 takes over 2.3 seconds because of a sequential table scan under load.*  
>  
> *Standard CI cannot test how code actually runs in real runtime. That is why we built ActionShield on TrueForge."*

---

### 🎬 ACT 2: Phase 1 — Deep Sandbox Testing & Issue Summary (00:35 – 01:20)

**On Screen**: Switch to Tab 2 ([`http://localhost:8790`](http://localhost:8790) — TrueForge). Select `actionshield-agent` and send the pre-flight prompt:  
`Run deep pre-flight testing on https://github.com/rajnishkumar13500/trufoundary-demo.git. Seed the sandbox with 50,000 orders and report what you find.`

Point cursor to the tool calls streaming in real time.

> **Voiceover (Narrator)**:  
> *"ActionShield acts as an autonomous pre-flight testing gatekeeper. Notice it does not touch production.*  
>  
> *Instead, it spins up an isolated Daytona sandbox replica, seeds it with 50,000 realistic orders in less than a second, and profiles the query execution plan.*  
>  
> *It identifies the exact bottleneck: an unindexed table scan sorted by created_at descending, reproducing a p95 latency of 2,340 milliseconds.*  
>  
> *It stops and presents the developer with an empirical issue summary—pointing to the exact file and query—asking if we want it to test a fix on a dedicated branch."*

---

### 🎬 ACT 3: Phase 2 — GitOps Branching & Adaptive Verification (01:20 – 02:10)

**On Screen**: Reply in TrueForge:  
`Yes, please create the branch fix/orders-index-optimization and test the fix in the sandbox.`

Watch the agent create the branch, trigger the Red Team reviewer, adapt the SQL, and re-benchmark in the sandbox.

> **Voiceover (Narrator)**:  
> *"We authorize the branch creation. Now watch the 'Aha!' moment of ActionShield.*  
>  
> *In Attempt 1, the agent tests a standard CREATE INDEX migration. Our Red Team reviewer immediately flags a critical hazard: a plain index acquires an exclusive table lock, blocking customer checkouts!*  
>  
> *ActionShield does not fail or guess. It adaptively replans—rewriting the migration to use CREATE INDEX CONCURRENTLY and adding an automated rollback script.*  
>  
> *It re-benchmarks inside the sandbox: the query plan flips to an Index Scan, and latency drops from 2,340 milliseconds down to 0.29 milliseconds—a 99.9% improvement with zero table locks!"*

---

### 🎬 ACT 4: Developer Handover & Continuous Learning (02:10 – 02:45)

**On Screen**:  
1. Switch to Tab 4 ([GitHub Repository](https://github.com/rajnishkumar13500/trufoundary-demo/tree/fix/orders-index-optimization)): Show branch `fix/orders-index-optimization`. Point out `main` is untouched.  
2. Switch to Tab 3 ([`http://localhost:3000`](http://localhost:3000) — Mission Dashboard): Show the live telemetry drop and Repository Memory card.

> **Voiceover (Narrator)**:  
> *"Notice our GitOps safety guarantee: ActionShield never forces code into main. It pushes a dedicated branch to GitHub with the full evidence package, allowing developers to review and merge manually.*  
>  
> *Finally, it stores this verified trajectory in Repository Case Memory. The next time anyone commits a query to this repository, ActionShield recalls this lesson in milliseconds.*  
>  
> *That is ActionShield on TrueForge: Deep sandbox testing, adaptive self-healing, and continuous repository learning. Thank you!"*

---

## 💡 Quick Tips for Recording

1. **Screen Resolution**: Record in 1080p (1920x1080) for sharp text.
2. **Mouse Movements**: Keep mouse movements smooth. Use cursor hovers to guide the viewer's eyes to latency numbers and tool logs.
3. **Pacing Check**:
   - End of Act 1 by **0:35**
   - End of Act 2 by **1:20**
   - End of Act 3 by **2:10**
   - Wrap up cleanly before **2:45**
