# STATE.md — Cross-Session Work State (MyDJKit)

**If it is not written here, it did not happen.** This file holds current state only: what
is in flight and what waits on someone. Its rules, and the permanent home for anything still
true next month, are in `docs/AGENTS.md`, "STATE.md discipline" (the reasons: `docs/WORKFLOW.md`,
"The state, backlog and phase files"). Every entry has a tool+model trace.

---

**Working mode:** solo (`docs/WORKFLOW.md`, "Working modes, by name"; `/myagentkit:mode` switches it).

## Active work

- Phase 1 set work: candidate downloads running (gamdl), then import → Analyze Tracks → select → audit → apply.
  Detailed, personal notes: `private/SESSION_NOTES.md` (git-ignored). [Claude Code, claude-opus-5-5, 2026-11-10]
- NotebookLM deep research (tools/repos and technical techniques) running; findings go to `RESEARCH_LOG.md`.
- Kit setup: files filled, gate run pending, fresh review of the setup diff pending before the first commit.

## Blocked / waiting on Kemal

- Approval of the push to a public GitHub repository. Before it: a fresh root commit (old history holds personal data)
  and a noreply author e-mail; verify `git log -p` of the pushed branch shows no playlist ID, city, banned artist or e-mail.

## Known issues / watch out

Environment and tooling traps have a permanent home: **`docs/GOTCHAS.md`**. Read it when
something behaves unexpectedly. What belongs here instead is a check that is outstanding
RIGHT NOW — a manual verification owed before the next commit, a claim that has not been
observed yet.

