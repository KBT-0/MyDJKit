# MyDJKit — Agent Constitution

Every agent, any tool or model, reads this file first; every line binds, and each pointer names
the section that holds the how. A tree's own `AGENTS.md` (`docs/AGENTS.md` for `docs/`) is read
before you edit that tree. **Started by another agent** (sub-agent, reviewer, briefed session)?
Keep the HARD RULES and the STOP and MENTION ONCE lists, raised to the agent that started you;
the brief names what to read, so it skips the reading order and the rest of "Duties". It
leaves `docs/STATE.md` to the lead and reports to the agent that started it. One started without this file
(the diff reviewer, `omitClaudeMd`) follows its own definition instead.

## What this project is

MyDJKit is a personal DJ assistant for a DDJ-FLX4 + Rekordbox 7 setup. It picks and orders
tracks by BPM and Camelot key compatibility (at least 80% of transitions blendable), keeps each
set's arc (intro → build → peak → close), downloads missing candidates from Apple Music with
gamdl, and writes the result safely into the Rekordbox database: playlists, hot cues and a
set guide. One user today. The repository is going PUBLIC: code and rules are shared, while
personal data (set definitions, plans, guide, session notes) lives in a git-ignored
`private/` folder synced to Cloudflare R2.

### Project rules (owner-authored; non-negotiable)

Set building follows `.claude/skills/dj-set/SKILL.md`.

**Music**
- **Pick by BPM and key compatibility.** Writing a list and sorting it afterwards is not enough. Neighbouring tracks must be
  Camelot-compatible (same key, ±1 on the same letter, A↔B on the same number, diagonal An↔B(n±1); in the set's peak,
  50–85% of the way through, a +2 or +7 energy boost also counts) with a tempo gap ≤4% (half/double time counts).
  Target: at least 80% of transitions blendable. `djasistan/audit.py` measures it and the gate hook enforces it.
- Keep each set's arc (intro → build → peak → close). Fix compatibility by swapping an incompatible track for a compatible
  one of the same genre (`engine.solve`, with a placement penalty), not by moving tracks far along the arc.
- Candidate pool: first Kemal's analysed library (Rekordbox already has BPM/key), then Apple Music via gamdl. Download
  ~30% more candidates than needed; the ones that do not fit are not deleted, they just stay out of the playlist.
- No run of over-familiar hits; favour deep cuts and artist variety. Never fill a set with one artist.
- Ask Kemal about direction and genre; make the detailed picks (tracks, order) yourself.
- **Personal taste rules** (banned artists, what a set name means, length limits) are each user's own and live in
  git-ignored `private/`: read `private/PREFERENCES.md` before set work; banned artists are `exclude_artists` in
  `private/sets.json`, which the code enforces. Never write such a rule into a tracked file.

**Rekordbox safety**
- Write to the DB only while Rekordbox is CLOSED: back up → change a staged copy → check integrity and that existing rows
  are unchanged → `os.replace` it live. Existing cues are never changed.
- Beat grid, BPM and key analysis happen in the Rekordbox GUI (Analyze Tracks).
- Hot cue pads: A=Kind 1, B=2, C=3, D=5, E=6 (Kind 4 is not a visible pad). The contentCue bundle must be updated too.
- Keep Kemal's playlist names (some were renamed by hand); update contents by playlist ID.

**Privacy**
- gamdl uses only `~/.gamdl/cookies.txt` (apple.com lines only). Never touch browser profile or cookie folders.
- The account e-mail is never sent to an outside service.

**Design authority is `docs/PROJECT.md`** (items DECIDED or OPEN, read by section). This file is
canonical (tool files only point here); cross-tool memory is `docs/STATE.md` only; CI runs the
same `./scripts/check.sh`; task transfer is `docs/HANDOFF.md`.

## Reading order (new session)

1. `./scripts/doctor.sh` (changes nothing; not for a small fix, see the checklist); on `MISSING:` tell
   Kemal and offer each fix first.
   This file is read once; do not open it again.
2. `docs/PHASES.md` (now, and what is OUT of scope); `docs/STATE.md`: its "Active work" and
   "Blocked" sections (updating it at session end is YOUR job).
3. `docs/ARCHITECTURE.md`: read it when the task crosses a module boundary or the folder's
   `AGENTS.md` / `README.md` does not say where the code lives; one SECTION of `docs/PROJECT.md`
   by its Contents, cited by number (`PROJECT §4.2`), never loaded whole.
4. The target folder's `AGENTS.md` / module `README.md`.

The session Kemal opens is the lead. Once per session it reads `docs/COMMUNICATION.md` and `docs/WORKFLOW.md`,
"Worker cost", its first block "The rules in brief". When needed: `docs/GOTCHAS.md` (paid-for
traps) when something behaves unexpectedly, `docs/BACKLOG.md` for the next task.

## HARD RULES (violation = failed task)

### Design authority

- Never contradict a DECIDED item of `docs/PROJECT.md`; never decide an OPEN one: flag it as a
  question for Kemal and go on with work that does not depend on it. Agents propose
  options with trade-offs; only Kemal marks DECIDED. Needing something on the
  `docs/PHASES.md` out-of-scope list is a STOP.

### Architecture boundaries (most are also compiler/CI-enforced)

- The harmony core (`djasistan/camelot.py`, `audit.py`, `engine.py`) never imports `pyrekordbox`
  or `sqlcipher3`, so it stays testable without Rekordbox (gate: `scripts/boundary_checks.sh`).
- Only `djasistan/rbwrite.py` writes the Rekordbox database (`.commit(`, `os.replace(`); every
  other project file only reads it (gate).
- No code touches browser profile or cookie folders; gamdl uses only `~/.gamdl/cookies.txt` (gate).
- No personal data in tracked files: no e-mail address, no `/Users/<name>` path, nothing under
  `private/` (gate; this repository is public).

- Cross-module access only through public contracts; propose a contract change instead.
- Any third-party dependency needs Kemal's approval.

### Task discipline

- One change in one module, inside the brief's `Owns:` paths; more is a STOP (split, report).
  No drive-by refactors; a tidy inside a line you had to change is part of the task. A second
  bug of the same cause in a file the task changes is part of the task too: fix it with its test
  and say so; one elsewhere is reported.
- No push, PR or remote update without Kemal's word in this session.
- A git command line holding `--out`, `--ext`, `--textc` or `--sub`, a commit message included,
  is denied (`.claude/settings.json`): write the message, in a step of its own (the denial reads the whole
  command line), to a `mktemp` file (PowerShell: `New-TemporaryFile`; a fixed name like
  `/tmp/msg.txt` is shared with parallel sessions) and `git commit -F FILE`.
- **Commit or stash BEFORE any command that discards work**, after `git status`; a recursive
  delete first proves it owns the folder (`docs/WORKFLOW.md`, "Destructive commands").
- **Never end running work** unless Kemal asked or it is provably finished or hung
  (`docs/WORKFLOW.md`, "Ending running work").
- **A bug you can fix now is fixed now**; a reviewer's finding follows `docs/REVIEW_GATE.md`,
  "Verdicts and who decides".
- No untested code enters `djasistan/` and `hooks/`: a logic change brings its test; `./scripts/check.sh`
  must PASS before you finish; plugin advice never replaces these rules. A test runs in its own
  command, read before any commit: never `test; git commit`, never piped through a filter. The
  commit hook runs `./scripts/check.sh` and refuses a red commit: do not also run it by hand; a task that ends without a commit runs it. A
  commit whose output lacks the gate's `CHECK: PASS` line ran no gate (an unwired clone,
  `docs/DEV_SETUP.md`): run it then and say the hook is unwired.
- **Read narrow:** grep or a range first, never a whole log, spill file or file over 300 lines; filter long output.
- **Never `git commit --no-verify`** or another way past the gate; a red gate is fixed or
  reported. AI tools may be credited in commit messages (a `Co-Authored-By:` trailer is fine):
  the owner allowed it at setup (`docs/PROJECT.md`).
- Look for a system that does the job (`docs/ARCHITECTURE.md`, the code) before writing one; a
  changed public API updates its module README in the same task.
- **Gates must be proven RED** (`docs/WORKFLOW.md`, "Writing a gate"). `docs/STATE.md` edits follow
  `docs/AGENTS.md`, "STATE.md discipline".

### Review gate and validation honesty

- **Risky diffs** (Rekordbox database writes (`djasistan/rbwrite.py`, `djasistan/rbread.py`, `hooks/gate.py`), the harmony check (`djasistan/camelot.py`, `audit.py`, `engine.py`), privacy and the public/private split (gamdl calls, R2 sync, `.gitignore`), and deletions (playlists, candidate audio, plan folders), plus gates/CI/check scripts/review tooling) pass the review
  gate before they reach the main branch; others get their tier's review (`docs/REVIEW_GATE.md`,
  "Risk tiers"). It starts unasked, when `docs/REVIEW_GATE.md` (its opening) says; in Claude Code a
  commit or merge changing a `risky_paths` file whose content no review accepted is refused. A
  FRESH session reviews, never the author
  (`docs/REVIEW_GATE.md`, "Invariant", "Rounds"). A verdict's manual checks go to `docs/STATE.md`.
- **Never report a verification you did not run**; say "not run".

### Language & style

- **Docs, code, identifiers, comments, commits and STATE.md: English.** 
- **Two registers; rule 3 outranks both.** (1) Chat in Turkish: the answer first, then
  stop (`docs/COMMUNICATION.md` binds every message Kemal reads). (2) Written artifacts:
  full sentences, the actor named ("The two registers"). (3) Never cut by a cap or a style: what
  FAILED, what was NOT run or verified, a security warning, an action that cannot be undone — in full,
  on its own line, in any language.
- One job per file and class; a file too large to read in one pass is a decay signal: report it.
  No hidden global state in core logic (dependencies, clock, randomness via the constructor). Short
  doc comments on public APIs; name things well instead of compensating with comments.

## Duties toward Kemal

**Default is silence**: if nothing below applies, work and say nothing about rules. **Never
repeat** a closed point: once acknowledged, overridden or passed over, a point is closed for the
session. **A question is not an order:** a question, or another model's output Kemal pastes,
is answered and discussed; files change only on an explicit go-ahead. **A one-off decision ends with its moment**
(`docs/COMMUNICATION.md`, "Questions and approvals"). **A short yes to a proposed hand-off is the
hand-off:** "go on" or a model name means update STATE, write the handoff, end with the new
session's opening prompt in a code block (`docs/COMMUNICATION.md`, "Handoff") and stop; new work
there needs an explicit "start it here". **Settled is done, not offered:** what Kemal decided
or the rules settle is done and reported; a question is only for an open decision. Kit feedback
under `kit_feedback: standing-approval` is sent while Kemal is present (autopilot keeps it
as a draft), and a settings file a tool rewrote itself is the lead's to take through its tier's
review (`docs/REVIEW_GATE.md`, "Risk tiers") and commit, never handed back to Kemal.

### STOP — pause the work and ask (rare)

- A "Design authority" rule would break, or a new dependency or MCP server is needed → name it and ask;
  never silently comply or refuse.
- A required verification cannot be run → "not run", stop; an unavailable reviewer stops only the
  affected approval, commit or release (`docs/REVIEW_RUNNING.md`, "Unavailable reviewer").
- Parallel work on unfrozen contracts or against the worktree policy (`docs/WORKFLOW.md`, the four
  "Parallel work" sections) → flag it first.
- A test deleted, skipped or weakened unasked, or a gate changed without a new red proof
  (`docs/WORKFLOW.md`, "Decay early-warning system").
- A Rekordbox database write without a fresh backup, or while Rekordbox runs → STOP. Quit it yourself
  first (`osascript -e 'quit app "rekordbox"'`) and reopen it after; do not ask Kemal to.
- Changing or deleting an existing cue, or renaming a playlist Kemal named → STOP and ask.
- Deleting audio files, playlists or plan folders the task does not list → STOP and ask.
- A push to a public remote, or anything leaving the machine with personal data (e-mail, cookies,
  `private/` content) → STOP and ask.
- A set's direction or genre → ask; track picks and their order are the agent's call.

### MENTION ONCE — one line in your closing summary, never mid-work

- Risky area touched → "review gate applies before the merge (in a single session on the main branch, before the commit)".
- A duplicate system, a README contradicting its API, a two-job file, a task spanning modules, a
  procedure done a third time (a skill), bulk work fit for a cheaper model.
- Context past 200k → no new round; 300k: `/compact` or a hand-off; 400k: stop
  (`docs/WORKFLOW.md`, "Worker cost", rule 8).
- A repeated cost with a cheaper way around it, with a number from `scripts/agent_cost.py`; never hunt for savings.
- **Something about the FOUNDATION itself was wrong, unclear or missing** — a gate that
  failed open, a rule that did not survive contact with real work, an ambiguous setup
  instruction, a document contradicting itself → offer to send it upstream with
  `/myagentkit:kit-feedback`. It scrubs this project out and shows the exact text; the line
  below says whether it then waits for a yes. Collect findings during the session and offer
  them ONCE, at its end, as one batch per area; take no for an answer, never send on your
  own initiative. Keep it light: a footnote in a closing summary, not a
  campaign.
  `kit_feedback: standing-approval`

## Task completion checklist

One module; `./scripts/check.sh` PASS; no boundary, DECIDED or scope conflict; README matches the API;
`docs/STATE.md` updated with a tool+model trace; a short what-and-why summary. A small fix (one commit,
one module; owner 2026-10-25) skips `doctor.sh` and the STATE.md trace and leaves `./scripts/check.sh` to
the commit hook and reads its `CHECK: PASS`; a risky diff still takes its review, and its manual checks still go to STATE.md with their tool+model trace. On compaction keep
open decisions, binding rules, changed files, the next step and Kemal's words verbatim.
