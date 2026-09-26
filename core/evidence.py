import time
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class TelemetrySnapshot(BaseModel):
    p50_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    db_query_ms: float = 0.0
    error_rate: float = 0.0
    throughput_rps: float = 0.0
    total_requests: int = 0

class ReviewerVerdict(BaseModel):
    reviewer: str # "Performance", "Reliability/DB", "Red Team"
    status: str # "PASS" or "FAIL"
    score: int # 1 to 10
    findings: List[str]
    concerns: List[str]
    reasoning: str

class EvidenceObject(BaseModel):
    execution_id: str = Field(default_factory=lambda: f"exec_{str(uuid.uuid4())[:8]}")
    timestamp: str = Field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    attempt_number: int = 1
    git_branch: str = "main"
    git_commit: Optional[str] = None
    git_diff: str = ""
    modified_files: List[str] = Field(default_factory=list)
    before_metrics: TelemetrySnapshot
    after_metrics: TelemetrySnapshot
    tests_status: Dict[str, str] = Field(default_factory=lambda: {"unit": "pass", "integration": "pass"})
    reviewers: List[ReviewerVerdict] = Field(default_factory=list)
    policy_evaluation: Dict[str, Any] = Field(default_factory=dict)
    status: str = "pending" # "passed", "failed", "pending"

    def calculate_improvement(self) -> Dict[str, Any]:
        before_p95 = self.before_metrics.p95_latency_ms
        after_p95 = self.after_metrics.p95_latency_ms
        improvement_pct = 0.0
        if before_p95 > 0:
            improvement_pct = round(((before_p95 - after_p95) / before_p95) * 100, 2)

        return {
            "p95_latency_before_ms": before_p95,
            "p95_latency_after_ms": after_p95,
            "p95_improvement_pct": improvement_pct,
            "db_query_before_ms": self.before_metrics.db_query_ms,
            "db_query_after_ms": self.after_metrics.db_query_ms,
            "error_rate_before": self.before_metrics.error_rate,
            "error_rate_after": self.after_metrics.error_rate
        }
