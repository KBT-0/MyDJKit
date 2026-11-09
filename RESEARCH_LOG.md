# Research log

## 2026-11-09: setup pass (Claude Code 2.1.321, codex-cli 0.162.1)

Baseline: the kit's `docs/research/README.md`, newest report 2026-10-22.

- **ACCEPTED: pyrekordbox 0.4.3 → 0.4.4** in the rekordbox-mcp venv (the DB reader/writer). The owner asked for it.
  The changelog for 0.4.4 was not verified. A read test against a copy of `master.db` passed (3730 tracks,
  58 playlists). The write path has not been exercised on 0.4.4 yet: the first apply run is the test, behind the
  usual backup → staged copy → integrity check. Reopen if a write misbehaves: pin back to 0.4.3.
- **ACCEPTED: `CLAUDE_CODE_SUBAGENT_EFFORT=medium`** (Claude Code 2.1.316) in `.claude/settings.json` `env`.
  It sets subagents' effort apart from the lead's. The owner wants it in the kit too and is passing it to the kit lead.
- Noted, no action: 2.1.318 moves a background subagent's long shell command to the background after 3 minutes
  (the cache stays warm); 2.1.317 gives a subagent on another model that model's saved effort.
- Not found: a gamdl changelog (the search returned nothing relevant). Not run: the rest of the Claude Code
  changelog past its first 100k characters.

## 2026-11-10: project research via NotebookLM deep research (two notebooks, 52 cited sources)

Queries carried only generic DJ topics, no personal data. Notebooks: "DJ set automation: tools & repos",
"DJ set building: technical tricks". Findings below are NotebookLM's synthesis, not independently re-checked unless noted.

Tools (default verdict REJECT; none adopted yet):
- `rbox` (Rust, Python bindings, by pyrekordbox's author; master.db + ANLZ read/write): a possible successor to pyrekordbox. Reopen if pyrekordbox breaks on a Rekordbox update.
- `rekordbox-mcp` (already in use as the venv source; backups before mutation). No change.
- `sean-a-wilson/rekordbox-skills` (Claude Code skills: playlist dedupe, upgrade finder): not this phase.
- SonoVault API (BPM/key/ISRC lookups for 90M tracks): rejected; Rekordbox's own analysis is what the decks play.
- Karakaya & Ergül Aydın 2024 (MILP + greedy for harmonic playlists): their model is close to `engine.solve`; nothing to adopt.

Techniques worth acting on (each needs Kemal's decision before it changes a rule):
1. Diagonal moves An ↔ B(n±1) share 6 of 7 scale notes (checked by hand: 8A=A minor and 7B=F major differ only by B/Bb).
   Today `camelot.key_ok` rejects them. Allowing them raises blendable transitions without real clashes.
2. +2 and +7 are "energy boost" moves: blend fast, mostly for the peak. Could count as allowed only in the peak part of the arc.
3. Without key lock, +6% tempo = +1 semitone = +7 on the wheel. Our ≤4% limit keeps keys intact only with key lock (Master Tempo) on.
4. Key detection: relative major/minor confusion is harmless (same notes); half/double BPM errors are already tolerated.
5. Hot cues written only to master.db show in Rekordbox but not on a CDJ/USB export (ANLZ files hold those). Irrelevant while
   Kemal plays a DDJ-FLX4 from the laptop; relevant if he ever exports to USB.
6. Rekordbox Cloud Library Sync can overwrite offline edits. Unknown whether Kemal uses it.
7. Alternative write path: generate a Rekordbox XML and import it in the GUI; slower, but no DB write at all.
