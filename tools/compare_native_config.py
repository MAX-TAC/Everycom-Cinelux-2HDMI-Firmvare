#!/usr/bin/env python3
"""Compare native execution code, dependencies and privacy-filtered configs across variants."""
from pathlib import Path
import json,sys,difflib,re,collections
one=json.loads(Path(sys.argv[1]).read_text());two=json.loads(Path(sys.argv[2]).read_text())
out=Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=True)
focus=re.compile(r'(?i)(trd|mtk|mstar|hdmi|cec|tof|motor|focus|keystone|camera|display|audio|codec|dolby|i2c|projection|screen|source|tv|power|boot|factory|project)')
sensitive=re.compile(r'(?i)(serial|password|passwd|secret|token|private|mac_address|macaddr|imei|ssid|widevine|hdcp|drm.?key|device.?id|auth.?key|public.?key)')
def cmp(a,b):
  only1=sorted(set(a)-set(b));only2=sorted(set(b)-set(a))
  shared=sorted(set(a)&set(b))
  changed=[k for k in shared if a[k].get('sha256')!=b[k].get('sha256')]
  code_changed=[k for k in changed if a[k].get('sections',{}).get('.text',{}).get('sha256')!=b[k].get('sections',{}).get('.text',{}).get('sha256')]
  code_same=[k for k in changed if k not in code_changed]
  return {'total_one':len(a),'total_two':len(b),'identical':len(shared)-len(changed),
    'changed_binary':len(changed),'code_text_changed':len(code_changed),
    'code_text_same_but_binary_diff':len(code_same),
    'only_one':only1,'only_two':only2,'changed_paths':changed,'code_changed':code_changed,
    'code_same_but_binary_diff':code_same}
a=one['native'];b=two['native'];nc=cmp(a,b)
critical=sorted(k for k in nc['changed_paths'] if focus.search(k))
native=[]
for k in critical:
  x=a[k];y=b[k]
  xtext=x.get('sections',{}).get('.text',{})
  ytext=y.get('sections',{}).get('.text',{})
  native.append({'path':k,'same_code_text':xtext.get('sha256')==ytext.get('sha256'),
    'one_text_size':xtext.get('size'),'two_text_size':ytext.get('size'),
    'one_elf_class':x.get('elf_class'),'two_elf_class':y.get('elf_class'),
    'needed_only_one':sorted(set(x.get('needed',[]))-set(y.get('needed',[]))),
    'needed_only_two':sorted(set(y.get('needed',[]))-set(x.get('needed',[]))),
    'hardware_exports_only_one':sorted(set(x.get('hardware_exports',[]))-set(y.get('hardware_exports',[]))),
    'hardware_exports_only_two':sorted(set(y.get('hardware_exports',[]))-set(x.get('hardware_exports',[])))})
config_one=one['configs'];config_two=two['configs']
c1=set(config_one);c2=set(config_two)
changes=[]
for k in sorted(c1&c2):
  x=config_one[k];y=config_two[k]
  if x['sha256']==y['sha256']:continue
  l1=x['lines'];l2=y['lines']
  if sensitive.search(k):continue
  lines=list(difflib.unified_diff(l1,l2,fromfile="one-HDMI/"+k,tofile="two-HDMI/"+k,n=2))
  if len(lines)>120:lines=lines[:120]+['... [diff truncated]']
  changes.append({'path':k,'changed_line_count':len(lines),'diff':lines})
result={'native_counts':{k:v for k,v in nc.items() if not isinstance(v,list)},
 'native_only_one':nc['only_one'],'native_only_two':nc['only_two'],
 'native_critical':native,
 'native_identical_text_despite_changed_binary':nc['code_same_but_binary_diff'][:150],
 'config_counts':{'one':len(config_one),'two':len(config_two),
                  'same_files':sum(config_one[k]['sha256']==config_two[k]['sha256'] for k in c1&c2),
                  'changed_files':len(changes),'only_one':len(c1-c2),'only_two':len(c2-c1)},
 'config_only_one':sorted(c1-c2),'config_only_two':sorted(c2-c1),
 'config_changes':changes,
 'dtbo_comparison':{'one':one['dtbo'],'two':two['dtbo']},
 'one_firmware_headers':one['firmware_images'],
 'two_firmware_headers':two['firmware_images']}
(out/'native_config_diff.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
lines=['# MediaTek / OEM native libraries, service configuration and DTBO diff','',
'The executable .text ELF sections were hashed separately from the whole binary. When full binary SHA differs but .text agrees, differences may be metadata, other data, or non-executable code; not proof of identical function.',
'Privacy-related configuration strings were filtered before comparison.',
'','## Shared library comparison','']
for k,v in result['native_counts'].items():lines.append('- '+k+': **'+str(v)+'**')
lines+=['','## Apparatus-related native libraries with different binary SHA','',
'| ELF | Same executable .text? | 1 HDMI text bytes | 2 HDMI text bytes | Dependencies difference |',
'|---|---|---:|---:|---|']
for x in native[:150]:
  deps='+ '+', '.join(x['needed_only_two'])+'; - '+', '.join(x['needed_only_one'])
  lines.append('| '+x['path']+' | '+str(x['same_code_text'])+' | '+str(x['one_text_size'])+
               ' | '+str(x['two_text_size'])+' | '+deps[:100].replace('|','/')+' |')
lines+=['','## Native binaries only in one-HDMI','']
lines+=['- '+k for k in nc['only_one']]
lines+=['','## Native binaries only in two-HDMI','']
lines+=['- '+k for k in nc['only_two']]
lines+=['','## Configuration comparison','']
for k,v in result['config_counts'].items():lines.append('- '+k+': '+str(v))
lines+=['','### Important differing config fragments','']
for c in changes[:65]:
  lines+=['#### '+c['path'],'','~~~diff',*c['diff'][:85],'~~~','']
lines+=['','## Device-tree overlay format','',
'One HDMI: '+json.dumps(one['dtbo'],ensure_ascii=False),
'Two HDMI: '+json.dumps(two['dtbo'],ensure_ascii=False),
'','## Conclusions and limits','',
'Equal exported interfaces or init service declarations is not proof that board-specific drivers are interchangeable.',
'Full hardware-specific service behavior needs live logs and tests; never flash a foreign DTBO or erase calibration before board identity and recovery are established.',
'']
(out/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('NATIVE SUMMARY',result['native_counts'],flush=True)
print('CONFIG SUMMARY',result['config_counts'],flush=True)
print('DTBO',result['dtbo_comparison'],flush=True)
