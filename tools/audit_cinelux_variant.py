#!/usr/bin/env python3
"""Generate non-binary comparable inventory of CineLux OTA partitions and Android app files.
Only read extracted files. Outputs SHA256/size/names; excludes contents and device secrets.
"""
from pathlib import Path
import argparse,hashlib,json,re,subprocess,collections
p=argparse.ArgumentParser()
p.add_argument('--parts',required=True)
p.add_argument('--logical',required=True)
p.add_argument('--erofs',required=True)
p.add_argument('--script',required=True)
p.add_argument('--report',required=True)
p.add_argument('--variant',required=True)
args=p.parse_args()
parts=Path(args.parts); logical=Path(args.logical); erofs=Path(args.erofs)
script=Path(args.script).read_text(errors='replace')
out={'variant':args.variant,'partitions':{},'android':{},'files':{},'build_props':{},
     'hal':{},'script':{},'component_groups':{},'errors':[]}
def checksum(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
    return h.hexdigest()
def identify(path):
    r=subprocess.run(['file','-b',str(path)],capture_output=True,text=True,errors='replace')
    return r.stdout.strip()[:190]
for f in parts.glob('*.img'):
    if f.name=='super.img':continue
    # Official firmware images only. User-specific calibration dumps NEVER included.
    out['partitions'][f.stem]={'size':f.stat().st_size,'sha256':checksum(f),'type':identify(f)}
for f in logical.glob('*.img'):
    out['android'][f.stem]={'size':f.stat().st_size,'sha256':checksum(f),'type':identify(f)}
script_commands=[]
for line in script.splitlines():
    s=line.strip()
    if s.startswith(('gpt create ', 'setenv ', 'addbootargs ')):
        if any(x in s.lower() for x in ('password','secret','token','serial','key','macaddr')):
            continue
        script_commands.append(s[:300])
out['script']={'commands':script_commands,
               'partition_layout':[x for x in script_commands if x.startswith('gpt create ')],
               'board_flags':[x for x in script_commands if x.startswith(('setenv android_product','setenv dtbo_cfg_sel','setenv android_manufacturer','addbootargs androidboot.selinux','setenv verify','setenv devicestate'))],
               'filepartload_count':sum(s.startswith('filepartload') for s in script.splitlines()),
               'super_swrite_count':sum(s.startswith('partition swrite mmc 0 super') for s in script.splitlines())}
prop_keys=('ro.build.version.release','ro.build.version.sdk','ro.build.version.security_patch',
 'ro.build.type','ro.build.tags','ro.build.date','ro.build.display.id','ro.product.model',
 'ro.product.device','ro.product.board','ro.product.manufacturer','ro.product.brand',
 'ro.board.platform','ro.hardware','ro.vendor.build.fingerprint','ro.build.fingerprint',
 'ro.vendor.build.security_patch','ro.product.vendor.model','ro.boot.hardware',
 'ro.build.version.incremental')
for partition in sorted(erofs.iterdir()) if erofs.exists() else []:
    if not partition.is_dir():continue
    part_name=partition.name
    found={}
    group=collections.defaultdict(list)
    for file in sorted(partition.rglob('*')):
        if not file.is_file() or file.is_symlink():continue
        rel=file.relative_to(partition).as_posix()
        if rel.startswith(('data/','mnt/vendor/persist/','mnt/vendor/factory/')):continue
        info={'size':file.stat().st_size,'sha256':checksum(file)}
        found[rel]=info
        if file.suffix.lower()=='.apk':
            group['apk'].append(rel)
            if '/priv-app/' in '/'+rel:group['privapp'].append(rel)
        if file.suffix=='.so':
            group['shared_libs'].append(rel)
        if rel.startswith(('vendor/bin/hw','bin/hw','system/bin','vendor/bin')):
            group['executables'].append(rel)
        if file.suffix=='.rc':group['init_rc'].append(rel)
        if file.name.endswith('build.prop') and file.stat().st_size<=100000:
            for line in file.read_text(errors='replace').splitlines():
                if not line or line.startswith('#') or '=' not in line:continue
                k,v=line.split('=',1)
                if k in prop_keys:out['build_props'][f'{part_name}:{rel}:{k}']=v.strip()[:230]
        if file.name=='manifest.xml' and '/vintf/' in '/'+rel and file.stat().st_size<300000:
            xml=file.read_text(errors='replace')
            out['hal'][f'{part_name}:{rel}']=sorted(set(re.findall(r'<name>([^<]+)</name>',xml)))[:180]
    out['files'][part_name]=found
    out['component_groups'][part_name]={k:sorted(v) for k,v in group.items()}
dest=Path(args.report);dest.parent.mkdir(exist_ok=True,parents=True)
dest.write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf8')
print('Inventory',args.variant, {k:len(v) for k,v in out['files'].items()},
      'partitions',len(out['partitions']), 'logical',len(out['android']))
