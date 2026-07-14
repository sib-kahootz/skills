---
name: new-branch
description: Create a new Git branch from an updated base branch using a Jira ticket URL, defaulting the base to master. Use when the user asks to create, switch to, or prepare a branch named from a Jira issue key and summary, especially from Jira URLs such as https://.../browse/PROJ-123.
---

# New Branch

Create a Git branch from an updated base branch using the Jira issue key and summary. Use `master` unless the user provides another base branch.

## Workflow

1. Extract the Jira ticket key from the URL, preserving its exact case and punctuation, for example `PROJ-123`.
2. Retrieve the Jira issue details and identify the summary/title.
   - Prefer an available Jira or Atlassian connector.
   - If no connector is available, use the workspace's existing Jira CLI or REST setup.
   - If the title cannot be retrieved, ask the user for the exact Jira summary before creating the branch.
3. Run `scripts/new_branch.py` from the target Git repository with the Jira URL and summary:

```powershell
python C:\Users\SimonBingham\.codex\skills\custom\new-branch\scripts\new_branch.py --jira-url "<jira-url>" --summary "<jira-summary>"
```

   When the user provides another base branch, pass it explicitly:

```powershell
python C:\Users\SimonBingham\.codex\skills\custom\new-branch\scripts\new_branch.py --jira-url "<jira-url>" --summary "<jira-summary>" --base-branch "<base-branch>"
```

4. Report the base branch used and the branch name created, or the existing branch that blocked creation.

## Branch Rules

Use this format:

```text
<ticket-id>-<ticket-title>
```

The script applies these rules to the title:

- Convert to lowercase.
- Replace whitespace and separators with hyphens.
- Remove characters invalid or undesirable in Git branch names.
- Collapse repeated hyphens.
- Trim leading and trailing hyphens.

Example:

```text
PROJ-123-add-user-authentication
```

The script checks out the selected base branch, pulls it from `origin`, checks local and remote branches for the same name, validates the final ref with `git check-ref-format`, and creates the new branch from the updated local base branch.
