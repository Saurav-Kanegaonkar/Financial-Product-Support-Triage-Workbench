# Analysis Plan

## Objective

Rank financial product support issues by business urgency and release risk so a Product Analyst can prioritize resolution procedures, Service Center updates, test requests, and scheduled incremental improvements.

## Inputs

- Support issue queue
- Product requirements mapped from recurring issues
- Test requests by release
- User-group communication records
- Vendor dependencies

## Scoring Logic

The triage score uses illustrative review weights, not an automated business rule. It combines:

- SLA breach risk from issue age versus target resolution window
- Severity weighting
- Defect recurrence
- Affected user count
- Customer effort score
- Vendor blocker flag
- Release readiness exposure

The score intentionally gives the largest fixed baseline to severity, caps SLA aging so stale lower-severity tickets do not overwhelm true P1 incidents, and then adds recurrence, affected-user, customer-effort, and vendor-blocker pressure to surface issues that need cross-team coordination.

## Review Questions

- Which issues should be escalated before the next user group?
- Which releases have the weakest test readiness?
- Which vendors are slowing application support?
- Which requirements represent recurring issues rather than one-off tickets?
