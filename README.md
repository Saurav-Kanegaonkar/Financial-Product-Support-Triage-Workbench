# Financial Product Support Triage Workbench

Synthetic but realistic support-operations project for a financial product analyst workflow. The workbench turns open application issues, user groups, vendor dependencies, release test results, and product requirements into a ranked triage queue that a product analyst could review before Service Center updates, upgrade planning, and user-group meetings.

## Why This Exists

Financial product teams need a practical way to decide which application issues should move first when the queue mixes severity, customer effort, stale open items, vendor blockers, and release-readiness risk. This project creates inspectable source-style data and a repeatable ranking script so a reviewer can see how open issues become product decisions.

## What Is Included

- `data/` contains five source-style CSVs: support issues, product requirements, test requests, user groups, and vendor dependencies.
- `scripts/generate_data.py` generates the synthetic operational data deterministically and writes ranked outputs.
- `analysis/sql_checks.sql` contains SQL checks for SLA aging, defect recurrence, release readiness, and vendor blockers.
- `analysis/executive_findings.md` summarizes the product-support recommendations.
- `analysis/outputs/` contains the ranked issue queue, release readiness summary, and KPI snapshot.

## Project Signal For Recruiters

This is intentionally not just a dashboard shell. The artifact proves the core Product Analyst muscle: translate application-support noise into product requirements, testing priorities, user-group communication, and incremental rollout decisions.

## Run

```bash
python3 scripts/generate_data.py
```

The script writes the data tables and analysis outputs using a fixed random seed.

## Resume Bullet

Built financial product support triage workbench scoring 420 synthetic Service Center issues across SLA risk, defect recurrence, and test readiness to prioritize 25 upgrade blockers.
