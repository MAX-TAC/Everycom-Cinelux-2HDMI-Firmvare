#!/usr/bin/env python3
"""Read-only inventory of the separate MediaTek/MStar Linux rootfs and third-party image.
Does not run any binary from firmware or publish device secrets.
"""
from pathlib import Path
import json,subprocess,sys,hashlib,re,collections
images=Path(sys.argv[1]);variant=sys.argv[2];dest=Path(sys.argv[3]);dest.parent.mkdir(parents=True,exist_ok=True)
root=Path('/tmp/medialinux_'+variant);root.mkdir(exist_ok=True)
sensitive=re.compile(r'(?i)(password|passwd|secret|private|token|serial|macaddr|mac_address|hdcp|widevine|drm.?key|imei|ssid|device.?id)')
result={'variant':variant,'images':{},'files':{},'service_names':{},'config_samples':{}}
def sha(path):
  h=hashlib.sha256()
  with path.open('rb') as stream:
    for b in iter(lambda:stream.read(4*1024*1024),b''):h.update(b)
  return h.hexdigest()
for name in ('linux_rootfs_a_a','3rd_a_a'):
  image=images/(name+'.img')
  if not image.is_file():continue
  target=root/name
  target.mkdir(exist_ok=True)
  cmd=['unsquashfs','-no-progress','-f','-d',str(target),str(image)]
  p=subprocess.run(cmd,capture_output=True,text=True,errors='replace',timeout=240)
  if p.returncode:raise RuntimeError(name+' squashfs extract failed: '+p.stderr[-800:])
  files={}
  services=[]
  snippets={}
  for file in sorted(target.rglob('*')):
    if not file.is_file() or file.is_symlink():continue
    rel=file.relative_to(target).as_posix()
    if sensitive.search(rel):continue
    filesize=file.stat().st_size
    files[rel]={'size':filesize,'sha256':sha(file)}
    if file.name.endswith(('.rc','.service','.sh')) or '/init.d/' in rel or '/etc/inittab' in rel:
      services.append(rel)
    if filesize<130000 and (file.name in ('fstab','inittab','build.prop','rcS') or
      file.suffix in ('.conf','.rc','.service','.prop')):
      try:
        txt=file.read_text(errors='replace')
        lines=[l.strip()[:190] for l in txt.splitlines() if
           len(l)<300 and not sensitive.search(l) and
           re.search(r'(?i)(start|service|load|insmod|daemon|tv|hdmi|audio|display|mstar|mtk|dvb|init|gpio|mount)',l)]
        if lines:snippets[rel]=lines[:16]
      except Exception:pass
  result['images'][name]={'file_size':image.stat().st_size,'fs_files_count':len(files)}
  result['files'][name]=files
  result['service_names'][name]=services
  result['config_samples'][name]=snippets
  print(variant,name,'files',len(files),'services',len(services),'configfiles',len(snippets),flush=True)
dest.write_text(json.dumps(result,ensure_ascii=False,indent=1),encoding='utf8')
