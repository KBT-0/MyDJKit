# Phases — what we are building now, and what we are deliberately not

Read every session: the CURRENT phase in full, every later phase in one line. When a phase
closes, its permanent findings move to their homes and its detail is deleted; its history
stays in git (other kits archive a finished plan instead; this one harvests and deletes). The
reasons are in `docs/WORKFLOW.md`, "The state, backlog and phase files".

---

## Current phase: Phase 1: sixteen blendable sets in Rekordbox

**What it must find out:** Can all 16 sets be written into Rekordbox safely, arc intact, with at least 80% of transitions blendable?

<!-- State what the phase must find out or which risk it retires, in one sentence (a
     question is a good form, not a requirement). If it cannot be put in one sentence, split
     the phase. A kit choice; no study measured it. -->

**In scope**

- Download and import the candidate tracks (gamdl → Rekordbox collection), Analyze Tracks.
- `select_sets.py` + `djasistan.audit` for every set; replace incompatible tracks with same-genre candidates.
- `djasistan/rbwrite.py` / apply step: playlist contents by ID (names kept), B–E hot cues on empty pads.
- `set_plan.json`, m3u8 and CSV per set; the set guide rendered from the plans.
- Verify (integrity, order, cues) and a per-set "blendable x/y" report.
- Split personal data into `private/`, clean the git history, choose a licence, publish the repository.

**NOT in scope — do not build these yet**

- R2 sync of `private/` → Phase 2.
- New set types or genres → Phase 2.
- Automatic transition/effect suggestions → later, not decided.
- Audio analysis outside Rekordbox → rejected (`docs/WORKFLOW.md`, "Evaluated and rejected").

<!-- Spend as much effort here as on the list above. Each entry names the phase it belongs to
     instead, so "not yet" does not read as "never". An agent that finds itself needing
     something on this list STOPS and reports rather than quietly widening the phase.
     Sources: non-goals in Google design docs (industrialempathy.com/posts/design-docs-at-google);
     GitHub Spec Kit, spec-driven.md; Anthropic's prompting guide on overeagerness. Naming
     the phase each entry belongs to is the kit's addition. -->

**Done when**

- `uv run python -m djasistan.audit state/pending_sets.json` reports ≥80% for every one of the 16 sets.
- The verify script reports integrity ok, every playlist in the planned order, no existing cue changed.
- The set guide lists all 16 sets. Kemal opens Rekordbox and confirms the playlists look right.

<!-- Commands or observations, never adjectives. "The simulation runs 100 days at seed 42
     with no price outside its declared band" is a criterion. "The economy feels balanced" is
     not — unless it names WHO decides and when, which makes a subjective criterion valid.
     An unowned subjective criterion is not a criterion. -->

---

## After this one

<!-- One line per phase, in order, and no more than a line. What it will find out is
     enough; scope and criteria are written when it becomes current. Reordering this list is
     a decision and belongs in docs/PROJECT.md with its reasoning — this is the view, not the
     authority. Sources: rolling-wave planning (detail when a stage becomes near); an
     architecture decision record is superseded, not edited (Nygard, cognitect.com 2011). -->

- Phase 2: can Kemal continue the work on another device (R2 sync of `private/`), and which new sets come next?
