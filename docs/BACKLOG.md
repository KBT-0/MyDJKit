# BACKLOG.md — Next and Parked Work (MyDJKit)

What is planned but not started, and what was put aside on purpose. Read it when the next
task is chosen, NOT at every session start: `docs/STATE.md` holds only what is in flight.
When work on a task starts, its line moves to `docs/STATE.md` and leaves this file.

---

## Next tasks (priority order)

- `hooks/gate.py`: also print the audit output when the audit passes, so the "private/sets.json yok" warning reaches the agent (needs its own review: hook).
- `djasistan/audit.py:13`: drop the leftover local imports in `banned_artists()`.
- Phase 2: R2 sync script for `private/` (rclone is installed; no remote configured yet).

## Deferred / parked
