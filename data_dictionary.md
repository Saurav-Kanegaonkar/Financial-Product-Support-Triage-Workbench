# Data Dictionary

## `data/support_issues.csv`

One row per open or recently closed application issue.

- `issue_id`: Stable issue key.
- `application`: Supported financial application area.
- `opened_date`: Date issue entered the queue.
- `status`: Current state.
- `severity`: Business severity from P1 to P4.
- `channel`: Intake source, including Service Center.
- `user_group`: Primary affected user population.
- `sla_hours`: Target resolution hours.
- `hours_open`: Current or final age of the issue.
- `recurrence_count`: Prior related issues in the lookback window.
- `affected_users`: Estimated affected user count.
- `customer_effort_score`: Synthetic 1-7 effort score.
- `vendor_blocked`: Whether a vendor action is required.
- `release_id`: Related release or upgrade.

## `data/product_requirements.csv`

One row per requirement derived from grouped issues.

- `requirement_id`: Requirement key.
- `source_issue_count`: Number of issues mapped into the requirement.
- `priority`: Product priority tier.
- `business_owner`: Owning department.
- `acceptance_criteria_count`: Count of acceptance criteria.
- `planned_increment`: Incremental rollout milestone.

## `data/test_requests.csv`

One row per release test request.

- `test_request_id`: Test request key.
- `release_id`: Release being validated.
- `application`: Application under test.
- `test_type`: UAT, regression, vendor validation, or data validation.
- `pass_rate`: Synthetic pass rate.
- `open_defects`: Remaining defects.
- `ready_for_release`: Boolean readiness flag.

## `data/user_groups.csv`

One row per recurring user group.

- `user_group`: User population.
- `meeting_frequency`: Expected forum cadence.
- `active_members`: Group size.
- `top_pain_point`: Most common issue theme.
- `sharepoint_updates_last_30d`: Communication updates in the last 30 days.

## `data/vendor_dependencies.csv`

One row per vendor dependency.

- `vendor_id`: Vendor key.
- `application`: Related application.
- `dependency_type`: Data feed, API, defect fix, access, or release signoff.
- `avg_turnaround_hours`: Vendor turnaround time.
- `open_items`: Open dependency count.
- `risk_level`: Dependency risk label.
