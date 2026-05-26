#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo


TAG_PATTERN = re.compile(r"^v(?P<year>\d{4})-W(?P<week>0[1-9]|[1-4]\d|5[0-3])$")
BASE_REF_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*(?:~[0-9]+)?$")
FIELD_SEPARATOR = "\x1f"
RECORD_SEPARATOR = "\x1e"
DEFAULT_IGNORED_TOPICS = ".github,.idea,scripts,docs"


@dataclass(frozen=True)
class Commit:
    hash: str
    subject: str
    files: list[str]
    topics: list[str]


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-c", "core.quotePath=false", *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate release notes from git commits grouped by topic."
    )
    parser.add_argument(
        "--date",
        default=os.getenv("RELEASE_DATE", ""),
        help="Release date in YYYY-MM-DD. Defaults to today in --timezone.",
    )
    parser.add_argument(
        "--timezone",
        default=os.getenv("RELEASE_TIMEZONE", "Asia/Seoul"),
        help="Timezone used when --date is omitted.",
    )
    parser.add_argument(
        "--base-ref",
        default=os.getenv("RELEASE_BASE_REF", ""),
        help="Git ref to compare from. Defaults to the previous ISO week release tag.",
    )
    parser.add_argument(
        "--output",
        default="release-notes.md",
        help="Path for the generated Markdown release notes.",
    )
    parser.add_argument(
        "--metadata",
        default="release-metadata.json",
        help="Path for generated metadata JSON. Use an empty string to skip.",
    )
    parser.add_argument(
        "--ignore-topic",
        action="append",
        default=[],
        help="Top-level directory to omit from release note topics. Repeatable.",
    )
    parser.add_argument(
        "--include-merges",
        action="store_true",
        help="Include merge commits in the release notes.",
    )
    return parser.parse_args()


def release_date(value: str, timezone: str) -> dt.date:
    if value:
        return dt.date.fromisoformat(value)
    return dt.datetime.now(ZoneInfo(timezone)).date()


def iso_week_range(
    value: dt.date,
    timezone: str,
) -> tuple[dt.datetime, dt.datetime]:
    tzinfo = ZoneInfo(timezone)
    week_start_date = value - dt.timedelta(days=value.isoweekday() - 1)
    week_start = dt.datetime.combine(week_start_date, dt.time.min, tzinfo=tzinfo)
    return week_start, week_start + dt.timedelta(days=7)


def version_for_date(value: dt.date) -> str:
    iso_year, iso_week, _ = value.isocalendar()
    return f"v{iso_year}-W{iso_week:02d}"


def tag_key(tag: str) -> tuple[int, int]:
    match = TAG_PATTERN.fullmatch(tag)
    if match is None:
        raise ValueError(f"Invalid release tag: {tag}")
    return (
        int(match.group("year")),
        int(match.group("week")),
    )


def release_tags() -> list[str]:
    tags = []
    for tag in run_git(["tag", "--list"]).splitlines():
        tag = tag.strip()
        if TAG_PATTERN.fullmatch(tag):
            tags.append(tag)
    return sorted(tags, key=tag_key)


def validate_base_ref(base_ref: str) -> str:
    if not base_ref:
        return ""
    if base_ref != base_ref.strip() or "\n" in base_ref or "\r" in base_ref:
        raise ValueError(f"Invalid base ref: {base_ref!r}")
    if ".." in base_ref or "//" in base_ref or base_ref.endswith((".", ".lock")):
        raise ValueError(f"Invalid base ref: {base_ref!r}")
    if not BASE_REF_PATTERN.fullmatch(base_ref):
        raise ValueError(f"Invalid base ref: {base_ref!r}")
    return base_ref


def previous_release_tag(current_version: str, base_ref: str) -> str | None:
    valid_base_ref = validate_base_ref(base_ref)
    if valid_base_ref:
        return valid_base_ref
    current_key = tag_key(current_version)
    previous_tags = [tag for tag in release_tags() if tag_key(tag) < current_key]
    return previous_tags[-1] if previous_tags else None


def tag_exists(tag: str) -> bool:
    return tag in set(release_tags())


def ignored_topics(extra_ignored_topics: list[str]) -> set[str]:
    raw_topics = os.getenv("RELEASE_NOTE_IGNORED_TOPICS", DEFAULT_IGNORED_TOPICS)
    topics = {topic.strip() for topic in raw_topics.split(",") if topic.strip()}
    topics.update(extra_ignored_topics)
    return topics


def topic_for_path(path: str, ignored: set[str]) -> str | None:
    normalized = path.strip("/")
    if "/" not in normalized:
        return None
    topic = normalized.split("/", 1)[0]
    if topic.startswith(".") or topic in ignored:
        return None
    return topic


def changed_files(commit_hash: str) -> list[str]:
    output = run_git(
        ["diff-tree", "--root", "--no-commit-id", "--name-only", "-r", commit_hash]
    )
    return [line for line in output.splitlines() if line]


def commit_log_range(previous_tag: str | None) -> str:
    return f"{previous_tag}..HEAD" if previous_tag else "HEAD"


def collect_commits(
    previous_tag: str | None,
    since: dt.datetime,
    before: dt.datetime,
    ignored: set[str],
    include_merges: bool,
) -> list[Commit]:
    git_format = f"%H{FIELD_SEPARATOR}%P{FIELD_SEPARATOR}%s{RECORD_SEPARATOR}"
    output = run_git(
        [
            "log",
            "--reverse",
            f"--format={git_format}",
            f"--since={since.isoformat(timespec='seconds')}",
            f"--before={before.isoformat(timespec='seconds')}",
            commit_log_range(previous_tag),
        ]
    )
    commits: list[Commit] = []

    for record in output.split(RECORD_SEPARATOR):
        if not record.strip():
            continue
        commit_hash, parents, subject = record.lstrip("\n").split(FIELD_SEPARATOR, 2)
        if not include_merges and len(parents.split()) > 1:
            continue

        files = changed_files(commit_hash)
        topics = []
        seen_topics = set()
        for file_path in files:
            topic = topic_for_path(file_path, ignored)
            if topic is not None and topic not in seen_topics:
                seen_topics.add(topic)
                topics.append(topic)

        if topics:
            commits.append(
                Commit(
                    hash=commit_hash,
                    subject=subject.strip(),
                    files=files,
                    topics=topics,
                )
            )

    return commits


def topic_order(commits: list[Commit]) -> list[str]:
    order: list[str] = []
    seen = set()
    for commit in commits:
        for topic in commit.topics:
            if topic not in seen:
                seen.add(topic)
                order.append(topic)
    return order


def commits_by_topic(commits: list[Commit]) -> dict[str, list[Commit]]:
    grouped = {topic: [] for topic in topic_order(commits)}
    for commit in commits:
        for topic in commit.topics:
            grouped[topic].append(commit)
    return grouped


def render_commit(commit: Commit) -> str:
    return f"- `{commit.hash[:7]}` {commit.subject}"


def render_markdown(
    version: str,
    date_value: dt.date,
    week_start: dt.datetime,
    week_end: dt.datetime,
    previous_tag: str | None,
    commits: list[Commit],
) -> str:
    lines = [f"# {version}", ""]
    lines.append(f"- Date: {date_value.isoformat()}")
    lines.append(
        "- Commit date range: "
        f"`{week_start.isoformat(timespec='seconds')}`..."
        f"`{week_end.isoformat(timespec='seconds')}`"
        " (end exclusive)"
    )
    if previous_tag:
        lines.append(f"- Base ref: `{previous_tag}`")
    else:
        lines.append("- Base ref: repository history")
    lines.append("")

    grouped = commits_by_topic(commits)
    if not grouped:
        lines.extend(["## Commits", "", "- 없음", ""])
    else:
        for topic, topic_commits in grouped.items():
            lines.extend([f"## {topic}", ""])
            lines.extend(render_commit(commit) for commit in topic_commits)
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_github_outputs(metadata: dict[str, object]) -> None:
    output_path = os.getenv("GITHUB_OUTPUT")
    if not output_path:
        return
    with Path(output_path).open("a", encoding="utf-8") as file:
        for key in (
            "version",
            "previous_tag",
            "commit_count",
            "topic_count",
            "target_sha",
            "should_release",
        ):
            value = metadata[key]
            if isinstance(value, bool):
                value = str(value).lower()
            if value is None:
                value = ""
            value = str(value)
            if "\n" in value or "\r" in value:
                raise ValueError(f"Invalid GitHub output value for {key}")
            file.write(f"{key}={value}\n")


def main() -> int:
    args = parse_args()
    date_value = release_date(args.date, args.timezone)
    week_start, week_end = iso_week_range(date_value, args.timezone)
    version = version_for_date(date_value)
    previous_tag = previous_release_tag(version, args.base_ref)
    ignored = ignored_topics(args.ignore_topic)
    commits = collect_commits(
        previous_tag,
        week_start,
        week_end,
        ignored,
        args.include_merges,
    )
    topics = topic_order(commits)
    target_sha = commits[-1].hash if commits else ""
    existing_tag = tag_exists(version)
    should_release = bool(commits) and not existing_tag

    output_path = Path(args.output)
    output_path.write_text(
        render_markdown(
            version,
            date_value,
            week_start,
            week_end,
            previous_tag,
            commits,
        ),
        encoding="utf-8",
    )

    metadata = {
        "version": version,
        "release_date": date_value.isoformat(),
        "week_start": week_start.isoformat(timespec="seconds"),
        "week_end": week_end.isoformat(timespec="seconds"),
        "timezone": args.timezone,
        "previous_tag": previous_tag,
        "current_tag_exists": existing_tag,
        "commit_count": len(commits),
        "topic_count": len(topics),
        "topics": topics,
        "target_sha": target_sha,
        "should_release": should_release,
        "output": str(output_path),
    }
    if args.metadata:
        Path(args.metadata).write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    write_github_outputs(metadata)
    print(json.dumps(metadata, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as error:
        sys.stderr.write(error.stderr)
        raise SystemExit(error.returncode) from error
    except Exception as error:
        sys.stderr.write(f"{error}\n")
        raise SystemExit(1) from error
