import json
import os
import uuid
import datetime
from typing import List, Dict, Any, Optional

MEMORY_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "case_memory.json")

class CaseMemoryStore:
    def __init__(self, storage_path: str = MEMORY_FILE_PATH):
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            initial_cases = [
                {
                    "case_id": "case_001_legacy_orders_slowdown",
                    "repo_id": "trufoundary-demo",
                    "incident": "Orders API high latency on user order listing",
                    "service": "orders-api",
                    "endpoint": "GET /orders",
                    "symptoms": [
                        "p95 latency > 2000ms",
                        "high DB query latency",
                        "orders table sequential scan",
                        "ordering by created_at DESC slow"
                    ],
                    "root_cause": "Missing composite index on orders(user_id, created_at DESC)",
                    "successful_plan": "Apply migration creating composite index idx_orders_user_created ON orders(user_id, created_at DESC)",
                    "rollback_strategy": "DROP INDEX IF EXISTS idx_orders_user_created",
                    "evidence_summary": {
                        "before_p95_ms": 2340.0,
                        "after_p95_ms": 0.054,
                        "improvement_percentage": 99.8
                    },
                    "final_status": "validated",
                    "created_at": "2026-09-01T10:00:00Z"
                }
            ]
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(initial_cases, f, indent=2)

    def search_cases(self, query_terms: List[str], repo_id: Optional[str] = None, service: Optional[str] = None) -> List[Dict[str, Any]]:
        with open(self.storage_path, "r", encoding="utf-8") as f:
            cases = json.load(f)

        results = []
        lowered_terms = [t.lower() for t in query_terms]

        for c in cases:
            if repo_id and c.get("repo_id") and c.get("repo_id") != repo_id:
                # Still include if matches, but give bonus if same repo
                pass
            if service and c.get("service") and c.get("service") != service:
                continue

            score = 0
            # Check repo match bonus
            if repo_id and c.get("repo_id") == repo_id:
                score += 5

            symptoms_text = " ".join(c.get("symptoms", [])).lower()
            incident_text = c.get("incident", "").lower()
            endpoint_text = c.get("endpoint", "").lower()
            root_cause_text = c.get("root_cause", "").lower()

            for term in lowered_terms:
                if term in symptoms_text:
                    score += 3
                if term in incident_text:
                    score += 2
                if term in root_cause_text:
                    score += 2
                if term in endpoint_text:
                    score += 1

            if score > 0:
                results.append((score, c))

        results.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in results]

    def get_repo_cases(self, repo_id: str) -> List[Dict[str, Any]]:
        with open(self.storage_path, "r", encoding="utf-8") as f:
            cases = json.load(f)
        return [c for c in cases if c.get("repo_id") == repo_id]

    def store_case(self, case_data: Dict[str, Any]) -> str:
        case_id = case_data.get("case_id") or f"case_{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M%S')}_{str(uuid.uuid4())[:4]}"
        case_data["case_id"] = case_id
        case_data["created_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        if "repo_id" not in case_data:
            case_data["repo_id"] = "trufoundary-demo"

        with open(self.storage_path, "r", encoding="utf-8") as f:
            cases = json.load(f)

        cases.append(case_data)

        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(cases, f, indent=2)

        return case_id

case_memory = CaseMemoryStore()
