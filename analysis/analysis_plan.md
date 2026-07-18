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

The triage score combines:

- SLA breach risk from issue age versus target resolution window
- Severity weighting
- Defect recurrence
- Affected user count
- Customer effort score
- Vendor blocker flag
- Release readiness exposure

## Review Questions

- Which issues should be escalated before the next user group?
- Which releases have the weakest test readiness?
- Which vendors are slowing application support?
- Which requirements represent recurring issues rather than one-off tickets?
