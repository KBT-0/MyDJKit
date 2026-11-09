# MyDJKit — What this project is, and what it has decided

This is the project's **permanent knowledge**: what it is, how it is meant to behave, and
every decision that shaped it — each with the reasoning that produced it. A rule recorded
without its reason is a rule the next reader deletes, and they are usually right to. (Source:
a decision record keeps its context and consequences, Nygard,
https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions.)

For a game this is the design document. For a product it is the spec and the decision log.
For a tool it is the scope and the choices behind it. The section names below are a starting
point and are meant to be replaced with this project's own vocabulary.

**Web contact:**

<!-- What an API gets when it asks for contact details (a User-Agent, a `From` header): a role
     address or the project URL Kemal chose, never a person's own address. Empty
     until then: an agent whose request is refused for want of it asks Kemal once
     and writes the answer here (`docs/WORKFLOW.md`, "Web requests carry no personal data").
     Some APIs refuse a generic User-Agent outright (Wikimedia's User-Agent policy). -->

## How this file is read — never all at once

**This file is NOT in the session reading order.** It grows for the life of the project and
loading it whole would be a bill paid on every task that has nothing to do with it. Agents
read the SECTION they need, found through the Contents below, and cite it by number
(`PROJECT §4.2`) instead of copying its text somewhere else. A quotation is a duplicate; a
citation is not.

That is why the numbering is mandatory and why `scripts/check.sh` enforces that every
section appears in the Contents. A table of contents nobody maintains stops being a
navigation tool and becomes a lie about the file's shape. (Sources: Claude Code memory,
https://code.claude.com/docs/en/memory: an imported file still loads whole; Anthropic's skill
authoring guide: a file over 100 lines gets a table of contents.)

## How this file is written

**Every item carries a status:**

- **DECIDED** — settled. Binding on every agent. Contradicting it is a failed task (a spec
  the code is checked against: GitHub Spec Kit, spec-driven.md).
- **OPEN** — raised and not resolved. An agent may NEVER resolve one: it stops that item,
  raises it with Kemal, and continues other work that does not depend on it.

(Sources: GitHub Spec Kit, spec-driven.md, marks an open point `[NEEDS CLARIFICATION]`
instead of guessing; Claude Code best practices, "Let Claude interview you".)

**Who may write what:**

| Change | Who |
|---|---|
| Add an OPEN item, a question, a constraint that emerged | The agent, freely, at any time |
| Write DECIDED for an item Kemal explicitly approved in this session | The agent, transcribing |
| Decide, on its own judgement, that something is DECIDED | Nobody. Never |
| Supersede an existing DECIDED item (it stays, marked SUPERSEDED) | Kemal only |
| Reword a DECIDED item that quotes the owner into its summary, same meaning | The agent drafts; Kemal approves before the text changes |

Every DECIDED item carries `Decided: YYYY-MM-DD, approved by Kemal`. Its text is the
rule as a short summary, not the owner's chat sentence (`docs/COMMUNICATION.md`, "Questions and
approvals").

The line is between transcribing an approval and inferring one. An agent that hears
something that sounds like a decision records it as **OPEN with a note that the owner
appeared to decide it**, and asks. The cost of a missed capture is a forgotten question; the
cost of a wrongly promoted one is every future session treating a musing as law.

**Nothing is deleted — it is superseded.** When a decision is replaced, the old item stays,
marked `SUPERSEDED by §x.y`, with its date. The reasoning behind an abandoned direction is
how the next person avoids re-proposing it, and it is the first thing lost when items are
edited in place. (Source: an accepted architecture decision record is never reopened; a new
one supersedes it, Fowler, https://martinfowler.com/bliki/ArchitectureDecisionRecord.html.)

## What does NOT belong here

| Content | Its home |
|---|---|
| What is being worked on right now | `docs/STATE.md` |
| The current phase's scope and non-goals | `docs/PHASES.md` |
| Where code lives, module boundaries, contracts | `docs/ARCHITECTURE.md` |
| How we work: gates, review, task discipline | `docs/WORKFLOW.md` |
| An environment or tooling trap | `docs/GOTCHAS.md` |

The line against `ARCHITECTURE.md` is the one that blurs: **why the product behaves this way
belongs here; where the code lives and what it may reach belongs there.** "Money is stored
as integer minor units" is a decision. "The economy module may not reference the engine" is
architecture.

The line against `PHASES.md`: this file says what the project IS, that one says what we are
building right now and — more usefully — what we are deliberately not building yet.
(Sources for the split: Claude Code memory and best practices, frequently changing state
out of the permanent file; matklad's ARCHITECTURE.md, where the code lives.)

---

## Contents

<!-- Every "## N." heading below must be listed here, and scripts/check.sh fails when one is
     missing. Keep the numbers stable: other documents cite them. -->

- 1. What this project is
- 2. Setup decisions (2026-11-09)

---

## 1. What this project is

MyDJKit is a personal DJ assistant for a DDJ-FLX4 + Rekordbox 7 setup. It picks and orders
tracks by BPM and Camelot key compatibility (at least 80% of transitions blendable), keeps each
set's arc (intro → build → peak → close), downloads missing candidates from Apple Music with
gamdl, and writes the result safely into the Rekordbox database: playlists, hot cues and a
set guide. One user today. The repository is going PUBLIC: code and rules are shared, while
personal data (set definitions, plans, guide, session notes) lives in a git-ignored
`private/` folder synced to Cloudflare R2.

The binding project rules are in `AGENTS.md`, "Project rules"; personal ones in `private/PREFERENCES.md`.

<!-- Everything else is added as it is decided. This file is expected to be nearly empty on
     day one and to grow through conversation — that is the intended shape, not a gap to be
     filled in by generating plausible content. An agent writing sections nobody asked for is
     inventing a project rather than recording one. Sources: Claude Code best practices,
     "Write an effective CLAUDE.md" (only what the agent cannot infer); context files padded
     with derivable content raise cost without raising success (Gloaguen et al.,
     arXiv:2602.11988). -->

## 2. Setup decisions (2026-11-09)

All DECIDED by Kemal in the setup interview unless marked OPEN.

- **2.1 DECIDED: kit feedback, standing approval.** Kemal wrote the kit himself and files its issues from his own GitHub account; no need to ask before sending.
- **2.2 DECIDED: the repository goes public.** Order: setup interview → personal data into `private/` → rewrite the two-commit history without it → licence → push, with Kemal's yes at the push.
- **2.3 DECIDED: personal data lives in git-ignored `private/`, synced to Cloudflare R2** (Kemal's free 10 GB bucket), so work continues on other devices. The sync itself is Phase 2.
- **2.4 DECIDED: own uv environment** (`pyproject.toml`, `uv.lock`): the public repository must carry its environment instead of borrowing a venv outside it.
- **2.5 DECIDED: gates are ruff + pytest + boundary checks.** Ruff runs the real-bug rules only (E9, F): the code is deliberately compact.
- **2.6 DECIDED: risky areas** are Rekordbox DB writes, the harmony check, privacy/public split and deletions (`AGENTS.md`).
- **2.7 DECIDED: four boundaries enforced by grep** (`docs/ARCHITECTURE.md`, "Boundary enforcement").
- **2.8 DECIDED: Claude only (solo).** No Codex subscription; revisit if that changes. Reviewer pinned to `claude-opus-5-5`.
- **2.9 DECIDED: AI tools may be credited in commits.**
- **2.10 DECIDED: Claude Code overlay installed; ponytail on; clangd-lsp off here; caveman and cc-plugin-you-should-know kept on** (Kemal's choice, against the agent's suggestion).
- **2.11 DECIDED: pyrekordbox 0.4.4 and `CLAUDE_CODE_SUBAGENT_EFFORT=medium`** (`RESEARCH_LOG.md`).
- **2.12 DECIDED: Claude quits and reopens Rekordbox itself** around a DB write; Kemal is not asked to.
- **2.13 DECIDED: everything in the repository is English**, the music and Rekordbox rules and the dj-set skill included (public readers). Cue comments shown on the deck stay Turkish. Chat with Kemal stays Turkish.
- **2.14 DECIDED: MIT licence** (`LICENSE`).

