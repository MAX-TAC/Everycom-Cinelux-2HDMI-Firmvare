#!/usr/bin/env python3
"""Search stock projector Android files for *firmware* version metadata, not app guesses.
Read-only, bounded; never publish serials/DRM/config secrets.
Args: <erofs_parent> <flashed_partitions_parent> <variant> <outdir>
"""
from pathlib import Path
import sys,re,json,subprocess
base=Path(sys.argv[1]); parts=Path(sys.argv[2]); version=sys.argv[3]; out=Path(sys.argv[4]);out.mkdir(parents=True,exist_ok=True)
META=re.compile(r'(?i)(?:^|[._\-])(version|ver|build|ota|upgrade|update|firmware|fw|model|board|platform|device|project)(?:[._\-]|$)')
SENS=re.compile(r'(?i)(serial|mac|ipaddr|wifi_password|imei|imei|token|password|passwd|secret|private.?key|widevine|drm|hdcp|bluetooth_address|uuid|android_id|device.?id|pubkey)')
patterns=[
 re.compile(r'(?i)\b(?:firmware|software|ota|update|upgrade|project|product|board|build|vendor)[\w.-]{0,48}\s*[=:]\s*[^\x00\r\n]{1,100}'),
 re.compile(r'(?i)\b(?:version|versionName|versionCode|fwver|swver|firmwareversion)[\w.-]{0,32}\s*[=:]\s*[^\x00\r\n]{1,100}'),
 re.compile(r'(?i)\b(?:version|ver)[\s:=-]{0,12}(?:v?1[.]0[.]4|v?[0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})\b')
]
hits=[];props=[];aux=[];apk=[];configs=[]
def add(rel,line,category):
    line=line.strip().replace('\x00',' ')
    if not line or len(line)>200 or SENS.search(line):return
    if not any(c.isalnum() for c in line):return
    if len(hits)<700:
        hits.append({'file':rel,'category':category,'line':line[:180]})
for part in sorted(base.iterdir()) if base.exists() else []:
  if not part.is_dir():continue
  for f in part.rglob('*'):
    if not f.is_file() or f.is_symlink():continue
    rel=part.name+'/'+str(f.relative_to(part))
    if f.name=='build.prop' and f.stat().st_size<250000:
      text=f.read_text(errors='replace')
      for line in text.splitlines():
        s=line.strip()
        if '=' not in s or s.startswith('#'):continue
        k,v=s.split('=',1)
        if SENS.search(k):continue
        if re.search(r'(?i)(version|build|fingerprint|ota|update|firmware|project|platform|product|ro\.vendor)',k):
          props.append({'file':rel,'key':k,'value':v[:220]})
      continue
    if f.suffix=='.apk' and any(n in rel.lower() for n in ('ruiyunota','kusettings','factory','trdservice','kusetupwizard','tvsettingsplus','zxlauncher')):
      r=subprocess.run(['aapt','dump','badging',str(f)],capture_output=True,text=True,errors='replace',timeout=25)
      p=next((x for x in r.stdout.splitlines() if x.startswith('package:')),None)
      apk.append({'file':rel,'package':p[:300] if p else None})
      continue
    if f.stat().st_size>2*1024*1024:continue
    if not (f.suffix.lower() in ('.xml','.prop','.json','.ini','.conf','.cfg','.txt','.rc','.properties','.mk','.sh','.yml','.yaml') or META.search(f.name)):continue
    if any(x in rel.lower() for x in ('/sepolicy','/policy','/fonts','/timezone','/usr/keychars','/usr/keylayout','/permissions/')):continue
    configs.append(rel)
    txt=f.read_text(errors='replace')
    for i,line in enumerate(txt.splitlines(),1):
      if len(line)>500 or SENS.search(line):continue
      if any(p.search(line) for p in patterns):
        if len(hits)<600:add(rel+'#L'+str(i),line,'android_config')
for f in sorted(parts.glob('*.img')) if parts.exists() else []:
  if f.stem not in ('tvconfig_a','tvservice_a','project_id','bootdata_a','3rd_a_a','linux_rootfs_a_a','emmc_boot','mboot_a','boot_a'):continue
  r=subprocess.run(['file','-b',str(f)],capture_output=True,text=True,errors='replace',timeout=30)
  aux.append({'image':f.name,'size':f.stat().st_size,'file_type':r.stdout.strip()[:200]})
# Textual report without full binary data, confidential fields or internal keys.
result={'variant':version,'system_build_properties':props,'oem_software_apk_versions':apk,
        'version_candidates':hits,'inspected_config_file_count':len(configs),
        'flashed_image_formats':aux,
        'method':'read-only scan; OTA version may instead live in factory partitions or /data'}
(out/'version_inventory.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
rows=['# CineLux firmware version metadata: '+version,'',
      'From full decrypted stock firmware, EROFS, APK package manifests and bounded config scan.',
      'Do not confuse Android platform build version, app APK version and OEM firmware OTA version.',
      '','## Build properties']
for p in props:
  if re.search(r'(ro.build.display.id|ro.build.version.incremental|ro.build.date|ro.build.version.release|ro.build.version.security_patch|ro.vendor.build.fingerprint|ro.product.model|ro.product.device)',p['key']):
    rows.append('- '+p['file']+' '+p['key']+'='+p['value'])
rows+=['','## OEM app APK versions']
rows+=['- '+x['file']+' — '+str(x['package']) for x in apk]
rows+=['','## Candidate firmware version strings in text configuration']
rows+=['- '+x['file']+': '+x['line'] for x in hits[:170]]
rows+=['','## Proprietary image formats']
rows+=['- '+x['image']+' '+str(x['size'])+'B : '+x['file_type'] for x in aux]
(out/'README.md').write_text('\n'.join(rows)+'\n',encoding='utf8')
print('Variant',version,'props',len(props),'APKs',len(apk),'candidate version strings',len(hits),'configs',len(configs),flush=True)
