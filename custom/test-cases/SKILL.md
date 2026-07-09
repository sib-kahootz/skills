---
name: test-cases
description: Create tester-ready spreadsheet test cases, manual QA checklists, and acceptance test plans for code changes, local branches, diffs, pull requests, tickets, releases, or feature work. Use when Codex should inspect implementation evidence, optionally enrich it with GitHub or Jira context, identify behavior and risk coverage, produce test cases with step-by-step instructions, expected results, setup assumptions, context gaps, coverage rationale, and offer to add the generated cases as a pull request comment when a PR exists for the branch.
---

# Test Cases

Create practical manual test plans a human tester can execute without reading the code. Base the plan on implementation evidence first, then enrich with ticket, PR, or user context.

Default to producing the generated test cases as a spreadsheet-compatible table. Create an `.xlsx` or `.csv` file when the user asks for a file; otherwise return a markdown table in chat using the same spreadsheet columns.

## Workflow

### 1. Resolve Scope

Accept any of:

- current branch or current changes
- named branch or commit range
- supplied diff
- PR URL or number
- Jira ticket or acceptance criteria
- user-described feature or release

For local branch work, inspect enough Git state to understand the comparison:

```bash
git status --short
git branch --show-current
git remote -v
git branch --all --verbose --no-abbrev
git diff --stat <base>...<head>
git diff --name-status <base>...<head>
git diff <base>...<head>
```

Infer base branch conservatively from explicit user input, `origin/HEAD`, upstream branch, then `main`, `master`, `develop`, or `dev`. Ask only when scope cannot be inferred safely.

Include staged, unstaged, and untracked files when the user asks for current changes or when they appear relevant.

### 2. Gather Context

Use available context, but treat it as evidence to reconcile:

- GitHub: PR title/body, labels, linked issues, review comments, changed files
- Jira: summary, description, acceptance criteria, comments, linked bugs, status, labels/components/fix versions
- Repository docs: setup, QA, permissions, feature flags, environments, test data, release notes
- Nearby code/tests: behavior, roles, state transitions, contracts, failure handling

If GitHub or Jira is unavailable, continue from local evidence. Mention missing context only when it creates a real blind spot.

### 3. Map Behavior And Risk

Summarize what changed in user-facing, operator-facing, API-facing, or data-facing terms.

Consider these areas and emit only relevant tests:

- happy path
- regression around touched behavior
- validation and edge cases
- roles, permissions, tenancy, ownership, and sensitive data
- feature flags, config, environments, and rollout state
- migrations, backward compatibility, and existing data
- UI, accessibility, responsive layout, forms, focus, keyboard, and dynamic content
- API contracts, error shapes, idempotency, and partial failures
- integrations, async jobs, queues, notifications, retries, and failure states
- performance, security, audit logging, monitoring, and observability
- deployment, cache clear, restart, rebuild, or post-release actions

Do not pad with generic tests that do not follow from the change.

### 4. Reconcile Conflicts

Call out disagreements instead of smoothing them over:

- Ticket requires behavior with no implementation evidence.
- Diff changes behavior not described in ticket or PR.
- PR text claims tests or deployment steps that the repo evidence does not support.
- Acceptance criteria are too vague to test directly.
- Test data, credentials, feature flags, or environment details are missing.

Convert vague requirements into observable checks and state the assumption.

### 5. Offer PR Comment

When the request is for a pull request or branch, check whether a PR exists for the branch after generating the test cases.

Prefer already-gathered GitHub connector context. For local branches, if needed, use GitHub CLI commands such as:

```bash
gh pr view --json number,title,url,headRefName,baseRefName
gh pr list --head <branch> --state open --json number,title,url,headRefName,baseRefName
```

If a matching PR exists, offer to add the generated markdown as a PR comment. Do not post the comment until the user explicitly confirms. If they confirm, post exactly the generated test cases unless the user asks for edits first.

Use the GitHub connector when available; otherwise use:

```bash
gh pr comment <pr-number-or-url> --body-file <temporary-markdown-file>
```

After posting, report the PR URL or number. If no PR exists, mention that PR commenting was not offered because no matching open PR was found.

## Parallel Agent Opportunities

When subagent tools are available and the test planning scope is broad enough to benefit, split test planning by risk area and keep final synthesis in the parent agent. 

Good splits:

- Behavior agent: map happy paths, regressions, state transitions, and core user workflows.
- Risk agent: map validation, permissions, security, accessibility, edge cases, and failure states.
- Release agent: map deployment checks, rollback checks, feature flags, integrations, environments, and test data gaps.

Do not let agents produce overlapping generic cases. Parent agent owns deduplication, chronology, tester-ready wording, and final coverage rationale.

## Output Contract

Use this structure unless the user asks for another format. Keep supporting context concise and make the spreadsheet table the primary deliverable:

```markdown
# Test Cases

## Scope

- Branch/change: ...
- Compared against: ...
- Context used: ...

## Assumptions / Tester Setup

- [ ] Tester has access to ...
- [ ] Feature flag ... is enabled.
- [ ] Test data exists for ...

## Context Gaps

- ...

## Coverage Rationale

- ...

## Test Cases

| Test Case ID | Feature | Test Case Description | Test Steps | Expected Result | Status | Comments |
| --- | --- | --- | --- | --- | --- | --- |
| TC-001 | ... | ... | 1. ...<br>2. ...<br>3. ... | ... | Not Run | Preconditions: ...<br>Notes: ... |
```

Add sections for deployment checks, rollback checks, or exploratory notes only when the change needs them.

### Spreadsheet Column Rules

- `Test Case ID`: Use stable sequential IDs such as `TC-001`, `TC-002`, and keep IDs unique across the output.
- `Feature`: Name the feature, workflow, API, permission area, integration, or release concern under test.
- `Test Case Description`: State the tester-readable scenario and risk covered in one concise sentence.
- `Test Steps`: Use chronological numbered steps. Put preconditions or required test data in the first step or in `Comments`.
- `Expected Result`: State observable outcomes and meaningful assertions.
- `Status`: Default to `Not Run` unless the user supplies another status.
- `Comments`: Include setup notes, assumptions, context gaps, required roles, feature flags, data IDs, environment needs, or exploratory notes.

## Test Case Quality Bar

- Make every case executable by a tester who has not read the code.
- Use chronological steps with one action or assertion per numbered step.
- Prefer observable behavior over implementation details.
- Include expected results for each meaningful assertion.
- Use real domain terms found in code, docs, ticket, or PR.
- Separate materially different risks into separate cases.
- Include negative and regression tests when they protect changed behavior.
- Include accessibility tests for UI changes affecting focus, keyboard flow, forms, semantic state, dynamic updates, or layout.
- Include permission/security tests when auth, roles, ownership, tenancy, validation, redirects, logging, or sensitive data changed.
- Include failure-state tests when integrations, async work, retries, notifications, or background jobs changed.
- Use placeholders or setup checkboxes for missing environments, users, IDs, flags, credentials, and seed data. Do not invent them.

## Final Notes

If the user wants cases for a PR or branch and no diff can be inspected, ask for the diff, branch, PR URL, or relevant files. If the user asks for high-level QA coverage without implementation access, produce a clearly assumption-based plan and label context gaps.
