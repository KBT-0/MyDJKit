"""Key name -> Camelot, and the DJ compatibility rules shared by the audit and the reorder."""
import re
MAJ={'B':'1B','F#':'2B','Gb':'2B','Db':'3B','C#':'3B','Ab':'4B','G#':'4B','Eb':'5B','D#':'5B','Bb':'6B','A#':'6B','F':'7B','C':'8B','G':'9B','D':'10B','A':'11B','E':'12B'}
MIN={'Abm':'1A','G#m':'1A','Ebm':'2A','D#m':'2A','Bbm':'3A','A#m':'3A','Fm':'4A','Cm':'5A','Gm':'6A','Dm':'7A','Am':'8A','Em':'9A','Bm':'10A','F#m':'11A','Gbm':'11A','Dbm':'12A','C#m':'12A'}
def cam(k):
    if not k: return None
    k=k.strip()
    if re.fullmatch(r'\d{1,2}[AB]',k): return k
    return MIN.get(k) or MAJ.get(k)
def key_ok(a,b):
    a,b=cam(a),cam(b)
    if not a or not b: return False
    an,al,bn,bl=int(a[:-1]),a[-1],int(b[:-1]),b[-1]
    d=(bn-an)%12
    # same letter ±1, A<->B same number, or diagonal An<->B(n±1): all share 6-7 of 7 scale notes
    return (al==bl and d in (0,1,11)) or an==bn or (al!=bl and d in (1,11))
def boost_ok(a,b):
    """Energy-boost move a->b: +2 or +7 on the same ring. Allowed only at the set's peak (audit.PEAK)."""
    a,b=cam(a),cam(b)
    return bool(a and b) and a[-1]==b[-1] and (int(b[:-1])-int(a[:-1]))%12 in (2,7)
def tempo_gap(a,b):
    """Smallest relative gap allowing half/double time."""
    return min(abs(a*f/b-1) for f in (1,2,.5))
assert key_ok('Am','8A') and key_ok('8A','9A') and key_ok('8A','8B') and not key_ok('8A','10A') and key_ok('12A','1A') and key_ok('8A','9B') and key_ok('8A','7B') and not key_ok('8A','10B')
