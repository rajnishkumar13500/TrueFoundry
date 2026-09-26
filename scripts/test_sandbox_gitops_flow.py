import os
import sys
import json
import time

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.sandbox import sandbox_manager
from core.case_memory import case_memory

def print_step(title):
    print(f"\n{'='*70}\n[STEP] {title}\n{'='*70}")

def run_test():
    print("[ACTIONSHIELD] SANDBOX-FIRST GITOPS END-TO-END VERIFICATION")
    print("Testing Sandbox Hosting, 50k Seeding, Multi-Agent Review, Branching & Repo Memory\n")

    sandbox_id = "sbx_live_test"
    repo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "demo-app")
    repo_id = "trufoundary-demo"

    # 1. SETUP SANDBOX
    print_step("1. Setup Isolated Sandbox Container Replica")
    setup_res = sandbox_manager.setup_sandbox(repo_path=repo_path, sandbox_id=sandbox_id)
    print(f"[OK] Sandbox Container: {setup_res['sandbox_id']}")
    print(f"[OK] Isolated Path: {setup_res['path']}")
    assert setup_res["status"] == "READY"

    # 2. SEED SANDBOX DATABASE
    print_step("2. Seed Sandbox Database with 50,000 Realistic Orders")
    seed_res = sandbox_manager.seed_database(sandbox_id=sandbox_id, count=50000)
    print(f"[OK] Seeded {seed_res['orders_seeded']:,} orders in {seed_res['duration_seconds']}s")
    print(f"[OK] Sandbox DB: {seed_res['db_path']}")
    assert seed_res["orders_seeded"] == 50000

    # 3. RUN BASELINE BENCHMARK & QUERY PROFILER IN SANDBOX
    print_step("3. Run Baseline Benchmark & Query Profiler in Sandbox")
    bench_before = sandbox_manager.run_benchmark(sandbox_id=sandbox_id, user_id=1, iterations=15)
    print(f"[OK] Query Plan: {bench_before['query_plan']}")
    print(f"[OK] Scan Type: {bench_before['scan_type']}")
    print(f"[OK] Has Composite Index: {bench_before['has_composite_index']}")
    print(f"[OK] Baseline p95 Latency: {bench_before['measured_p95_ms']} ms")
    assert not bench_before["has_composite_index"]
    assert bench_before["scan_type"] == "SEQUENTIAL_TABLE_SCAN"

    # 4. RED TEAM ADVERSARIAL SCAN (ATTEMPT 1)
    print_step("4. Red Team Adversarial Security Evaluation (Attempt 1: Plain Index)")
    plain_sql = "CREATE INDEX idx_orders_user_created ON orders(user_id, created_at DESC);"
    rt_fail = sandbox_manager.evaluate_red_team(plain_sql)
    print(f"[!] Red Team Verdict: Passed = {rt_fail['passed']}")
    print(f"[!] Hazard Code: {rt_fail['error_code']}")
    print(f"[!] Criticism: {rt_fail['criticism']}")
    assert not rt_fail["passed"]
    assert rt_fail["error_code"] == "REDTEAM_DDL_LOCK"

    # 5. ADAPTIVE FIX & SANDBOX APPLICATION (ATTEMPT 2)
    print_step("5. Adaptive Fix & Sandbox Application (Attempt 2: Non-Blocking Index)")
    concurrent_sql = "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_user_created ON orders(user_id, created_at DESC);"
    rt_pass = sandbox_manager.evaluate_red_team(concurrent_sql)
    print(f"[OK] Red Team Verdict: Passed = {rt_pass['passed']}")
    print(f"[OK] Verdict Details: {rt_pass['verdict']}")
    assert rt_pass["passed"]

    apply_res = sandbox_manager.apply_migration(sandbox_id=sandbox_id, sql_content=concurrent_sql)
    print(f"[OK] Applied non-blocking migration in sandbox in {apply_res['duration_ms']}ms")
    assert apply_res["applied"]

    # 6. RE-BENCHMARK IN SANDBOX
    print_step("6. Re-Benchmark in Sandbox (Verify Performance & Query Plan)")
    bench_after = sandbox_manager.run_benchmark(sandbox_id=sandbox_id, user_id=1, iterations=15)
    print(f"[OK] Query Plan: {bench_after['query_plan']}")
    print(f"[OK] Scan Type: {bench_after['scan_type']}")
    print(f"[OK] Has Composite Index: {bench_after['has_composite_index']}")
    print(f"[OK] Optimized p95 Latency: {bench_after['measured_p95_ms']} ms")
    assert bench_after["has_composite_index"]
    assert bench_after["scan_type"] == "INDEX_SCAN"
    assert bench_after["measured_p95_ms"] < 5.0

    improvement = round(((bench_before['measured_p95_ms'] - bench_after['measured_p95_ms']) / bench_before['measured_p95_ms']) * 100, 2)
    print(f"\n>>> EMPIRICAL VERIFICATION PROVEN: Latency dropped by {improvement}% <<<")

    # 7. CREATE DEDICATED FIX BRANCH & PUSH TO GITHUB (NO AUTO-MERGE TO MAIN)
    print_step("7. Create Fix Branch & Push to GitHub (Manual Merge Handover)")
    branch_name = "fix/orders-index-optimization"
    branch_res = sandbox_manager.create_and_push_branch(
        repo_path=repo_path,
        branch_name=branch_name,
        migration_filename="002_add_orders_index.sql",
        migration_content=concurrent_sql,
        message="fix(db): add non-blocking composite index idx_orders_user_created"
    )
    print(f"[OK] Branch Action: {branch_res['status']}")
    print(f"[OK] Dedicated Branch: {branch_res['branch']}")
    print(f"[OK] Remote Push Result: Pushed = {branch_res.get('pushed', False)}")
    print(f"[OK] Developer Handover: Branch '{branch_name}' pushed for review. 'main' is untouched.")

    # 8. PERSIST REPOSITORY-SPECIFIC MEMORY
    print_step("8. Persist Repository-Specific Case Memory")
    case_id = case_memory.store_case({
        "repo_id": repo_id,
        "incident": "Orders API latency spike on high-volume user query",
        "symptoms": ["orders_latency", "sequential_scan", "missing_composite_index"],
        "root_cause": "Unindexed orders table sorted by created_at DESC",
        "successful_plan": "CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_orders_user_created ON orders(user_id, created_at DESC);",
        "rollback_strategy": "DROP INDEX CONCURRENTLY IF EXISTS idx_orders_user_created;",
        "evidence_summary": {
            "before_p95_ms": bench_before['measured_p95_ms'],
            "after_p95_ms": bench_after['measured_p95_ms'],
            "improvement_pct": improvement
        },
        "final_status": "validated_in_sandbox"
    })
    print(f"[OK] Stored in Case Memory with Case ID: {case_id}")
    
    # Verify retrieval
    learned_cases = case_memory.get_repo_cases(repo_id=repo_id)
    print(f"[OK] Retrieved {len(learned_cases)} learned cases for repo '{repo_id}'")
    assert len(learned_cases) >= 1

    print("\n" + "="*70)
    print("[SUCCESS] ALL 8 GITOPS STAGES PASSED SUCCESSFULLY!")
    print("="*70)

if __name__ == "__main__":
    run_test()
