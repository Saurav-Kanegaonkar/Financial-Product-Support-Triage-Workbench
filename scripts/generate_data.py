from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "analysis" / "outputs"
IMAGES = ROOT / "docs" / "images"
RNG = random.Random(42)

APPLICATIONS = [
    "Advisor Portal",
    "Trade Support",
    "Public Finance CRM",
    "Client Reporting",
    "Compliance Workflow",
    "Data Entitlements",
]
USER_GROUPS = [
    "Operations",
    "Financial Advisors",
    "Public Finance",
    "Compliance",
    "Sales Support",
]
SEVERITY_WEIGHT = {"P1": 40, "P2": 28, "P3": 14, "P4": 6}


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def generate_support_issues() -> list[dict]:
    rows = []
    today = date(2026, 7, 18)
    for i in range(1, 1101):
        severity = RNG.choices(["P1", "P2", "P3", "P4"], weights=[5, 20, 50, 25])[0]
        sla_hours = {"P1": 8, "P2": 24, "P3": 72, "P4": 168}[severity]
        hours_open = max(2, int(RNG.gammavariate(2.2, 28)))
        opened = today - timedelta(hours=hours_open)
        rows.append(
            {
                "issue_id": f"HTS-{i:04d}",
                "application": RNG.choice(APPLICATIONS),
                "opened_date": opened.isoformat(),
                "status": RNG.choices(["Open", "In Progress", "Vendor Pending", "Testing", "Closed"], weights=[25, 30, 12, 18, 15])[0],
                "severity": severity,
                "channel": RNG.choices(["Service Center", "User Group", "Email", "Vendor", "Release Testing"], weights=[55, 15, 10, 8, 12])[0],
                "user_group": RNG.choice(USER_GROUPS),
                "sla_hours": sla_hours,
                "hours_open": hours_open,
                "recurrence_count": RNG.choices([0, 1, 2, 3, 4, 5], weights=[42, 26, 15, 9, 5, 3])[0],
                "affected_users": RNG.randint(3, 180),
                "customer_effort_score": round(RNG.uniform(2.1, 6.8), 1),
                "vendor_blocked": RNG.choices([0, 1], weights=[78, 22])[0],
                "release_id": f"REL-{RNG.randint(1, 8):02d}",
            }
        )
    return rows


def generate_requirements(issues: list[dict]) -> list[dict]:
    rows = []
    for i in range(1, 121):
        source_count = RNG.randint(2, 18)
        rows.append(
            {
                "requirement_id": f"REQ-{i:03d}",
                "application": RNG.choice(APPLICATIONS),
                "source_issue_count": source_count,
                "priority": RNG.choices(["Critical", "High", "Medium", "Low"], weights=[10, 30, 45, 15])[0],
                "business_owner": RNG.choice(USER_GROUPS),
                "acceptance_criteria_count": RNG.randint(3, 9),
                "planned_increment": f"Increment {RNG.randint(1, 4)}",
            }
        )
    return rows


def generate_tests() -> list[dict]:
    rows = []
    for i in range(1, 181):
        pass_rate = round(RNG.uniform(0.72, 0.99), 3)
        open_defects = max(0, int((1 - pass_rate) * RNG.randint(8, 35)))
        rows.append(
            {
                "test_request_id": f"TEST-{i:03d}",
                "release_id": f"REL-{RNG.randint(1, 8):02d}",
                "application": RNG.choice(APPLICATIONS),
                "test_type": RNG.choice(["UAT", "Regression", "Vendor Validation", "Data Validation"]),
                "pass_rate": pass_rate,
                "open_defects": open_defects,
                "ready_for_release": 1 if pass_rate >= 0.9 and open_defects <= 2 else 0,
            }
        )
    return rows


def generate_user_groups() -> list[dict]:
    pain_points = ["SLA visibility", "Report accuracy", "Vendor turnaround", "Access defects", "Release communication"]
    return [
        {
            "user_group": group,
            "meeting_frequency": RNG.choice(["Weekly", "Biweekly", "Monthly"]),
            "active_members": RNG.randint(18, 95),
            "top_pain_point": RNG.choice(pain_points),
            "sharepoint_updates_last_30d": RNG.randint(3, 16),
        }
        for group in USER_GROUPS
    ]


def generate_vendors() -> list[dict]:
    rows = []
    dependency_types = ["Data Feed", "API", "Defect Fix", "Access", "Release Signoff"]
    for i in range(1, 13):
        app = APPLICATIONS[(i - 1) % len(APPLICATIONS)]
        rows.append(
            {
                "vendor_id": f"VEND-{i:02d}",
                "application": app,
                "dependency_type": dependency_types[(i - 1) % len(dependency_types)],
                "avg_turnaround_hours": RNG.randint(18, 160),
                "open_items": RNG.randint(1, 14),
                "risk_level": RNG.choices(["Low", "Medium", "High", "Critical"], weights=[20, 35, 32, 13])[0],
            }
        )
    return rows


def score_issue(row: dict) -> float:
    sla_ratio = float(row["hours_open"]) / float(row["sla_hours"])
    score = SEVERITY_WEIGHT[row["severity"]]
    score += min(35, sla_ratio * 12)
    score += int(row["recurrence_count"]) * 4
    score += min(18, int(row["affected_users"]) / 10)
    score += float(row["customer_effort_score"]) * 3
    score += 10 if int(row["vendor_blocked"]) else 0
    return round(score, 2)


def write_outputs(issues: list[dict], tests: list[dict]) -> None:
    ranked = []
    for issue in issues:
        scored = dict(issue)
        scored["triage_score"] = score_issue(issue)
        scored["sla_breached"] = 1 if int(issue["hours_open"]) > int(issue["sla_hours"]) else 0
        ranked.append(scored)
    ranked.sort(key=lambda row: row["triage_score"], reverse=True)
    write_csv(OUT / "ranked_issue_queue.csv", ranked)
    write_csv(OUT / "top_25_upgrade_blockers.csv", ranked[:25])

    by_release: dict[str, list[dict]] = {}
    for test in tests:
        by_release.setdefault(test["release_id"], []).append(test)
    release_rows = []
    for release_id, release_tests in sorted(by_release.items()):
        release_rows.append(
            {
                "release_id": release_id,
                "test_requests": len(release_tests),
                "avg_pass_rate": round(sum(float(t["pass_rate"]) for t in release_tests) / len(release_tests), 3),
                "open_defects": sum(int(t["open_defects"]) for t in release_tests),
                "not_ready_tests": sum(1 for t in release_tests if int(t["ready_for_release"]) == 0),
            }
        )
    write_csv(OUT / "release_readiness_summary.csv", release_rows)

    open_issues = [row for row in issues if row["status"] != "Closed"]
    kpis = [
        {"metric": "issue_count", "value": len(issues)},
        {"metric": "open_issue_count", "value": len(open_issues)},
        {"metric": "sla_breach_rate", "value": round(sum(1 for row in open_issues if int(row["hours_open"]) > int(row["sla_hours"])) / len(open_issues), 3)},
        {"metric": "avg_hours_open", "value": round(sum(int(row["hours_open"]) for row in open_issues) / len(open_issues), 1)},
        {"metric": "vendor_blocked_share", "value": round(sum(int(row["vendor_blocked"]) for row in open_issues) / len(open_issues), 3)},
        {"metric": "avg_customer_effort_score", "value": round(sum(float(row["customer_effort_score"]) for row in open_issues) / len(open_issues), 2)},
    ]
    write_csv(OUT / "kpi_snapshot.csv", kpis)


def write_evidence_images() -> None:
    IMAGES.mkdir(parents=True, exist_ok=True)
    issues = pd.read_csv(OUT / "ranked_issue_queue.csv")
    releases = pd.read_csv(OUT / "release_readiness_summary.csv")
    top_blockers = pd.read_csv(OUT / "top_25_upgrade_blockers.csv")

    app_summary = (
        issues.groupby("application")
        .agg(
            avg_triage_score=("triage_score", "mean"),
            sla_breach_rate=("sla_breached", "mean"),
            issue_count=("issue_id", "count"),
        )
        .sort_values("avg_triage_score", ascending=True)
    )

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#315c74" if value < app_summary["avg_triage_score"].max() else "#b04a35" for value in app_summary["avg_triage_score"]]
    app_summary["avg_triage_score"].plot(kind="barh", ax=ax, color=colors)
    ax.set_title("Average Triage Score by Supported Application", fontsize=15, weight="bold")
    ax.set_xlabel("Average triage score")
    ax.set_ylabel("")
    for index, value in enumerate(app_summary["avg_triage_score"]):
        ax.text(value + 0.6, index, f"{value:.1f}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(IMAGES / "triage-score-by-application.png", dpi=180)
    plt.close(fig)

    heatmap_data = releases.set_index("release_id")[["avg_pass_rate", "open_defects", "not_ready_tests"]]
    normalized = heatmap_data.copy()
    normalized["open_defects"] = normalized["open_defects"] / max(1, normalized["open_defects"].max())
    normalized["not_ready_tests"] = normalized["not_ready_tests"] / max(1, normalized["not_ready_tests"].max())

    fig, ax = plt.subplots(figsize=(9, 5))
    image = ax.imshow(normalized, cmap="YlOrRd", aspect="auto")
    ax.set_title("Release Readiness Risk Matrix", fontsize=15, weight="bold")
    ax.set_xticks(range(len(normalized.columns)), ["Pass rate", "Open defects", "Tests not ready"])
    ax.set_yticks(range(len(normalized.index)), normalized.index)
    for row in range(len(heatmap_data.index)):
        for col, column in enumerate(heatmap_data.columns):
            value = heatmap_data.iloc[row, col]
            label = f"{value:.3f}" if column == "avg_pass_rate" else str(int(value))
            ax.text(col, row, label, ha="center", va="center", color="#222", fontsize=9)
    fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(IMAGES / "release-readiness-risk-matrix.png", dpi=180)
    plt.close(fig)

    table_cols = ["issue_id", "application", "severity", "status", "triage_score", "sla_breached"]
    table_data = top_blockers[table_cols].head(10)
    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.axis("off")
    table = ax.table(
        cellText=table_data.values,
        colLabels=["Issue", "Application", "Severity", "Status", "Score", "SLA"],
        loc="center",
        cellLoc="left",
        colLoc="left",
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.45)
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight="bold", color="white")
            cell.set_facecolor("#315c74")
        elif row % 2 == 0:
            cell.set_facecolor("#f2f5f7")
    ax.set_title("Top Upgrade Blockers for Release Review", fontsize=15, weight="bold", pad=16)
    fig.tight_layout()
    fig.savefig(IMAGES / "top-upgrade-blockers.png", dpi=180)
    plt.close(fig)


def main() -> None:
    issues = generate_support_issues()
    requirements = generate_requirements(issues)
    tests = generate_tests()
    user_groups = generate_user_groups()
    vendors = generate_vendors()

    write_csv(DATA / "support_issues.csv", issues)
    write_csv(DATA / "product_requirements.csv", requirements)
    write_csv(DATA / "test_requests.csv", tests)
    write_csv(DATA / "user_groups.csv", user_groups)
    write_csv(DATA / "vendor_dependencies.csv", vendors)
    write_outputs(issues, tests)
    write_evidence_images()


if __name__ == "__main__":
    main()
