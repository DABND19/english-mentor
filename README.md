# english-mentor

Claude Code skill that reviews English writing and gives structured feedback for a non-native speaker.

## Trigger

Prefix your text with `/english-mentor:writing`. Also triggers on an explicit request to check/correct English writing.

## Output

Fixed 5-section format:

1. Original text with errors marked inline (`` `span` ``[N])
2. Error breakdown — numbered explanation per marked error
3. Structure & logic
4. Style
5. Recurring patterns — including history from local tracking

See [SKILL.md](SKILL.md) for the full spec.

## Install

```
/plugin marketplace add DABND19/english-mentor
/plugin install english-mentor@english-mentor
```

## Progress tracking

`scripts/track.py` logs each review to a local SQLite DB (`~/.english-mentor/progress.db`, override with `ENGLISH_MENTOR_DB`) so recurring error categories can be tracked across sessions.

```
python3 scripts/track.py stats [--json]   # summary of recurring error categories
python3 scripts/track.py log              # reads a JSON payload from stdin, stores it
```

Only works with persistent filesystem access (e.g. Claude Code CLI). No-op in a browser sandbox.
