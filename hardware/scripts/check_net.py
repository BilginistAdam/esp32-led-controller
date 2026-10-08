import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sexp import *
from design import PARTS
n=parse(open('ledctl.net').read())
nets=find(n,'nets')[0]
got={}; types={}
for net in find(nets,'net'):
    name=find(net,'name')[0][1].lstrip('/')
    nodes=find(net,'node')
    for nd in nodes:
        r,p=find(nd,'ref')[0][1],find(nd,'pin')[0][1]
        got[(r,p)]=name
        t=find(nd,'pintype'); types.setdefault(name,[]).append(t[0][1] if t else '?')
    real=[x for x in nodes]
    if len({find(x,'ref')[0][1] for x in nodes})<2 and not name.startswith('unconnected'): print('SINGLE-PART NET',name)
bad=0
for ref,(l,s,v,fp,pos,c) in PARTS.items():
    if ref.startswith("#"): continue
    for p,nn in c.items():
        if got.get((ref,p))!=nn: print('MISMATCH',ref,p,nn,got.get((ref,p))); bad+=1
# mini ERC: power_in nets need a power_out
for name,ts in types.items():
    if 'power_in' in ts and 'power_out' not in ts and name not in ('GND','+3V3','VBUCK'): print('ERC: power_in not driven on',name)  # these carry PWR_FLAGs
    if ts.count('output')>1: print('ERC: multiple outputs on',name)
print('mismatches:',bad,'| nets:',len([k for k in types if not k.startswith('unconnected')]))
