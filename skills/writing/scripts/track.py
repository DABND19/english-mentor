#!/usr/bin/env python3
"""
Local progress tracker for the english-writing-feedback skill.

Stores review history in a local SQLite file so recurring error patterns
can be tracked across sessions. Only useful when Claude has real, persistent
filesystem access (e.g. Claude Code CLI) -- in a browser sandbox the
filesystem resets between conversations, so this script is a no-op in
practice there.

Usage:
    python3 track.py log      # reads a JSON payload from stdin, stores it
    python3 track.py stats    # prints a summary of recurring error categories
    python3 track.py stats --json   # same, but machine-readable

JSON payload for `log` (read from stdin):
{
  "original": "the raw text that was reviewed",
  "corrected": "the corrected version",
  "errors": [
    {"category": "articles", "note": "short explanation of the specific mistake"},
    {"category": "prepositions", "note": "..."}
  ],
  "tips": ["tip 1", "tip 2"]
}

`category` should be a short, stable, lowercase label (e.g. "articles",
"prepositions", "tense", "word-choice", "word-order", "register") so counts
can be aggregated meaningfully across many reviews. Reuse existing category
names rather than inventing near-duplicates.
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from typing import Any

DB_PATH: str = os.environ.get(
    "ENGLISH_MENTOR_DB",
    os.path.expanduser("~/.english-mentor/progress.db"),
)


def get_conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            original TEXT NOT NULL,
            corrected TEXT NOT NULL,
            tips TEXT
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            review_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            note TEXT,
            FOREIGN KEY (review_id) REFERENCES reviews(id)
        )
        """
    )
    return conn


def cmd_log() -> None:
    try:
        payload: dict[str, Any] = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON on stdin: {e}", file=sys.stderr)
        sys.exit(1)

    original = payload.get("original", "")
    corrected = payload.get("corrected", "")
    errors = payload.get("errors", [])
    tips = payload.get("tips", [])

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reviews (created_at, original, corrected, tips) VALUES (?, ?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), original, corrected, json.dumps(tips)),
    )
    review_id = cur.lastrowid
    for err in errors:
        cur.execute(
            "INSERT INTO errors (review_id, category, note) VALUES (?, ?, ?)",
            (review_id, err.get("category", "uncategorized"), err.get("note", "")),
        )
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM reviews")
    total_reviews = cur.fetchone()[0]
    conn.close()

    print(
        f"logged review #{review_id} ({len(errors)} error(s)). total reviews so far: {total_reviews}"
    )


def cmd_stats(as_json: bool = False) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM reviews")
    total_reviews = cur.fetchone()[0]

    cur.execute(
        """
        SELECT category, COUNT(*) as cnt
        FROM errors
        GROUP BY category
        ORDER BY cnt DESC
        """
    )
    category_counts = cur.fetchall()

    cur.execute(
        """
        SELECT category, note, review_id
        FROM errors
        ORDER BY review_id DESC
        LIMIT 5
        """
    )
    recent = cur.fetchall()
    conn.close()

    if as_json:
        print(
            json.dumps(
                {
                    "total_reviews": total_reviews,
                    "category_counts": [
                        {"category": c, "count": n} for c, n in category_counts
                    ],
                    "recent_errors": [
                        {"category": c, "note": nt, "review_id": r}
                        for c, nt, r in recent
                    ],
                }
            )
        )
        return

    if total_reviews == 0:
        print("no reviews logged yet")
        return

    print(f"total reviews logged: {total_reviews}")
    print("error categories (most frequent first):")
    for category, count in category_counts:
        print(f"  - {category}: {count}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Track english-writing-feedback progress locally"
    )
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("log")
    stats_parser = sub.add_parser("stats")
    stats_parser.add_argument("--json", action="store_true", help="output as JSON")

    args = parser.parse_args()

    if args.command == "log":
        cmd_log()
    elif args.command == "stats":
        cmd_stats(as_json=args.json)


if __name__ == "__main__":
    main()
