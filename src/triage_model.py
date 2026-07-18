from __future__ import annotations

SEVERITY_WEIGHT = {"P1": 40, "P2": 28, "P3": 14, "P4": 6}


def triage_score(issue: dict) -> float:
    """Score one support issue for product analyst review priority."""
    sla_ratio = float(issue["hours_open"]) / float(issue["sla_hours"])
    score = SEVERITY_WEIGHT[issue["severity"]]
    score += min(35, sla_ratio * 12)
    score += int(issue["recurrence_count"]) * 4
    score += min(18, int(issue["affected_users"]) / 10)
    score += float(issue["customer_effort_score"]) * 3
    score += 10 if int(issue["vendor_blocked"]) else 0
    return round(score, 2)
