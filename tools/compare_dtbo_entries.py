#!/usr/bin/env python3
"""Read-only per-entry Android DTBO overlay image analysis."""
from pathlib import Path
import sys,hashlib,struct,json,re
path=Path(sys.argv[1]);out=Path(sys.argv[2]);name=sys.argv[3];out.parent.mkdir(parents=True,exist_ok=True)
with path.open('rb') as f:
    header=f.read(32)
    vals=struct.unpack('>8I',header)
    magic,total,hs,es,n,entries_offset,pg,ver=vals
    assert magic==0xd7b7ab1e and es>=32 and n<=1000 and total<=path.stat().st_size
    entries=[]
    for idx in range(n):
        f.seek(entries_offset+idx*es)
        e=f.read(es)
        size,offset,hwid,rev,c0,c1,c2,c3=struct.unpack('>8I',e[:32])
        if size>12*1024*1024 or offset+size>path.stat().st_size:raise ValueError("Bad entry "+str(idx))
        f.seek(offset);b=f.read(size)
        dtmagic=b[:4].hex()
        strings=[]
        if dtmagic=='d00dfeed':
          # Basic labels only, avoid publishing serial, IDs or personal fields.
          for m in re.finditer(rb'(?:[A-Za-z][A-Za-z0-9 ,_.-]{7,100})\x00',b[:32768]):
            t=m.group(0)[:-1].decode('latin1','replace')
            if any(v in t.lower() for v in ('mediatek','mt5873','mt9660','griggs','projector','hdmi','panel','audio','tof','dpl','gpio')) and len(strings)<15:
              strings.append(t[:90])
        entries.append({'index':idx,'bytes':size,'offset':offset,'id':hwid,'rev':rev,
          'custom':[c0,c1,c2,c3],'sha256':hashlib.sha256(b).hexdigest(),
          'blob_magic':dtmagic,'labels':strings})
result={'variant':name,'header':{'count':n,'total':total,'version':ver,'entry_size':es},
        'entries':entries}
out.write_text(json.dumps(result,indent=2,ensure_ascii=False))
print(name,'DTBO overlays',n,'valid FDT',sum(e['blob_magic']=='d00dfeed' for e in entries),flush=True)
