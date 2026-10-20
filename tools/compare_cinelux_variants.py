#!/usr/bin/env python3
"""Compare static vendor images. Requires two generated JSON manifests, no binary firmware."""
import sys,json
from pathlib import Path
one=json.loads(Path(sys.argv[1]).read_text())
two=json.loads(Path(sys.argv[2]).read_text())
out=Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=True)
def filemaps(blob):
    return {f"{partition}/{path}":record for partition,files in blob["files"].items() for path,record in files.items()}
a=filemaps(one);b=filemaps(two)
common=set(a)&set(b)
same=sorted(k for k in common if a[k]['sha256']==b[k]['sha256'])
diff=sorted(k for k in common if a[k]['sha256']!=b[k]['sha256'])
only1=sorted(set(a)-set(b))
only2=sorted(set(b)-set(a))
def comp(left,right):
    keys=sorted(set(left)|set(right))
    return [{'name':k,'one':left.get(k),'two':right.get(k),'identical':left.get(k)==right.get(k)} for k in keys]
partition=comp(one['partitions'],two['partitions'])
android=comp(one['android'],two['android'])
props=comp(one['build_props'],two['build_props'])
script1=one['script'];script2=two['script']
def is_apk(path):return path.lower().endswith('.apk')
def high_interest(path):
    name=path.lower()
    return any(x in name for x in
     ('settings','keystone','focus','source','tvinput','tvservice','tvframework','trd','project','launcher','display','hdmi','cec',
      'camera','ota','mtk','mstar','audio','bluetooth','dolby','sound','boot','init.','vendor/etc','peripheral','factory'))
report={
    'variants':{'one':one['variant'],'two':two['variant']},
    'counts':{'one_file_count':len(a),'two_file_count':len(b),'common_paths':len(common),
      'byte_identical_file_paths':len(same),'changed_common_paths':len(diff),
      'only_in_one':len(only1),'only_in_two':len(only2),
      'common_identical_percent':round(100*len(same)/len(common),2) if common else None},
    'partition_comparison':partition,'android_partition_comparison':android,
    'build_prop_comparison':props,
    'script_comparison':{
      'partition_layout_same':script1['partition_layout']==script2['partition_layout'],
      'board_flags_same':script1['board_flags']==script2['board_flags'],
      'one_board_flags':script1['board_flags'],'two_board_flags':script2['board_flags'],
      'one_filepartload_count':script1['filepartload_count'],
      'two_filepartload_count':script2['filepartload_count'],
      'one_super_fragments':script1['super_swrite_count'],
      'two_super_fragments':script2['super_swrite_count'],
      'only_one_commands':sorted(set(script1['commands'])-set(script2['commands']))[:80],
      'only_two_commands':sorted(set(script2['commands'])-set(script1['commands']))[:80]},
    'apps':{'one_only':sorted(k for k in only1 if is_apk(k)),
      'two_only':sorted(k for k in only2 if is_apk(k)),
      'changed':sorted(k for k in diff if is_apk(k)),
      'identical':sorted(k for k in same if is_apk(k))},
    'changed_interesting':sorted(k for k in diff if high_interest(k)),
    'only_one_interesting':sorted(k for k in only1 if high_interest(k)),
    'only_two_interesting':sorted(k for k in only2 if high_interest(k)),
    'changed_all':diff,'only_one_all':only1,'only_two_all':only2,
    'same_count_by_partition':{s:len([x for x in same if x.startswith(s+'/')]) for s in sorted(one['files'])},
    'diff_count_by_partition':{s:len([x for x in diff if x.startswith(s+'/')]) for s in sorted(one['files'])},
    'one_hals':one.get('hal',{}),'two_hals':two.get('hal',{})}
(out/'comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
lines=['# Everycom CineLux 1 HDMI vs 2 HDMI: decrypted firmware comparison','',
'Official firmware files were decrypted and inspected offline. No projectors were flashed.',
'One HDMI release: Original_Firmware_for_1_HDMI_ports (2026-08-13 filename)',
'Two HDMI release: Original_Firmware (2026-09-30 filename).','',
'## Overall file comparison','',
'| Metric | Value |','|---|---:|']
for name,value in report['counts'].items():lines.append(f'| {name} | {value} |')
lines+=['','## Android logical partitions','',
 '| Partition | One HDMI size | Two HDMI size | Exact SHA256 match |','|---|---:|---:|---|']
for x in android:
    lines.append('| '+x['name']+' | '+str(x['one']['size'] if x['one'] else '-')+
       ' | '+str(x['two']['size'] if x['two'] else '-')+' | '+('YES' if x['identical'] else 'NO')+' |')
lines+=['','## Other selected flashed partitions (whole-image SHA256)','',
 '| Partition | One HDMI size | Two HDMI size | Exact match |','|---|---:|---:|---|']
for x in partition:
    lines.append('| '+x['name']+' | '+str(x['one']['size'] if x['one'] else '-')+
       ' | '+str(x['two']['size'] if x['two'] else '-')+' | '+('YES' if x['identical'] else 'NO')+' |')
lines+=['','## Bootloader/GPT script comparison','',
 'GPT partition layout identical: '+str(report['script_comparison']['partition_layout_same']),
 'Board flags identical: '+str(report['script_comparison']['board_flags_same']),
 'One-HDMI filepartload commands: '+str(script1['filepartload_count'])+', super fragments: '+str(script1['super_swrite_count']),
 'Two-HDMI filepartload commands: '+str(script2['filepartload_count'])+', super fragments: '+str(script2['super_swrite_count']),
 '']
for label,items in [('One HDMI boot flags',script1['board_flags']),('Two HDMI boot flags',script2['board_flags'])]:
    lines+=['### '+label,'~~~',*items,'~~~']
lines+=['','## Android build properties differing','',
 '| Property (partition:path:key) | 1 HDMI | 2 HDMI |','|---|---|---|']
for x in props:
    if x['identical']:continue
    lines.append('| '+x['name']+' | '+str(x['one'] or '-').replace('|','/')[:110]+' | '+str(x['two'] or '-').replace('|','/')[:110]+' |')
lines+=['','## APK packages','',
 '| Group | Count |','|---|---:|']
for k,v in report['apps'].items():lines.append('| '+k+' | '+str(len(v))+' |')
for k,v in report['apps'].items():
    lines+=['','### '+k,'']
    lines+=['- '+x for x in v[:110]]
    if len(v)>110:lines+=['('+str(len(v)-110)+' additional APK paths in JSON report)']
lines+=['','## Hardware and device service differences','',
 'Paths highlighted because they may matter for HDMI, autofocus, keystone, audio, vendor framework or boot safety.']
for group,key in [('Only 1 HDMI','only_one_interesting'),('Only 2 HDMI','only_two_interesting'),('Files with changed hash','changed_interesting')]:
    v=report[key]
    lines+=['','### '+group+f' ({len(v)} paths)','']
    lines+=['- '+x for x in v[:170]]
    if len(v)>170:lines+=['('+str(len(v)-170)+' additional changed paths in JSON)']
lines+=['','## Completeness and warnings','',
'Identical file hash means byte-for-byte identical; differing hash does not necessarily mean different behavior.',
'Different builds can contain changed timestamps, build fingerprints and identical-function recompiles.',
'Hardware equivalence and HDMI port routing require live testing, device tree and driver analysis.',
'Manufacturer PKG encryption key enables extraction but not automatically valid signing or safe flashing.',
'The raw file inventory used for comparison is retained as GitHub Actions artifacts, not committed to Git.',
'']
(out/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('Comparison:',report['counts'],flush=True)
print('APK:',{k:len(v) for k,v in report['apps'].items()},flush=True)
print('Partition equality:',[(x['name'],x['identical']) for x in partition],flush=True)
