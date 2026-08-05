# english-mentor

Agent Skill (Claude Code plugin / Pi package) that reviews English writing and gives structured feedback for a non-native speaker.

## Trigger

Prefix your text with `/english-mentor:writing`. Also triggers on an explicit request to check/correct English writing.

## Output

Fixed 5-section format:

1. Original text with errors marked inline (`` `span` ``[N])
2. Error breakdown — numbered explanation per marked error
3. Structure & logic
4. Style
5. Recurring patterns — including history from local tracking

See [skills/writing/SKILL.md](skills/writing/SKILL.md) for the full spec.

## Install

**Claude Code:**

```
/plugin marketplace add DABND19/english-mentor
/plugin install english-mentor@english-mentor
```

**[Pi](https://pi.dev):**

```
pi install git:github.com/DABND19/english-mentor        # global
pi install git:github.com/DABND19/english-mentor -l      # project-local
```

Pi auto-discovers the skill from the conventional `skills/` directory — no extra manifest needed.

## Progress tracking

`skills/writing/scripts/track.py` logs each review to a local SQLite DB (`~/.english-mentor/progress.db`, override with `ENGLISH_MENTOR_DB`) so recurring error categories can be tracked across sessions.

```
python3 skills/writing/scripts/track.py stats [--json]   # summary of recurring error categories
python3 skills/writing/scripts/track.py log              # reads a JSON payload from stdin, stores it
```

Only works with persistent filesystem access (e.g. Claude Code CLI). No-op in a browser sandbox.
