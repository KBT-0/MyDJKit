"""Audit a set: how many neighbouring tracks are BPM + key compatible. Used by the gate hook and by hand.

Usage: python -m djasistan.audit state/pending_sets.json
pending_sets.json = {"<set>": [{"title","artist","bpm","key"}, ...], ...}
"""
import json,sys
from pathlib import Path
from .camelot import key_ok,boost_ok,tempo_gap,cam
MIN_RATIO=.80          # at least 80% of transitions must be blendable
MAX_TEMPO_GAP=.04      # ±4% pitch (half/double time allowed)
def banned_artists():
    """Each user's own list: `exclude_artists` in private/sets.json (git-ignored). None there -> nothing banned."""
    import json; from pathlib import Path
    f=Path(__file__).resolve().parents[1]/'private/sets.json'
    return tuple(a.casefold() for a in json.loads(f.read_text()).get('exclude_artists',[])) if f.exists() else ()
PEAK=(.5,.85)          # share of the set where +2/+7 energy boosts count as blendable
# shortcut: engine.solve does not seek boosts, it only stops being penalised for them here; teach the solver if peaks stay flat
def check(tracks,banned_list=None):
    ban=banned_artists() if banned_list is None else banned_list
    pairs=list(zip(tracks,tracks[1:]))
    peak=lambda i:PEAK[0]<=(i+1)/len(tracks)<PEAK[1]   # position of the incoming track
    bad=[(i+1,a,b) for i,(a,b) in enumerate(pairs) if not ((key_ok(a['key'],b['key']) or (peak(i) and boost_ok(a['key'],b['key']))) and tempo_gap(a['bpm'],b['bpm'])<=MAX_TEMPO_GAP)]
    banned=[t for t in tracks if any(x in (t.get('artist') or '').casefold() for x in ban)]
    ratio=1-len(bad)/max(len(pairs),1)
    return ratio,bad,banned
def main(path):
    sets=json.load(open(path)); ok=True
    if not (Path(__file__).resolve().parents[1]/'private/sets.json').exists():
        print('UYARI: private/sets.json yok: yasaklı sanatçı listesi bu cihazda uygulanmıyor (private/ klasörünü kopyala).')
    for name,tracks in sets.items():
        ratio,bad,banned=check(tracks)
        fail=ratio<MIN_RATIO or banned
        ok&=not fail
        print(f"{'FAIL' if fail else 'OK  '} {name}: {len(tracks)-1-len(bad)}/{len(tracks)-1} uyumlu geçiş ({ratio:.0%})"+(f", yasaklı sanatçı: {[t['artist'] for t in banned]}" if banned else ''))
        for i,a,b in bad: print(f"     {i:2d}. {a['title'][:30]} ({a['bpm']:.0f} {cam(a['key'])}) -> {b['title'][:30]} ({b['bpm']:.0f} {cam(b['key'])})")
    return ok
if __name__=='__main__': sys.exit(0 if main(sys.argv[1]) else 1)
