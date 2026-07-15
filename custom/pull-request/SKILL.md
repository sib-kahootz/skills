---
name: pull-request
description: Prepare, review, update, push, and create GitHub pull requests from local branch work. Use when the user asks to open a PR, create a pull request, update an existing PR, prepare a draft PR, publish current branch work, push a branch for review, write or refresh a PR title/body, add reviewer testing focus guidance, assign the PR, choose or apply PR labels, or check PR readiness before publishing. When a pull request already exists for the branch, review and update that PR instead of creating a duplicate. Default to draft PRs unless the user explicitly asks for ready-for-review.
---

# Pull Request

Prepare a pull request that is safe to publish. Prefer the GitHub connector when available; use authenticated `gh` as fallback.

Git is required. GitHub access is required to publish. Jira is optional: use it when available and a ticket key can be inferred, but do not block only because Jira is unavailable.

PR documentation must describe the net change from the base branch to the head branch only. Do not document changes between commits on the current branch, do not write a branch changelog, and do not describe what changed "since the last update" unless the user explicitly asks for that history.

## Safety Rules

- Do not create or publish a new PR before explicit user confirmation.
- Default to draft PRs.
- Do not stage, commit, push, reset, stash, clean, or checkout over user work without clear scope.
- Do not stage unrelated changes silently.
- Do not modify code, tests, docs, assets, generated files, or config in the branch. This skill only inspects branch content and updates PR metadata after confirmation.
- If readiness checks find problems, report them as blockers or risks; do not fix them unless the user stops using this skill and explicitly asks for code changes.
- Do not push to an unexpected remote, base, or head branch.
- Do not claim tests, PR body/title updates, labels, assignment, or publish state succeeded unless the tool confirms it.
- If publishing fails after a push, report exactly what succeeded and what remains; do not risk duplicate PR creation without user approval.
- If an existing PR is found, treat it as the target PR: review it, refresh stale metadata, and update it instead of creating another PR.

## Workflow

### 1. Resolve Scope

Run:

```bash
git status -sb
git branch --show-current
git remote -v
git branch --all --verbose --no-abbrev
```

Identify:

- base branch
- head branch
- current worktree state
- remote to push to
- whether uncommitted changes are in scope
- whether a PR already exists for the branch

Infer base branch in order:

1. explicit user input
2. `origin/HEAD`
3. GitHub default branch if available
4. local `main`, `master`, `develop`, then `dev`

Ask before staging or committing when the worktree contains unrelated or ambiguous changes.

### 2. Detect Existing PR

Before drafting a new PR, check whether the current branch already has an open PR.

With `gh`, run:

```bash
gh pr view --json number,title,body,state,isDraft,url,baseRefName,headRefName,labels,assignees
```

If unavailable or ambiguous, search by head branch:

```bash
gh pr list --head <headBranch> --state open --json number,title,state,isDraft,url,baseRefName,headRefName
```

When an existing PR is found:

- Continue the workflow as an update to that PR, not as a new PR.
- Compare the current PR title, body, base branch, labels, assignees, draft state, and reviewer guidance against the branch evidence.
- Preserve human-written PR content that is still accurate and relevant unless it is stale, misleading, duplicated, or contradicted by the current branch.
- Refresh the PR body when the net `baseBranch...headBranch` diff makes the existing body stale, misleading, duplicated, or incomplete.
- Refresh labels only when `references/labels.local.json` is available and its guidance indicates drift. Leave existing labels unchanged otherwise.
- Mention any base branch mismatch and ask before changing base.
- Do not close, reopen, mark ready, or convert to draft unless the user explicitly asks or confirms.

### 3. Gather Context

Collect:

```bash
git diff --stat baseBranch...headBranch
git log --oneline --decorate -n 30 baseBranch..headBranch
git diff --name-status baseBranch...headBranch
git diff baseBranch...headBranch
git diff -U0 baseBranch...headBranch
```

Use `baseBranch...headBranch` as the sole source for PR body content, reviewer focus, deployment notes, migration notes, risks, and testing scope. Use commit logs only to find context such as ticket keys or intent; do not turn commit-to-commit changes into PR documentation.

Inspect the zero-context diff for newly added code lines containing `TODO`. For each added TODO, record the file path, line number when available from the diff hunk, and the TODO text. Ignore removed or unchanged TODOs. Ignore generated/vendor files unless the PR otherwise requires documenting them.

If uncommitted changes are in scope, also inspect:

```bash
git diff --cached
git diff
```

Inspect local PR guidance before drafting:

- repository PR template, if present
- `README*`, `CONTRIBUTING*`, `AGENTS.md`
- relevant docs under `docs/`
- test/build config and package scripts
- nearby code and tests for changed areas

Find Jira keys in branch name, commits, changed paths, and user text. If Jira tools are available, read summary, acceptance criteria, status, labels/components/fix versions, relevant comments, and linked issues.

### 4. Check Readiness

Before proposing the PR, check for issues that would make it premature or confusing:

- accidental debug/local files
- missing generated assets, migrations, snapshots, lockfiles, or docs
- missing tests for risky behavior
- merge conflict or branch drift risk
- unclear screenshots, migration notes, rollout notes, or manual QA needs
- release actions: config changes, schema changes, restarts, cache clears, rebuilds, post-release tasks
- security, accessibility, performance, compatibility, or data-contract risk
- newly added TODO items that reviewers need to see and track

Run focused tests, type checks, lint, build, or migration checks when discoverable and proportionate. If not run, say why and include unverified areas in the PR body.

Do not make branch file changes while checking readiness. Treat missing tests, stale docs, accidental files, formatting issues, lint failures, and similar findings as review notes for the user, not as work to repair inside this workflow.

### 5. Draft Or Refresh PR

Read `references/pr-description.md` and follow its structure unless the repo has a stricter template.

Title rules:

- Start the title with a verb and name the changed area or outcome.
- Prefix with `[ABC-123]` when one clear Jira ticket exists.
- Keep Jira ticket IDs in the title as plain text because GitHub titles do not support Markdown links.
- If multiple Jira keys exist and no primary key is clear, ask which to use or omit the prefix and disclose the ambiguity before publishing.
- Avoid vague titles such as `updates`, `changes`, `fixes`, or `stuff`.

Body must include:

- Jira ticket ID as a Markdown link when its URL can be determined, for example `[ABC-123](https://your-jira.example/browse/ABC-123)`
- every Jira ticket ID rendered in the PR body as a Markdown link when its URL can be determined; keep only the PR title ticket prefix as plain text because GitHub titles do not render Markdown
- summary of what changed and why
- concrete implementation changes
- automated and manual testing
- high-level summary of where reviewers should focus their testing
- deployment steps, including `Standard deploy only. No special deployment steps.` only when true
- migration notes when migrations are present, following `references/pr-description.md`
- risks and impacts, including unverified areas
- a `TODO Items` section when newly added TODOs are present, with one unchecked Markdown checkbox per TODO item

If `references/labels.local.json` exists, read and validate it before proposing labels. Use only labels and meanings supplied by that file, then prepare:

- labels to apply
- labels that may need confirmation
- labels intentionally not applied despite related-looking changes, when that helps avoid confusion

If the file is absent or invalid, do not propose, add, remove, or otherwise change labels. State that label configuration was not supplied and leave existing PR labels unchanged. Do not treat any label as required without local configuration.

For an existing PR, produce an update proposal with:

- current PR URL and state
- title/body changes to apply, or "no title/body change needed" with reason
- labels to add/remove and labels to leave unchanged
- assignee changes to apply or leave unchanged
- checks/tests newly run and checks/tests still unverified
- deployment, migration, release, and risk notes required by the current `baseBranch...headBranch` diff

### 6. Propose Before Publishing Or Updating

Show the user:

- base and head branch
- PR URL when updating an existing PR
- draft or ready-for-review state
- title
- full body
- labels, or `not configured` when `references/labels.local.json` is absent or invalid
- assignee, defaulting to current GitHub user when discoverable
- tests and checks run
- deployment steps
- remaining risk or unanswered questions

For a new PR, ask whether to publish. For an existing PR, ask whether to apply the proposed PR updates unless the user's request already clearly authorized updating it. If the user asks for edits, update the proposal and ask again.

## Parallel Agent Opportunities

When subagent tools are available and the preparation scope is broad enough to benefit, split preparation into independent checks and keep publish/update actions in the parent agent. 

Good splits:

- Readiness agent: inspect diffs for accidental files, missing tests, migrations, generated assets, drift, and release risk.
- PR draft agent: draft or refresh title/body from branch evidence, templates, Jira context, deployment notes, and reviewer focus.
- Labels and verification agent: inspect label guidance, assignee assumptions, runnable checks, and unverified areas.

Do not let agents stage, commit, push, edit PRs, change labels, or publish. Parent agent owns confirmation, branch push, PR creation/update, and final verified state.

### 7. Publish Or Update

Ensure the branch is pushed to the intended remote before PR creation. Ask before pushing if the upstream is missing, surprising, or not already clear from the request.

If an existing PR was found, update that PR instead of creating a new one.

With `gh`, prefer body files for body updates:

```bash
gh pr edit <prUrlOrNumber> --title "<title>" --body-file <bodyFile>
```

Only edit fields that need to change. When a valid `references/labels.local.json` was supplied and label changes were confirmed, add and remove labels explicitly:

```bash
gh pr edit <prUrlOrNumber> --add-label "label-a,label-b"
gh pr edit <prUrlOrNumber> --remove-label "label-c"
```

For assignee:

```bash
gh pr edit <prUrlOrNumber> --add-assignee <currentGitHubLogin>
```

After editing, re-read the PR to verify applied state:

```bash
gh pr view <prUrlOrNumber> --json number,title,body,state,isDraft,url,baseRefName,headRefName,labels,assignees
```

For new PRs, create a draft PR unless the user explicitly approved ready-for-review.

With `gh`, prefer a body file:

```bash
gh pr create --draft --base <baseBranch> --head <headBranch> --title "<title>" --body-file <bodyFile>
```

Only omit `--draft` after explicit ready-for-review approval.

Resolve current GitHub user when assigning:

```bash
gh api user --jq .login
```

Then apply assignment and, only when a valid `references/labels.local.json` was supplied and label changes were confirmed, labels when supported:

```bash
gh pr edit <prUrlOrNumber> --add-assignee <currentGitHubLogin>
gh pr edit <prUrlOrNumber> --add-label "bug,NEED migrate step"
```

If labels or assignment fail, report the intended values for manual application.

## Final Response

Report concisely:

- PR URL and draft/ready state
- base and head branch
- whether the PR was newly created or an existing PR was updated
- assignee applied or still needed
- labels applied or still needed
- tests/checks run and not verified
- reviewer testing focus included
- deployment steps included
- known risks or release actions

Keep the final response reviewer-oriented, not celebratory.
