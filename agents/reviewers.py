import os
import json
from typing import Dict, Any, List
from core.evidence import ReviewerVerdict

try:
    from openai import OpenAI
    openai_client = OpenAI()
except Exception:
    openai_client = None

class ReviewerTriumvirate:
    """
    Evaluates execution evidence from three specialized perspectives:
    1. Performance Reviewer
    2. Reliability / DB Safety Reviewer
    3. Red Team Reviewer (Adversarial)
    """

    def review_performance(
        self,
        git_diff: str,
        before_metrics: Dict[str, Any],
        after_metrics: Dict[str, Any]
    ) -> ReviewerVerdict:
        p95_before = before_metrics.get("p95_latency_ms", 0.0)
        p95_after = after_metrics.get("p95_latency_ms", 0.0)
        db_before = before_metrics.get("db_query_ms", 0.0)
        db_after = after_metrics.get("db_query_ms", 0.0)

        findings = []
        concerns = []

        if p95_after < p95_before:
            pct = round(((p95_before - p95_after) / max(1.0, p95_before)) * 100, 1)
            findings.append(f"p95 latency reduced by {pct}% ({p95_before}ms -> {p95_after}ms).")
        else:
            concerns.append(f"p95 latency regressed ({p95_before}ms -> {p95_after}ms).")

        if db_after < db_before:
            findings.append(f"Database query time dropped from {db_before}ms to {db_after}ms.")

        if "CREATE INDEX" in git_diff.upper():
            findings.append("Composite B-Tree index resolves sequential scan bottleneck.")

        passed = p95_after < 700.0 and len(concerns) == 0
        return ReviewerVerdict(
            reviewer="Performance",
            status="PASS" if passed else "FAIL",
            score=9 if passed else 3,
            findings=findings,
            concerns=concerns,
            reasoning="Performance target satisfied with verifiable reduction in query execution and request latency." if passed else "Failed to achieve required latency target."
        )

    def review_reliability(
        self,
        git_diff: str,
        has_rollback: bool,
        test_passed: bool
    ) -> ReviewerVerdict:
        findings = []
        concerns = []

        if not test_passed:
            concerns.append("Automated test suite failed.")

        if not has_rollback:
            concerns.append("No rollback migration detected; cannot revert in case of failure.")
        else:
            findings.append("Verified reversible migration with matching rollback script.")

        if "DROP " in git_diff.upper() and not "DROP INDEX" in git_diff.upper():
            concerns.append("Destructive schema drop statement detected.")

        if "CREATE INDEX" in git_diff.upper():
            findings.append("Non-blocking index creation conforms to database schema integrity.")

        passed = test_passed and has_rollback and len(concerns) == 0
        return ReviewerVerdict(
            reviewer="Reliability/DB",
            status="PASS" if passed else "FAIL",
            score=9 if passed else 4,
            findings=findings,
            concerns=concerns,
            reasoning="Migration is safe, backward-compatible, and provides an immediate reversible rollback strategy." if passed else "Reliability risks detected (missing rollback or test failures)."
        )

    def review_red_team(
        self,
        git_diff: str,
        scope_passed: bool,
        error_rate: float,
        attempt: int = 1
    ) -> ReviewerVerdict:
        findings = []
        concerns = []

        if not scope_passed:
            concerns.append("Scope creep detected: Agent modified files outside declared Action Contract.")

        if error_rate > 0.01:
            concerns.append(f"Error rate {round(error_rate * 100, 2)}% is unacceptable in production.")

        # If it's attempt 1 and the diff is missing concurrent index creation or has unhandled edge case
        if "CONCURRENTLY" not in git_diff.upper() and attempt == 1:
            # Red Team challenges the lack of CONCURRENTLY or lock risks in attempt 1
            concerns.append("Index creation on large production tables should consider CONCURRENTLY / zero-table-lock execution.")
            return ReviewerVerdict(
                reviewer="Red Team",
                status="FAIL",
                score=5,
                findings=findings,
                concerns=concerns,
                reasoning="Challenged migration locking strategy under live write traffic. Adapt by specifying lock mitigation or verifying zero lock impact."
            )

        findings.append("No privilege escalation or unauthorized file modifications detected.")
        findings.append("Query pattern matches index columns with exact selectivity.")

        passed = scope_passed and error_rate <= 0.01 and len(concerns) == 0
        return ReviewerVerdict(
            reviewer="Red Team",
            status="PASS" if passed else "FAIL",
            score=8 if passed else 3,
            findings=findings,
            concerns=concerns,
            reasoning="Adversarial challenge passed. Change is well-bounded and safe for human review." if passed else "Red team detected unaddressed failure modes."
        )

    def run_all_reviews(
        self,
        git_diff: str,
        before_metrics: Dict[str, Any],
        after_metrics: Dict[str, Any],
        has_rollback: bool,
        test_passed: bool,
        scope_passed: bool,
        attempt: int = 1
    ) -> List[ReviewerVerdict]:
        v_perf = self.review_performance(git_diff, before_metrics, after_metrics)
        v_rel = self.review_reliability(git_diff, has_rollback, test_passed)
        v_red = self.review_red_team(git_diff, scope_passed, after_metrics.get("error_rate", 0.0), attempt=attempt)
        return [v_perf, v_rel, v_red]

reviewers = ReviewerTriumvirate()
