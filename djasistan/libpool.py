"""Library candidates (already analysed) for a set, placed on the arc where originals of similar tempo sit."""
import re,unicodedata
from .camelot import tempo_gap,cam
from .audit import banned_artists
BAN=banned_artists()
norm=lambda s: re.sub(r'[^a-z0-9]','',unicodedata.normalize('NFKD',(s or '').casefold().replace('ı','i')))
def song_key(t): return norm(re.sub(r'\s*[\(\[].*','',t['Title']))+'|'+norm((t['ArtistName'] or '').split(',')[0].split(' & ')[0])
def item(t,p,orig):
    return {'id':t['ID'],'bpm':t['BPM']/100,'key':t['KeyName'],'p':p,'orig':orig,'artist':norm((t['ArtistName'] or '').split(',')[0].split(' & ')[0]),'group':song_key(t),'t':t}
def pool(lib,folders,orig,lo=0,hi=999):
    L=len(orig); out=[]
    seen={song_key(t) for t in orig}
    for t in lib:
        if not any('/My_Playlists/'+f+'/' in t['FolderPath'] for f in folders): continue
        if not t['BPM'] or not cam(t['KeyName']) or any(b in (t['ArtistName'] or '').casefold() for b in BAN): continue
        b=t['BPM']/100
        if not (lo<=b<=hi): continue
        k=song_key(t)
        if k in seen: continue
        near=[i for i,o in enumerate(orig) if tempo_gap(b,o['BPM']/100)<=.04]
        if not near: continue
        seen.add(k); out.append(item(t,sum(near)/len(near)/max(L-1,1),False))
    return out
