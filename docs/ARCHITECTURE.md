# Architecture Map

This file answers **"where does X live?"** It holds boundaries, invariants and who may decide
what, not a description of each file, and agents read it to orient (`AGENTS.md`, reading
order), so it stays short: aim for about 100 lines. If an agent cannot orient with it, look
at this file first; the cause may also be a missing module README. (Sources: matklad,
https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html: keep it short, name invariants and
boundaries; Claude Code memory, https://code.claude.com/docs/en/memory: an instruction file
under 200 lines.)

## Runtime topology

```
gamdl (Apple Music) ──► candidate audio ──► Rekordbox GUI (Analyze Tracks: BPM, key, grid)
                                                   │ master.db (encrypted SQLite)
select_sets.py ◄── rbread.py (read) ◄──────────────┘
      │ state/pending_sets.json
      ▼
audit.py ──► hooks/gate.py (PreToolUse) ──► rbwrite.py (Rekordbox closed) ──► master.db
```
- **Rekordbox GUI**: the only authority on BPM, key and beat grid. Nothing here re-analyses audio.
- **rbread.py**: read-only view of playlists with BPM/key.
- **select_sets.py + engine.py**: decide which tracks and in which order.
- **audit.py + hooks/gate.py**: decide whether a write may happen (≥80% blendable, Rekordbox closed).
- **rbwrite.py** (not written yet): the only writer; backup → staged copy → integrity → `os.replace`.

<!-- A small diagram plus one line per process: what it is, and what authority it has.
     "Which component is allowed to decide X?" must be answerable from this section.
     Sources: matklad (invariants and boundaries code cannot show); Claude Code best
     practices, https://code.claude.com/docs/en/best-practices ("architectural decisions
     specific to your project"). -->

## Repository layout

```
djasistan/        harmony core and Rekordbox access (one package)
hooks/            Claude Code hook: the Rekordbox write gate
tests/            pytest suite and boundary-check fixtures
select_sets.py    pick + order every set into state/pending_sets.json
.claude/skills/   the dj-set skill (the set-building procedure)
private/          personal data, git-ignored, synced to R2 (not in the repo)
state/            run output, git-ignored
docs/ scripts/    kit documents and gates
```

Two documentation subdirectories exist for process output rather than design:

- `docs/reviews/` — raw review-gate output, one file per review
  (`<UTC-timestamp>-<random>-<reviewer>-review.md`), recording the reviewing model and
  whether it is attested, reasoning effort, sandbox mode, limits, scope and base ref.
  Every reviewer writes the same header table and one verdict line, so the records stay
  comparable when the author and reviewer roles swap. Written by the review wrapper and
  never edited afterwards: it is evidence, not a document.
- `docs/worktree-notes/` — progress notes from sessions working on a branch or in a
  worktree, one file per branch, so `docs/STATE.md` never becomes a merge conflict. The
  integrating session folds a note into STATE.md at merge time and deletes it.

## Module map

Each module: its own folder, its own project/build unit, its own README summarising its
public API, its own tests (a kit choice; no study measured this layout). Modules see each
other ONLY through public contracts.

| Module | Responsibility |
|---|---|
| `djasistan/camelot.py` | key → Camelot, key and tempo compatibility rules |
| `djasistan/audit.py` | blendable-transition ratio and banned artists for a set |
| `djasistan/engine.py` | choose and order a set: arc place penalty + compatible neighbours |
| `djasistan/libpool.py` | library candidates for a set, placed on the arc |
| `djasistan/rbread.py` | read-only Rekordbox playlists with BPM/key |
| `djasistan/rbwrite.py` | (planned) the only Rekordbox database writer |
| `hooks/gate.py` | refuse a write while Rekordbox runs or the audit fails |
| `select_sets.py` | run the selection for every set in `private/sets.json` |

<!-- One table per top-level area. Columns: Module | Responsibility | (optional) the design
     document section it implements. One line each — this is a map, not documentation; a
     module's detail lives in its own folder (its AGENTS.md and README), read when work
     there needs it, not here on every read (Claude Code best practices: no file-by-file
     descriptions in an instruction file). -->

## Boundary enforcement (rule ≠ advice)

For each boundary below, state WHAT enforces it — and write "not enforced" where nothing
does. A boundary enforced only by prose is a request, and requests decay; the point of this
section is to make that distinction visible rather than to imply it away. An honest gap gets
closed. A gap everyone assumes is covered does not.

1. Harmony core imports no DB library: grep in `scripts/boundary_checks.sh`, fixture in `tests/boundary_checks_test.sh`.
2. Only `djasistan/rbwrite.py` writes the DB: grep for `.commit(` / `os.replace(` in project code (same files).
   Not enforced: a write through another API (e.g. raw `sqlite3` `executescript`); review catches it.
3. No browser profile/cookie paths: grep (same files).
4. No personal data in tracked files: e-mail and `/Users/<name>` grep, and any file under `private/` (same files).
5. Rekordbox closed and audit ≥80% before a write: `hooks/gate.py` (PreToolUse), tested in `tests/test_rules.py`.

<!-- Numbered list. For each: the rule, and WHAT enforces it — a compiler error, a project
     reference whitelist, a grep in scripts/check.sh. If nothing enforces it, write "not
     enforced" rather than implying otherwise; an honest gap can be closed, a fictional
     gate cannot. Source: OpenAI's harness team enforces its architecture with linters and
     structural tests, not prose (the kit's docs/research/agent-kits-in-practice.md, §2.2);
     the reasoning: the kit's docs/rules-that-enforce.md. -->

## Contract change procedure

A task that wants to change a module's public API: (1) proposes the change in that module's
README; (2) finds the affected modules mechanically (builds or runs the tests of every
module that depends on it, searches for the changed symbol) and lists what it found;
(3) applies it after Kemal's approval. Step 2 is a check, not a reading of the
contract: users come to rely on behaviour no contract promises (Hyrum's Law,
https://www.hyrumslaw.com/), and consumer-driven contract tests find them by running them
(Pact, https://docs.pact.io/).

If a contract changes often, report it: the boundary may be in the wrong place.
