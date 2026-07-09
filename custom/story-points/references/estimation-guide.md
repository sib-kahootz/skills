# Estimation Guide

## Workflow

1. Identify the story type: feature, bug, chore, spike, migration, operational task, or mixed work.
2. Restate the expected outcome in one sentence using product language from the ticket.
3. Split the work mentally into implementation, data or migration work, integration points, testing, review, and release coordination.
4. If a local checkout is available, run a quick code-path scan to find likely affected files, modules, tests, configuration, database migrations, or API/UI entry points.
5. Check for uncertainty drivers.
6. Compare against known local calibration if the ticket, project, or conversation includes examples of previous stories and their point values.
7. Choose the smallest point value that covers the likely work and uncertainty. Do not average unrelated possibilities; explain the branch that would move the estimate up or down.

## Quick Code-Path Scan

Keep the scan bounded. Use it to improve estimate quality, not to fully implement or review the story.

1. Search for ticket keywords, feature names, endpoint names, UI labels, domain terms, and likely database/table names with `rg`.
2. Prefer direct evidence from routes, handlers, services, components, schema/migration files, tests, and existing nearby implementations.
3. Cite the likely files or directories that materially influence the estimate. If the scan is inconclusive, say so and estimate from ticket context.
4. Do not read broad areas of the repo unless the first-pass evidence shows the story crosses multiple subsystems.
5. If no checkout is available, state that no local code-path scan was performed.

## Uncertainty Drivers

- unclear acceptance criteria
- unknown affected code areas
- cross-team or third-party dependency
- data migration or backfill
- permissions, security, billing, audit, or compliance behavior
- UI and API changes in the same story
- production-risky rollout or rollback constraints

## Default Scale

Use this scale only when no team-specific calibration is available:

- `1`: trivial, well-understood change with narrow tests and little review risk.
- `2`: small change in one area, clear acceptance criteria, low uncertainty.
- `3`: normal story touching a few files or one workflow, with moderate tests.
- `5`: multi-step story, multiple components, non-trivial testing, or some unknowns.
- `8`: broad or risky story with multiple workflows, integration points, migration, or high uncertainty.
- `13`: too large for a normal sprint story; recommend splitting before committing.

Avoid `0` unless the team explicitly uses it. Treat investigation-only work as a spike and estimate the time-box or use the team's spike convention.

## Output Format

Return:

```markdown
Recommended estimate: N points
Confidence: High|Medium|Low

Likely code paths:
- path/to/file.ext: why it matters

Why:
- ...

Could move down if:
- ...

Could move up if:
- ...

Suggested split, if needed:
- ...

Jira update:
- I can apply `N` story points to `ISSUE-123` and add this rationale as a comment. Confirm before I update Jira.
```

Keep the answer short unless the user asks for detailed reasoning. When confidence is low, give the best provisional estimate and the one or two missing facts that matter most.

Include the Jira update offer only when the estimate came from a Jira issue and Jira write access appears available. Omit it for pasted descriptions, unresolved Jira links, or read-only Jira access.
