#!/usr/bin/env python3
"""Compare two static, source-free APK analysis summaries: includes changed Java methods.
Metadata only. Does not reproduce proprietary source.
"""
import sys,json
from pathlib import Path
a=json.loads(Path(sys.argv[1]).read_text())['apps']
b=json.loads(Path(sys.argv[2]).read_text())['apps']
out=Path(sys.argv[3]);out.mkdir(parents=True,exist_ok=True)
result={'apps':{},'definitions':{
  'file_sha':'Hash of original application package. Different hashes can be only resources/signatures.',
  'dex_sha':'Hash of bytecode (classes.dex); differing indicates actual bytecode differences.',
  'class_hash':'Hash of approximate normalized decompiled Java. Heuristic, affected by decompiler.',
  'method_hash':'Hash of approximate normalized decompiled method body. Heuristic, not proof of behavior.',
  'permission_change':'Change in requested permissions; permission grant and runtime behavior not proven.'}}
for name in sorted(set(a)|set(b)):
  x=a.get(name,{});y=b.get(name,{})
  if x.get('missing') or y.get('missing'):
    result['apps'][name]={'only':'two' if x.get('missing') else 'one'};continue
  cx=x.get('codefiles',{});cy=y.get('codefiles',{})
  shared=set(cx)&set(cy)
  identical=sorted(k for k in shared if cx[k]['sha256']==cy[k]['sha256'])
  changed=sorted(k for k in shared if cx[k]['sha256']!=cy[k]['sha256'])
  onlyx=sorted(set(cx)-set(cy));onlyy=sorted(set(cy)-set(cx))
  methodstats={'unchanged':0,'changed':0,'added':0,'removed':0}
  diff_methods=[]
  for f in sorted(set(cx)|set(cy)):
    mx=x.get('methods',{}).get(f,{});my=y.get('methods',{}).get(f,{})
    for key in sorted(set(mx)|set(my)):
      if key not in mx:status='added'
      elif key not in my:status='removed'
      elif mx[key]['digest']==my[key]['digest']:status='unchanged'
      else:status='changed'
      methodstats[status]+=1
      if status!='unchanged' and len(diff_methods)<350:
        diff_methods.append({'class':f,'method':key[:180],'status':status})
  px=set(x.get('permissions',[]));py=set(y.get('permissions',[]))
  item={
    'one':{'apk_sha256':x.get('sha256'),'dex_sha256':x.get('dex'),'version':x.get('app_version'),
       'package':x.get('package'),'java_classes':x.get('java_class_count')},
    'two':{'apk_sha256':y.get('sha256'),'dex_sha256':y.get('dex'),'version':y.get('app_version'),
       'package':y.get('package'),'java_classes':y.get('java_class_count')},
    'apk_exact_match':x.get('sha256')==y.get('sha256'),
    'all_dex_exact_match':x.get('dex')==y.get('dex'),
    'classes':{'shared':len(shared),'exact_same':len(identical),'changed':len(changed),
               'only_one':len(onlyx),'only_two':len(onlyy)},
    'methods':methodstats,
    'changed_methods_sample':diff_methods,
    'classes_only_one':onlyx[:90],'classes_only_two':onlyy[:90],
    'changed_classes_sample':changed[:120],
    'permissions_only_one':sorted(px-py),
    'permissions_only_two':sorted(py-px),
    'native_libraries_one':x.get('native_libraries',[]),
    'native_libraries_two':y.get('native_libraries',[]),
    'interesting_classes_one':x.get('interesting_classes',[]),
    'interesting_classes_two':y.get('interesting_classes',[]),
    'service_strings_one':x.get('referenced_service_strings',[]),
    'service_strings_two':y.get('referenced_service_strings',[]),
    'calls_one':x.get('api_usage_count',{}),'calls_two':y.get('api_usage_count',{}),
    'manifest_one':x.get('manifest_extract',{}),
    'manifest_two':y.get('manifest_extract',{}),
    'decompilation_warnings_one':x.get('jadx_warnings','')[-600:],
    'decompilation_warnings_two':y.get('jadx_warnings','')[-600:],
  }
  result['apps'][name]=item
(out/'apk_method_diff.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf8')
lines=['# Everycom CineLux — deep OEM app comparison (1 vs 2 HDMI)','',
'APK and Java method hashes are extracted without executing OEM code. Decompiled sources are NOT published.',
'Both original APKs may be from builds with different compiler flags; class/method diffs are indicative, not behavior proof.',
'','| App | APK exact? | DEX exact? | Same classes | Changed classes | Changed methods | Added/removed methods |',
'|---|---|---|---:|---:|---:|---:|']
for name,item in result['apps'].items():
  if item.get('only'):
    lines.append('| '+name+' | Only '+item['only']+' | — | — | — | — | — |')
    continue
  c=item['classes'];m=item['methods']
  lines.append('| '+name+' | '+str(item['apk_exact_match'])+' | '+str(item['all_dex_exact_match'])+' | '+str(c['exact_same'])+
       ' | '+str(c['changed'])+' | '+str(m['changed'])+' | '+str(m['added']+m['removed'])+' |')
for name,item in result['apps'].items():
  lines+=['','## '+name,'']
  if item.get('only'):
    lines.append('Package only available in '+item['only']+' HDMI image.');continue
  lines+=['One HDMI: '+str(item['one']['package'])+' version '+str(item['one']['version']),
          'Two HDMI: '+str(item['two']['package'])+' version '+str(item['two']['version']),
          'Exact dex same: '+str(item['all_dex_exact_match']),
          'App permissions only in 1 HDMI: '+', '.join(item['permissions_only_one']),
          'App permissions only in 2 HDMI: '+', '.join(item['permissions_only_two']),
          'Native loaded 1 HDMI: '+', '.join(item['native_libraries_one']),
          'Native loaded 2 HDMI: '+', '.join(item['native_libraries_two']),
          'Method change counts: '+json.dumps(item['methods']),'']
  v=[x for x in item['changed_methods_sample'] if
        any(w in (x['class']+' '+x['method']).lower()
        for w in ('keystone','focus','motor','hdmi','source','i2c','display','settings','trd','camera','image','picture','cec','sound','ota','upgrade'))]
  lines+=['### Changed methods of likely hardware relevance (sample)','']
  lines+=['- '+x['status']+' '+x['class']+' :: '+x['method'] for x in v[:60]]
  lines+=['','### Added classes (sample)','']
  lines+=['- '+x for x in item['classes_only_two'][:40]]
  lines+=['','### Removed classes (sample)','']
  lines+=['- '+x for x in item['classes_only_one'][:40]]
lines+=['','## Source limitations','',
'This is code-level **static** evidence. It does not show a class actually runs, its effectiveness on hardware, or the reason a binary was rebuilt.',
'Dependency-safe removal and HDMI cross-compatibility require ADB runtime traces and hardware tests.',
'']
(out/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('COMPARISON',[(n,d.get('methods'),d.get('all_dex_exact_match')) for n,d in result['apps'].items()],flush=True)
