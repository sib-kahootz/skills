#!/usr/bin/env python3
"""Create a Jira-named Git branch from an updated base branch."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata


ISSUE_KEY_RE = re.compile(r"([A-Z][A-Z0-9]+-\d+)", re.IGNORECASE)


def run_git(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def extract_issue_key(jira_url: str) -> str:
    match = ISSUE_KEY_RE.search(jira_url)
    if not match:
        raise ValueError(f"Could not find a Jira issue key in URL: {jira_url}")
    return match.group(1)


def slugify_summary(summary: str) -> str:
    normalized = unicodedata.normalize("NFKD", summary)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = ascii_text.lower()
    slug = re.sub(r"[\\/\s_]+", "-", slug)
    slug = re.sub(r"[^a-z0-9.-]+", "-", slug)
    slug = re.sub(r"\.+", ".", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-.")
    if not slug:
        raise ValueError("Jira summary produced an empty branch title")
    return slug


def branch_exists(branch: str) -> tuple[bool, str | None]:
    local = run_git(["show-ref", "--verify", "--quiet", f"refs/heads/{branch}"], check=False)
    if local.returncode == 0:
        return True, "local"

    remote = run_git(["show-ref", "--verify", "--quiet", f"refs/remotes/origin/{branch}"], check=False)
    if remote.returncode == 0:
        return True, "remote"

    return False, None


def validate_branch_name(branch: str) -> None:
    result = run_git(["check-ref-format", "--branch", branch], check=False)
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "invalid branch name"
        raise ValueError(f"Generated branch name is not valid: {branch}\n{message}")


def create_branch(jira_url: str, summary: str, base_branch: str, dry_run: bool) -> str:
    issue_key = extract_issue_key(jira_url)
    branch = f"{issue_key}-{slugify_summary(summary)}"
    validate_branch_name(branch)

    if dry_run:
        return branch

    run_git(["rev-parse", "--is-inside-work-tree"])
    run_git(["switch", base_branch])
    run_git(["pull", "--ff-only", "origin", base_branch])

    exists, location = branch_exists(branch)
    if exists:
        raise RuntimeError(f"Branch already exists ({location}): {branch}")

    run_git(["switch", "-c", branch, base_branch])
    return branch


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jira-url", required=True, help="Jira ticket URL containing the issue key")
    parser.add_argument("--summary", required=True, help="Jira ticket summary/title")
    parser.add_argument("--base-branch", default="master", help="Base branch to update and branch from")
    parser.add_argument("--dry-run", action="store_true", help="Print the branch name without Git changes")
    args = parser.parse_args()

    try:
        branch = create_branch(args.jira_url, args.summary, args.base_branch, args.dry_run)
    except (subprocess.CalledProcessError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(branch)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
