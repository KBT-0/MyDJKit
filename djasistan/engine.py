"""Pick and order a set: keep each track near its place in the story, maximise BPM+key compatible neighbours."""
from .camelot import key_ok,tempo_gap
def edge(a,b):
    g=tempo_gap(a['bpm'],b['bpm']); k=key_ok(a['key'],b['key'])
    if k and g<=.04: s=10-g*50          # blendable; closer tempo is better
    elif k and g<=.06: s=1
    else: s=-8
    if a['artist'] and a['artist']==b['artist']: s-=4
    return s,(k and g<=.04)
def place_pen(item,i,L):
    q=i/max(L-1,1); d=abs(item['p']-q)
    return -40*max(0,d-.18)             # free to move inside its part of the arc
def solve(items,L,width=3000,first=None,last=None):
    """items: dicts with id,bpm,key,p (0..1 arc position),orig,artist,group(optional same-song key)."""
    n=len(items); E=[[edge(a,b)[0] for b in items] for a in items]
    start=[first] if first is not None else range(n)
    beam=[(place_pen(items[s],0,L)+(3 if items[s]['orig'] else 0),(s,),frozenset([items[s].get('group',s)])) for s in start]
    for i in range(1,L):
        nxt={}
        for sc,seq,used in beam:
            cur=seq[-1]
            for j in range(n):
                g=items[j].get('group',j)
                if g in used: continue
                if last is not None and ((i==L-1)!=(j==last)): continue
                s=sc+E[cur][j]+place_pen(items[j],i,L)+(3 if items[j]['orig'] else 0)
                k=(used|{g},j)
                if k not in nxt or nxt[k][0]<s: nxt[k]=(s,seq+(j,),used|{g})
        beam=sorted(nxt.values(),key=lambda x:-x[0])[:width]
    sc,seq,_=beam[0]
    return [items[j] for j in seq],sum(edge(items[a],items[b])[1] for a,b in zip(seq,seq[1:]))
