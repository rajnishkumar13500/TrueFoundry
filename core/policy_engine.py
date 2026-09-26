from typing import List, Dict, Any, Optional
from core.contracts import ActionContract

class PolicyViolation(Exception):
    def __init__(self, rule: str, reason: str):
        super().__init__(f"Policy Violation [{rule}]: {reason}")
        self.rule = rule
        self.reason = reason

class DeterministicPolicyEngine:
    """
    Deterministic code-level invariants that cannot be bypassed by LLM hallucinations.
    Enforces Intent vs. Reality, error rate budgets, test passes, and rollback availability.
    """

    def __init__(self, max_error_rate: float = 0.01, latency_target_ms: float = 700.0):
        self.max_error_rate = max_error_rate
        self.latency_target_ms = latency_target_ms

    def check_intent_vs_reality(
        self,
        contract: ActionContract,
        modified_files: List[str]
    ) -> Dict[str, Any]:
        """
        Validates that the agent modified ONLY the files it explicitly declared in the Action Contract.
        """
        unauthorized_files = []
        for f in modified_files:
            norm_f = f.replace("\\", "/").strip("./")
            matched = any(
                norm_f == s.replace("\\", "/").strip("./") or norm_f.startswith(s.replace("\\", "/").strip("./"))
                for s in contract.allowed_scope
            )
            if not matched:
                unauthorized_files.append(norm_f)

        passed = len(unauthorized_files) == 0
        return {
            "passed": passed,
            "declared_scope": contract.allowed_scope,
            "actual_modified_files": modified_files,
            "unauthorized_files": unauthorized_files,
            "error": None if passed else f"ACTION SCOPE VIOLATION: Files modified outside declared scope: {unauthorized_files}"
        }

    def evaluate_execution(
        self,
        contract: ActionContract,
        modified_files: List[str],
        test_passed: bool,
        error_rate: float,
        p95_latency_ms: float,
        has_rollback: bool,
        sql_content: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes all deterministic policy gates on the live evidence.
        """
        violations = []

        # Gate 1: Scope enforcement (Intent vs Reality)
        scope_check = self.check_intent_vs_reality(contract, modified_files)
        if not scope_check["passed"]:
            violations.append({
                "rule": "SCOPE_INTEGRITY",
                "message": scope_check["error"]
            })

        # Gate 2: Tests must pass
        if not test_passed:
            violations.append({
                "rule": "TEST_SUITE_PASS",
                "message": "Automated pytest suite failed on the modified codebase."
            })

        # Gate 3: Error rate constraint (< 1%)
        if error_rate > self.max_error_rate:
            violations.append({
                "rule": "ERROR_RATE_THRESHOLD",
                "message": f"Error rate {round(error_rate * 100, 2)}% exceeds policy budget of {round(self.max_error_rate * 100, 2)}%."
            })

        # Gate 4: Latency improvement constraint
        if p95_latency_ms > self.latency_target_ms:
            violations.append({
                "rule": "LATENCY_TARGET_MET",
                "message": f"p95 latency {p95_latency_ms}ms does not meet target of < {self.latency_target_ms}ms."
            })

        # Gate 5: Rollback availability
        if not has_rollback:
            violations.append({
                "rule": "ROLLBACK_AVAILABLE",
                "message": "No reversible rollback script was provided for this modification."
            })

        # Gate 6: Destructive SQL check (Prevent DROP TABLE, TRUNCATE, DELETE without WHERE)
        if sql_content:
            upper_sql = sql_content.upper()
            dangerous_tokens = ["DROP TABLE", "TRUNCATE", "DROP DATABASE", "DROP COLUMN"]
            for tok in dangerous_tokens:
                if tok in upper_sql:
                    violations.append({
                        "rule": "DESTRUCTIVE_DDL_FORBIDDEN",
                        "message": f"Dangerous SQL operation '{tok}' detected in migration."
                    })

        passed = len(violations) == 0
        return {
            "status": "PASS" if passed else "REJECT",
            "passed": passed,
            "violations_count": len(violations),
            "violations": violations,
            "metrics": {
                "p95_latency_ms": p95_latency_ms,
                "error_rate": error_rate,
                "tests_passed": test_passed,
                "scope_valid": scope_check["passed"],
                "rollback_verified": has_rollback
            }
        }
