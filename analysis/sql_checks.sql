-- Financial Product Support Triage Workbench SQL checks
-- Tables assumed: support_issues, product_requirements, test_requests, user_groups, vendor_dependencies

-- 1. SLA breach and backlog aging by supported application.
SELECT
  application,
  COUNT(*) AS open_issues,
  SUM(CASE WHEN hours_open > sla_hours THEN 1 ELSE 0 END) AS sla_breaches,
  ROUND(AVG(hours_open), 1) AS avg_hours_open
FROM support_issues
WHERE status <> 'Closed'
GROUP BY application
ORDER BY sla_breaches DESC, avg_hours_open DESC;

-- 2. Defect recurrence by application and severity.
SELECT
  application,
  severity,
  COUNT(*) AS issue_count,
  SUM(recurrence_count) AS recurring_defects
FROM support_issues
GROUP BY application, severity
ORDER BY recurring_defects DESC;

-- 3. Release readiness blockers.
SELECT
  release_id,
  COUNT(*) AS test_requests,
  ROUND(AVG(pass_rate), 3) AS avg_pass_rate,
  SUM(open_defects) AS open_defects,
  SUM(CASE WHEN ready_for_release = 0 THEN 1 ELSE 0 END) AS not_ready_tests
FROM test_requests
GROUP BY release_id
ORDER BY not_ready_tests DESC, open_defects DESC;

-- 4. Vendor dependencies with high turnaround.
SELECT
  application,
  dependency_type,
  open_items,
  avg_turnaround_hours,
  risk_level
FROM vendor_dependencies
WHERE risk_level IN ('High', 'Critical')
ORDER BY avg_turnaround_hours DESC;
