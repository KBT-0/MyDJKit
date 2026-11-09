---
name: dj-set
description: Build a BPM/key-compatible DJ set for Rekordbox, audit or repair an existing set, download missing tracks from Apple Music (gamdl). Use for set, playlist, transition, hot cue and "order compatibly" requests (Turkish too: set, geçiş, uyumlu sırala).
---
# Building a DJ set

1. **Direction**: settle genre/mood/venue with Kemal (one question). Write the set's arc as 3–4 parts.
2. **Candidate pool**: first the Rekordbox library (`rbread.connect()` + folder filter, `libpool.pool`), then
   Apple Music candidates (`lists/*.txt`, one `part|Artist - Title` per line). Aim for ~1.3× the target track count.
3. **Download**: match through the Apple Music API (gamdl `AppleMusicApi.get_search_results`, not iTunes Search: rate limit),
   download with gamdl, 3 in parallel. Never re-download what the library already has.
4. **Import**: quit Rekordbox yourself (`osascript -e 'quit app "rekordbox"'`), add the files to the collection
   (pyrekordbox, staged DB), reopen it. Analyze Tracks is a GUI step: ask Kemal if it cannot be automated.
5. **Pick + order**: `engine.solve(items, L)`: each track carries `p` (its place on the arc, 0..1), `orig`, `group`
   (blocks repeats of the same song). Compatible transition +10, incompatible −8, same artist back to back −4,
   moving more than 18% from its arc place is penalised.
6. **Audit**: write the result to `state/pending_sets.json`, run `uv run python -m djasistan.audit state/pending_sets.json`.
   Continue at ≥80% compatible and no banned artist; otherwise widen the pool (same genre, candidates for the missing key/BPM region).
7. **Install**: playlist + B–E cues. The cue comments stay as Kemal reads them on the deck:
   `START`, `4 BAR SAY`, `HAZIRLIK 4 BAR`, `GECIS BASLA`, `DEVIR / SON`.
   The gate hook blocks the write while Rekordbox runs or the audit has not passed.
8. **Guide**: set plan + transition notes (blend: shared tempo, pitch %; phrase: hand over at the end of a phrase) in the HTML guide.

When reporting, give "compatible transitions x/y" per set; if the number is low, say so plainly.
