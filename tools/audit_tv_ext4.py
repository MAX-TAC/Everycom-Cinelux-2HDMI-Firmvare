#!/usr/bin/env python3
"""Static filesystem inventories for factory-packed MediaTek TV configuration/service partitions.
No raw file content and no customer-specific identifiers are committed.
"""
from pathlib import Path
import re,sys,json,subprocess,hashlib
parts=Path(sys.argv[1]);variant=sys.argv[2];out=Path(sys.argv[3]);out.parent.mkdir(parents=True,exist_ok=True)
names=['tvconfig_a','tvservice_a','project_id','bootdata_a']
root=Path('/tmp/tvext4_'+variant);root.mkdir(exist_ok=True)
secret=re.compile(r'(?i)(serial|private|secret|token|password|macaddr|mac_address|hdcp|widevine|drm|imei|device.?id|wifi.?pass|nvr|keybox|key_store)')
interesting=re.compile(r'(?i)(hdmi|focus|camera|tof|tv|trd|i2c|pq|image|picture|sound|audio|display|panel|boot|startup|config|service|motor|gpio|firmware|upgrade|mtk|keystone|rjpj)')
outdata={'variant':variant,'partitions':{},'samples':{},'errors':[]}
def sha(file):
  h=hashlib.sha256()
  with file.open('rb') as f:
    for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
  return h.hexdigest()
for name in names:
  f=parts/(name+'.img')
  if not f.is_file():continue
  dest=root/name;dest.mkdir(exist_ok=True)
  p=subprocess.run(['debugfs','-R','rdump / '+str(dest),str(f)],capture_output=True,
    text=True,errors='replace',timeout=220)
  if p.returncode!=0:
    outdata['errors'].append({'partition':name,'error':p.stderr[-250:]})
  files={}
  excerpts={}
  for child in dest.rglob('*'):
    if not child.is_file() or child.is_symlink():continue
    rel=child.relative_to(dest).as_posix()
    if secret.search(rel):continue
    sz=child.stat().st_size
    files[rel]={'bytes':sz,'sha256':sha(child)}
    if sz>120000 or not interesting.search(rel):continue
    if child.suffix.lower() not in ('.xml','.ini','.conf','.cfg','.properties','.prop','.txt','.json','.sh','.rc','.sql'):
      continue
    try:
      text=child.read_text(errors='replace')
      selected=[l.strip()[:200] for l in text.splitlines() if
        0<len(l)<350 and interesting.search(l) and not secret.search(l)]
      if selected:excerpts[rel]=selected[:20]
    except Exception:pass
  outdata['partitions'][name]={'bytes':f.stat().st_size,'files':files,'total_files':len(files)}
  outdata['samples'][name]=excerpts
  print(variant,name,'files',len(files),'interesting text',len(excerpts),flush=True)
out.write_text(json.dumps(outdata,indent=1,ensure_ascii=False),encoding='utf8')
