from typing import List, Optional
from pydantic import BaseModel, Field

class ActionContract(BaseModel):
    goal: str = Field(..., description="High-level engineering objective")
    proposed_change: str = Field(..., description="Summary of the proposed code or schema modification")
    allowed_scope: List[str] = Field(
        default_factory=list,
        description="List of file paths or glob patterns permitted to be modified"
    )
    constraints: List[str] = Field(
        default_factory=lambda: [
            "No data loss",
            "Tests must pass",
            "Error rate < 1%",
            "No unrelated file changes",
            "Migration must be reversible"
        ],
        description="Hard engineering invariants"
    )
    success_criteria: List[str] = Field(
        default_factory=lambda: [
            "p95 latency < 700ms",
            "tests pass",
            "error rate < 1%",
            "database remains healthy",
            "scope matches declared change"
        ],
        description="Measurable success metrics"
    )
    rollback_strategy: str = Field(
        ...,
        description="Explicit, reversible procedure if the change fails or causes regressions"
    )

    def validate_scope(self, modified_files: List[str]) -> bool:
        """Check if all modified files fall within declared allowed_scope"""
        if not self.allowed_scope:
            return False
        for f in modified_files:
            # Normalize path separators
            norm_f = f.replace("\\", "/").strip("./")
            matched = any(
                norm_f == s.replace("\\", "/").strip("./") or norm_f.startswith(s.replace("\\", "/").strip("./"))
                for s in self.allowed_scope
            )
            if not matched:
                return False
        return True
