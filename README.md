# no-tech-scribe

Working rules for AI coding agents whose operator is new to programming or new to agents. The rules cover what new users rarely set up themselves: a whoami, a project document with a MoSCoW list, building in layers, scope control, work snapshots, session memory and lessons.

## Use it

Give your agent the link from the [latest release](https://github.com/odjhey/no-tech-scribe/releases/latest), for example:

> Read https://github.com/odjhey/no-tech-scribe/releases/latest/download/no-tech-scribe.txt and follow it as your working instructions for this session.

To pin one version, use the version link from that release's notes.

## Edit the rules

The rules live in [src/no-tech-scribe.md](src/no-tech-scribe.md). Each rule is one line: `NTS-NNN: rule text`.

- Keep an ID when a rule moves or its wording improves.
- Give a materially different rule a new ID.
- To drop a rule, delete its line. Gaps in the numbers are fine.
- Never reuse a retired ID. New IDs go above the highest released ID.

`scripts/check-ids.py` checks these rules against every released tag. It runs on every push and pull request, and before each release. It fails when:

- an ID is used twice or a rule line is malformed;
- an ID dropped in an earlier release is used again;
- a new ID is not above the highest released ID;
- a rule has a new ID but the same text as a released rule (renumbered).

It warns when a released rule's wording changed a lot. A person then decides: same rule (keep the ID) or different rule (delete it and add a new ID).

[RELEASING.md](RELEASING.md) explains how to publish a version.

## Sources

The "Write code" rules (NTS-030 to NTS-034) are short paraphrases of:

- [Laziness Protocol](https://github.com/cursor/plugins/blob/main/pstack/skills/principle-laziness-protocol/SKILL.md) from cursor/plugins: consolidate decisions, minimize the diff.
- [Ponytail](https://github.com/dietrichgebert/ponytail) (MIT): the reuse-first order, finish the whole change, never cut safety, mark shortcuts.
