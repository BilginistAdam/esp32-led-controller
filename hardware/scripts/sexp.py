import re
TOK=re.compile(r'\s*(\(|\)|"(?:[^"\\]|\\.)*"|[^\s()"]+)')
class Sym(str): pass
def parse(text):
    pos=0; stack=[[]]
    for m in TOK.finditer(text):
        t=m.group(1)
        if t=='(':
            stack.append([])
        elif t==')':
            x=stack.pop(); stack[-1].append(x)
        elif t[0]=='"':
            stack[-1].append(t[1:-1].replace('\\"','"').replace('\\\\','\\'))
        else:
            stack[-1].append(Sym(t))
    return stack[0][0]
def dump(x,ind=0):
    if isinstance(x,list):
        if all(not isinstance(e,list) for e in x):
            return '('+' '.join(dump(e) for e in x)+')'
        k=0
        while k<len(x) and not isinstance(x[k],list): k+=1
        s='('+' '.join(dump(e) for e in x[:k])
        for e in x[k:]:
            s+='\n'+'  '*(ind+1)+dump(e,ind+1)
        return s+')'
    if isinstance(x,Sym): return str(x)
    if isinstance(x,(int,float)): return fmt(x)
    return '"'+str(x).replace('\\','\\\\').replace('"','\\"')+'"'
def fmt(v):
    s=('%.4f'%v).rstrip('0').rstrip('.')
    return '0' if s in('-0','') else s
def find(x,key): return [e for e in x if isinstance(e,list) and e and e[0]==key]
_cache={}
def libsyms(lib):
    if lib not in _cache:
        p=lib if '/' in lib else f'/usr/share/kicad/symbols/{lib}.kicad_sym'
        root=parse(open(p).read())
        _cache[lib]={e[1]:e for e in find(root,'symbol')}
    return _cache[lib]
def getsym(lib,name):
    """return flattened symbol (extends resolved)"""
    import copy
    d=libsyms(lib); s=copy.deepcopy(d[name]); ex=find(s,'extends')
    if ex:
        base=getsym(lib,ex[0][1])
        # take base graphics/units, child properties
        props=find(s,'property')
        out=[Sym('symbol'),name]
        for e in base[2:]:
            if isinstance(e,list) and e[0]=='property': continue
            if isinstance(e,list) and e[0]=='symbol':
                e=copy.deepcopy(e); e[1]=e[1].replace(ex[0][1],name,1)
            out.append(e)
        # insert props after header items
        hdr=[e for e in out[2:] if isinstance(e,list) and e[0] in('pin_numbers','pin_names','in_bom','on_board','exclude_from_sim')]
        rest=[e for e in out[2:] if e not in hdr]
        return [Sym('symbol'),name]+hdr+props+rest
    return s
def pins(sym):
    res=[]
    for u in find(sym,'symbol'):
        unit=int(u[1].split('_')[-2])
        for p in find(u,'pin'):
            at=find(p,'at')[0]
            nm=find(p,'name')[0][1]; num=find(p,'number')[0][1]
            ln=find(p,'length')[0][1]
            res.append(dict(type=str(p[1]),x=float(at[1]),y=float(at[2]),rot=int(float(at[3])) if len(at)>3 else 0,name=nm,num=num,len=float(ln),unit=unit))
    return res
