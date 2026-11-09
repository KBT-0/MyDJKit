import json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from djasistan.camelot import cam,key_ok,tempo_gap
from djasistan.audit import check
def test_camelot():
    assert cam('Am')=='8A' and cam('C')=='8B' and cam('F#m')=='11A' and cam('8A')=='8A'
    assert key_ok('8A','9A') and key_ok('12A','1A') and key_ok('8A','8B') and not key_ok('8A','10A')
def test_tempo_half_double():
    assert tempo_gap(140,70)==0 and tempo_gap(124,128)<.04 and tempo_gap(90,120)>.04
def test_audit_flags_bad_and_banned():
    t=[{'title':'a','artist':'x','bpm':124,'key':'8A'},{'title':'b','artist':'Banned Artist','bpm':124,'key':'9A'},{'title':'c','artist':'y','bpm':100,'key':'2A'}]
    ratio,bad,banned=check(t,('banned artist',))
    assert ratio==.5 and len(bad)==1 and len(banned)==1
def test_gate_ignores_other_commands():
    gate=Path(__file__).resolve().parents[1]/'hooks/gate.py'
    p=subprocess.run([sys.executable,str(gate)],input=json.dumps({'tool_input':{'command':'ls'}}),capture_output=True,text=True)
    assert p.returncode==0 and p.stdout==''
    for c in ('cat > x <<EOF\nrun install.py later\nEOF','grep install.py notes.md'):
        p=subprocess.run([sys.executable,str(gate)],input=json.dumps({'tool_input':{'command':c}}),capture_output=True,text=True)
        assert p.stdout=='',c
def test_gate_catches_real_runs():
    import re
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'hooks'))
    W=re.compile(open(Path(__file__).resolve().parents[1]/'hooks/gate.py').read().split("WRITERS=re.compile(r'")[1].split("')")[0])
    assert W.search('../rekordbox-mcp/.venv/bin/python install.py') and W.search('python3 -I apply_sets.py')
def test_diagonal_and_peak_boost():
    from djasistan.camelot import boost_ok
    assert key_ok('8A','9B') and key_ok('9B','8A') and key_ok('8B','7A') and not key_ok('8A','10B')
    assert boost_ok('8A','10A') and boost_ok('8A','3A') and not boost_ok('8A','10B') and not boost_ok('10A','8A')
    t=lambda k:{'title':k,'artist':k,'bpm':124,'key':k}
    early=[t('8A'),t('10A')]+[t('10A')]*8           # +2 at the start: not blendable
    peak=[t('8A')]*6+[t('10A')]*4                     # +2 at 5/9 of the set: blendable
    assert check(early)[0]<1 and check(peak)[0]==1
    def at(j):  # 21 tracks, one +2 boost into track j+1 (position (j+1)/21)
        return [t('8A')]*(j+1)+[t('10A')]*(20-j)
    assert check(at(9))[0]<1 and check(at(10))[0]==1 and check(at(16))[0]==1 and check(at(17))[0]<1
if __name__=='__main__':
    for n,f in list(globals().items()):
        if n.startswith('test_'): f()
    print('ALL TESTS PASS')
