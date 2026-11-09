"""Pick + order every set from Rekordbox data; write state/pending_sets.json (audited by the gate) and state/selection.json."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from djasistan.rbread import connect,playlist,Q
from djasistan.engine import solve
from djasistan.libpool import song_key,norm
from djasistan.camelot import cam,tempo_gap
R=Path(__file__).parent; EV=R.parent/'.dj-tool-evaluation'
cfg=json.load(open(R/'private/sets.json')); BAN=cfg['exclude_artists']
db=connect()
lib=[dict(r) for r in db.execute(Q+" WHERE (c.rb_local_deleted IS NULL OR c.rb_local_deleted=0)")]
by_path={t['FolderPath']:t for t in lib}
def usable(t): return t and t['BPM'] and cam(t['KeyName']) and not any(b in (t['ArtistName'] or '').casefold() for b in BAN)
def it(t,p,orig): return {'id':t['ID'],'bpm':t['BPM']/100,'key':t['KeyName'],'p':p,'orig':orig,'artist':norm((t['ArtistName'] or '').split(',')[0].split(' & ')[0]),'group':song_key(t),'t':t}
orig={s['name']:playlist(db,s['playlist_id']) for s in cfg['sets'] if 'playlist_id' in s}
reserved={song_key(t):n for n,T in orig.items() for t in T}
used=set(); out={}; sel={}
for s in cfg['sets']:
    O=[t for t in orig.get(s['name'],[]) if usable(t)]
    L=s.get('length') or len(orig[s['name']])
    items=[it(t,i/max(len(O)-1,1),True) for i,t in enumerate(O)]
    anchors=[(x['bpm'],x['p']) for x in items]
    for work,stem in s.get('lists',[]):
        man=json.load(open(EV/work/'manifest.json')).get(stem,[])
        ph=json.load(open(EV/work/'phases.json')).get(stem) if (EV/work/'phases.json').exists() else None
        for i,e in enumerate(man):
            t=by_path.get(e.get('path'))
            if not usable(t): continue
            p=(ph[e['reference']]-.5)/4 if ph else i/max(len(man)-1,1)
            items.append(it(t,p,'playlist_id' not in s)); anchors.append((t['BPM']/100,p))
    for t in lib:
        if not any('/My_Playlists/'+f+'/' in t['FolderPath'] for f in s.get('library',[])) or not usable(t): continue
        b=t['BPM']/100; lo,hi=s.get('bpm',[0,999])
        if not lo<=b<=hi: continue
        near=[p for a,p in anchors if tempo_gap(a,b)<=.04]
        if near: items.append(it(t,sum(near)/len(near),False))
    seen=set(); pool=[]
    for x in items:   # one copy per song; never take another set's original or a song already used
        g=x['group']
        if g in seen or g in used or reserved.get(g,s['name'])!=s['name']: continue
        seen.add(g); pool.append(x)
    if len(pool)<2: print(f"{s['name']:28s} havuz boş (indirilenler henüz Rekordbox'ta değil)"); continue
    seq,good=solve(pool,min(L,len(pool)),width=600 if len(pool)>200 else 1500)
    used|={x['group'] for x in seq}
    out[s['name']]=[{'title':x['t']['Title'],'artist':x['t']['ArtistName'] or '','bpm':x['bpm'],'key':x['key'],'id':x['id'],'path':x['t']['FolderPath']} for x in seq]
    sel[s['name']]={'good':good,'n':len(seq),'kept':sum(x['orig'] for x in seq),'orig':len(orig.get(s['name'],[])),'pool':len(pool)}
    print(f"{s['name']:28s} {len(seq):2d} parça  uyumlu {good}/{len(seq)-1}  korunan {sel[s['name']]['kept']}/{sel[s['name']]['orig']}  havuz {len(pool)}",flush=True)
(R/'state').mkdir(exist_ok=True)
json.dump(out,open(R/'state/pending_sets.json','w'),ensure_ascii=False,indent=1)
json.dump(sel,open(R/'state/selection.json','w'),ensure_ascii=False,indent=1)
