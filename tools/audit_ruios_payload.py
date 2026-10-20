#!/usr/bin/env python3
"""Read-only audit of decrypted Android A/B OTA payload images and EROFS file trees.
Inputs: extracted-partition-dir, extracted-erofs-dir, code, output-dir.
Persists only filenames, checksums and Android version properties; no OEM proprietary bytes.
"""
from pathlib import Path
import sys,subprocess,json,hashlib,re
parts=Path(sys.argv[1]); fs=Path(sys.argv[2]); code=sys.argv[3]; out=Path(sys.argv[4]);out.mkdir(exist_ok=True,parents=True)
HASH_CHUNK=4*1024*1024
def sha(p):
  h=hashlib.sha256()
  with p.open('rb') as f:
    for b in iter(lambda:f.read(HASH_CHUNK),b''):h.update(b)
  return h.hexdigest()
files={};partitions={};apps={};buildprops={};namespaces={};hal={}
for img in sorted(parts.glob('*.img')):
  p=subprocess.run(['file','-b',str(img)],capture_output=True,text=True)
  partitions[img.stem]={'bytes':img.stat().st_size,'sha256':sha(img),'type':p.stdout.strip()[:160]}
for d in sorted(fs.iterdir()):
  if not d.is_dir():continue
  for f in d.rglob('*'):
    if not f.is_file() or f.is_symlink():continue
    rel=f.relative_to(d).as_posix()
    path=d.name+'/'+rel
    # avoid serial-containing and private individual device data if any
    if rel.startswith(('data/','mnt/vendor/persist/','mnt/vendor/factory/')):continue
    files[path]={'size':f.stat().st_size,'sha256':sha(f)}
    if f.name=='build.prop' and f.stat().st_size<150000:
      for line in f.read_text(errors='replace').splitlines():
        if line.startswith('#') or '=' not in line:continue
        k,v=line.split('=',1)
        if any(x in k.lower() for x in ('serial','macaddr','password','secret','token','key.','uuid','deviceid')):continue
        if any(x in k for x in ('version','fingerprint','product','ro.build','ro.vendor','ota','firmware','model')):
          buildprops[f'{path}:{k}']=v[:200]
    if f.suffix=='.apk':
      cp=subprocess.run(['aapt','dump','badging',str(f)],capture_output=True,text=True,errors='replace')
      m=next((x for x in cp.stdout.splitlines() if x.startswith('package:')),'')
      found=re.findall(r"(name|versionCode|versionName)='([^']*)'",m)
      apps[path]={'aapt':dict(found),'sha256':files[path]['sha256']}
    if f.name=='manifest.xml' and 'vintf' in str(f):
      data=f.read_text(errors='replace')
      hal[path]=sorted(set(re.findall(r'<name>([^<]+)</name>',data)))[:250]
    if f.suffix in ('.rc','.kl','.idc','.xml','.ini') and any(x in path.lower() for x in ('hdmi','i2c','audio','focus','tof','trd','launcher','ota')):
      namespaces[path]=files[path]
o={'code':code,'partitions':partitions,'files':files,'apps':apps,'build_props':buildprops,'hal':hal,'hardware_config_candidates':namespaces}
(out/'inventory.json').write_text(json.dumps(o,ensure_ascii=False,indent=1))
lines=['# Extracted RUIOS OTA '+code+' image inventory','','This was reconstructed with payload-dumper-go from a genuine stock Android A/B OTA. No firmware executed or flashed.',
       '','## Partitions']
lines+=['| Partition | Bytes | Type |','|---|---:|---|']
for name,row in partitions.items():lines.append(f'| {name} | {row["bytes"]} | {row["type"]} |')
lines+=['','## System versions']
for name,value in buildprops.items():
  if re.search(r'(ro.build.version.incremental|ro.build.display.id|ro.build.date|ro.build.fingerprint|ro.product.model|ro.product.device)',name):
    lines.append('- '+name+' = '+value)
lines+=['','## OEM and selected Android APKs','','| APK | Package | Version |','|---|---|---|']
for path,info in apps.items():
  if any(x in path.lower() for x in ('kusettings','rui','keystone','source','trd','tvsettings','zx','ota','mtk','live','provision','factory','netflix','setupwizard','systemui','launcher')):
    lines.append('| '+path+' | '+info['aapt'].get('name','')+' | '+info['aapt'].get('versionName','')+' |')
lines+=['','Total extracted files: '+str(len(files))+', APK: '+str(len(apps))]
(out/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('Audited OTA:',code,'partitions',list(partitions),'files',len(files),'APKs',len(apps),flush=True)
