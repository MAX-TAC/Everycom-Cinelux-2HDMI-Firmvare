#!/usr/bin/env python3
"""Read-only firmware version scan of packaged vendor ext4 partitions; no private device dumps."""
from pathlib import Path
import sys,subprocess,re,json,shutil
parts=Path(sys.argv[1]);variant=sys.argv[2];out=Path(sys.argv[3])
out.mkdir(parents=True,exist_ok=True)
root=Path('/tmp/oem_version_roots');root.mkdir(exist_ok=True)
names=('project_id','tvconfig_a','tvservice_a','bootdata_a')
sensitive=re.compile(r'(?i)(serial|password|passwd|secret|token|api.?key|private.?key|certificate|imei|wifi|mac.?address|bt.?address|widevine|drm|hdcp|uuid|/mnt/vendor/persist|/mnt/vendor/factory|device.?id)')
interesting=re.compile(r'(?i)(?:firmware|fw[_-]?ver|soft[_-]?ver|software|ota|upgrade|update|project[_-]?ver|project[_-]?name|build[_-]?ver|product[_-]?ver|sw[_-]?ver|version(?:code|name)?|1[.]0[.]4)')
text_types={'.json','.xml','.ini','.cfg','.conf','.rc','.prop','.properties','.txt','.sh','.yaml','.yml','.version'}
report={'variant':variant,'images':[],'matches':[],'named_files':[],'errors':[]}
for name in names:
    p=parts/(name+'.img')
    if not p.exists():
        report['errors'].append('Missing '+name);continue
    dest=root/name
    dest.mkdir(parents=True,exist_ok=True)
    try:
        r=subprocess.run(['debugfs','-R','rdump / '+str(dest),str(p)],capture_output=True,
          text=True,timeout=180,errors='replace')
        fmt=subprocess.run(['file','-b',str(p)],capture_output=True,text=True).stdout.strip()
        files=list(dest.rglob('*'))
        item={'name':name,'format':fmt[:200],'extracted_files':sum(1 for f in files if f.is_file()),'exit_code':r.returncode}
        report['images'].append(item)
        print('OEM ext4',name,item,flush=True)
        if r.returncode!=0:report['errors'].append(name+': '+r.stderr[-200:])
        for f in files:
            if not f.is_file() or f.is_symlink():continue
            rel=name+'/'+f.relative_to(dest).as_posix()
            if sensitive.search(rel):continue
            if interesting.search(f.name):report['named_files'].append(rel)
            if f.stat().st_size>2*1024*1024:continue
            if f.suffix.lower() not in text_types and not interesting.search(f.name):continue
            txt=f.read_text(errors='replace')
            if '\x00' in txt[:4000] and f.suffix.lower() not in text_types:continue
            for line_no,line in enumerate(txt.splitlines(),1):
                line=line.strip()
                if not line or len(line)>300 or sensitive.search(line):continue
                if interesting.search(line):
                    report['matches'].append({'file':rel,'line':line_no,'text':line[:200]})
                    if len(report['matches'])>=1500:break
    except Exception as e:report['errors'].append(name+': '+str(e))
(dest if False else out/'scan.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
lines=['# Packaged OEM configuration firmware-version scan: '+variant,'',
 'Only prepackaged manufacturer images project_id, tvconfig, tvservice, bootdata.',
 'System was never run or flashed. Sensitive fields and device identifiers are filtered.',
 '','## Packaged ext4 images', '']
for f in report['images']:
    lines.append('- '+f['name']+': '+str(f['extracted_files'])+' files, '+f['format'])
lines+=['','## Potential version-bearing files']
lines+=['- '+p for p in report['named_files'][:160]]
lines+=['','## Version string candidates']
lines+=['- '+x['file']+':'+str(x['line'])+' '+x['text'] for x in report['matches'][:200]]
lines+=['','## Warnings']
lines+=['- '+x for x in report['errors']]
(out/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('Metadata matches',len(report['matches']),'version-like filenames',len(report['named_files']),flush=True)
