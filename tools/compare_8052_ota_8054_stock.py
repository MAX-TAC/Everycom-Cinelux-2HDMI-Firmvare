#!/usr/bin/env python3
"""Read-only SHA comparison: October 8052 OTA vs September factory 8054 saved manifest.
No OEM binaries or private device data are published. No flashing.
"""
import argparse,hashlib,json,re,struct,subprocess,zipfile
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--images",type=Path,required=True)
p.add_argument("--erofs",type=Path,required=True)
p.add_argument("--out",type=Path,default=Path("analysis/Latest_8052_OTA_vs_8054_Stock"))
a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=True)
stock=json.loads(Path("analysis/Stock_8052_vs_8054_Board/comparison.json").read_text())
origapps=json.loads(Path("analysis/Deep_APK_Comparison/apk_method_diff.json").read_text())["apps"]
sha=lambda x:hashlib.sha256(x).hexdigest()
configs={
"board.ini":("tvconfig","bsp/board/BD_MT5873_H1V1_B6_S/board.ini"),
"tvconfig/dtbo_mapping.ini":("tvconfig","config/dtbo_mapping.ini"),
"bootdata/dtbo_mapping.ini":("bootdata","config/dtbo_mapping.ini"),
"BasicSound_HDMI.ini":("tvconfig","bsp/chip/aq/InputSrc/BasicSound_HDMI.ini"),
"BasicSound_DTV.ini":("tvconfig","bsp/chip/aq/InputSrc/BasicSound_DTV.ini"),
"BasicSound_MM.ini":("tvconfig","bsp/chip/aq/InputSrc/BasicSound_MM.ini"),
"ConfigDefaultValue.ini":("tvconfig","platform/data/misc/ConfigDefaultValue.ini"),
"gammatable_1.ini":("tvconfig","bsp/common/PQ_general/gammatable_1.ini"),
"pmu_mcs51_sign.bin":("bootdata","pmu/pmu_mcs51_sign.bin")}
result={"sources":{"ota8052":"RUIOS.8052.1.0.4 (2026-10-12)",
                   "factory8054":"RUIOS.8054.1.0.1 (2026-09-30)"},
        "configs":{},"apps":{},"props":{},"libs":{},"dtbo":{}}
for name,(partition,path) in configs.items():
    img=a.images/(partition+".img")
    r=subprocess.run(["debugfs","-R","cat /"+path,str(img)],
                     capture_output=True,timeout=70)
    if r.returncode or not r.stdout:raise RuntimeError(name+": "+r.stderr.decode(errors="replace")[-180:])
    base=stock["files"][name]
    result["configs"][name]={"same_sha":sha(r.stdout)==base["sha8054"],
       "ota_sha":sha(r.stdout),"stock8054_sha":base["sha8054"],
       "ota_length":len(r.stdout),"stock_length":base["bytes"][1]}
    print("CONFIG",name,result["configs"][name]["same_sha"],flush=True)
dtbo=a.images/"dtbo.img"
if dtbo.exists():
    with dtbo.open("rb") as f:
        hdr=f.read(32);magic,total,hl,entrysize,count,offset,page,version=struct.unpack(">8I",hdr)
        assert magic==0xd7b7ab1e and entrysize==32 and count==207
        f.seek(offset);toc=f.read(entrysize*count)
        hashes=[]
        for i in range(count):
            size,pos,*_=struct.unpack(">8I",toc[i*entrysize:(i+1)*entrysize][:32])
            f.seek(pos);data=f.read(size)
            assert len(data)==size and data[:4]==bytes.fromhex("d00dfeed")
            hashes.append(sha(data))
    result["dtbo"]={"entries":count,"unique_hashes":len(set(hashes)),
                     "image_sha":sha(dtbo.read_bytes()),
                     "stock8054_blob_compare":"not performed: full stock per-blob SHA list not committed"}

files={
"TvSettingsPlus":"system_ext/priv-app/TvSettingsPlus/TvSettingsPlus.apk",
"Factory":"system_ext/app/Factory/Factory.apk",
"KeystoneCorrection":"system/system/priv-app/KeystoneCorrection/KeystoneCorrection.apk",
"RuiAutoFocus":"system/system/app/RuiAutoFocus/RuiAutoFocus.apk",
"KuSourceRJ":"system/system/app/KuSourceRJ/KuSourceRJ.apk",
"trdservice":"system/system/app/trdservice/trdservice.apk",
"trdmiddle":"vendor/priv-app/trdmiddle/trdmiddle.apk",
"KuSettings":"system/system/app/KuSettings/KuSettings.apk",
"RuiYunOta":"system/system/priv-app/RuiYunOta/RuiYunOta.apk",
"KuSetupWizard":"system/system/app/KuSetupWizard/KuSetupWizard.apk",
"Provision":"system_ext/priv-app/Provision/Provision.apk"}
for name,rel in files.items():
    path=a.erofs/rel
    old=origapps.get(name,{}).get("two",{})
    if isinstance(old,str):old={}
    if not path.is_file():
        result["apps"][name]={"ota_present":False,"stock8054_recorded":bool(old)}
        print("APK MISSING",name,flush=True);continue
    data=path.read_bytes()
    with zipfile.ZipFile(path) as z:
        dex={n:{"sha256":sha(z.read(n)),"size":z.getinfo(n).file_size}
             for n in z.namelist() if re.fullmatch(r"classes\d*\.dex",n)}
    factory_sha=old.get("apk_sha256")
    factory_dex=old.get("dex_sha256")
    result["apps"][name]={"ota_present":True,"ota_sha":sha(data),
       "stock8054_sha":factory_sha,
       "same_apk":sha(data)==factory_sha if factory_sha else None,
       "same_dex":dex==factory_dex if factory_dex else None,
       "ota_dex":dex,"stock8054_dex":factory_dex}
    print("APK",name,"same_apk",result["apps"][name]["same_apk"],
          "same_dex",result["apps"][name]["same_dex"],flush=True)
vendor=a.erofs/"vendor/build.prop"
if vendor.exists():
    for line in vendor.read_text(errors="replace").splitlines():
        if not line or line.startswith("#") or "=" not in line:continue
        k,v=line.split("=",1)
        safe=re.fullmatch(r"ro\.rjpj\.(?:machine\.id|hdmi\.[a-zA-Z0-9_.]+|support\.toffunction|autofocus\.[a-zA-Z0-9_.]+|autokeystone\.[a-zA-Z0-9_.]+|yunota\.(?:version|url|zip))",k)
        if safe or k in ("ro.product.ota","ro.zeasn.devicetype"):
            baseline=stock.get("oem_properties",{}).get(k,{})
            result["props"][k]={"ota8052":v[:180],"factory8054":baseline.get("8054"),
                                 "same":v==baseline["8054"] if "8054" in baseline else None}
native=[
"system/system/lib/libsettingsi2c_jni.so",
"system/system/lib/libfactoryi2c_jni.so",
"system/system/lib/libi2c_jni.so",
"system/system/lib/libtrd_jni.so",
"system/system/lib/libtof_jni.so",
"system/system/lib/librjpj_private_function.so",
"vendor/lib/modules/ruimotor.ko",
"vendor/lib/modules/stmvl53l1.ko",
"vendor/etc/audio_policy_configuration.xml"]
for name in native:
    f=a.erofs/name
    result["libs"][name]={"present_ota8052":f.is_file(),
                          "sha256":sha(f.read_bytes()) if f.is_file() else None}
(a.out/"comparison.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
lines=["# October OTA 8052 vs September stock 8054","",
"Comparison of verified original sources, no OEM code published, no device flashed.",
"Old August 8052 versus September 8054 differences can reflect software updates instead of board changes.",
"",
"## Board and audio configuration SHA comparison","",
"| File | Identical latest 8052 vs factory 8054 |","|---|---|"]
for name,row in result["configs"].items():
    lines.append("| "+name+" | "+("YES" if row["same_sha"] else "NO")+" |")
lines+=["","## Android OEM app APK and DEX comparison","",
"| App | OTA present | APK identical to 8054 | All DEX identical to 8054 |","|---|---|---|---|"]
for name,row in result["apps"].items():
    lines.append("| "+name+" | "+str(row["ota_present"])+" | "+str(row.get("same_apk"))+" | "+str(row.get("same_dex"))+" |")
lines+=["","## OTA 8052 vs factory 8054 profile values","","| Property | OTA 8052 | Factory 8054 |","|---|---|---|"]
for name,row in sorted(result["props"].items()):
    lines.append("| "+name+" | "+row["ota8052"].replace("|","/")+" | "+str(row["factory8054"]).replace("|","/")+" |")
lines+=["","## Key OEM drivers/libraries in latest 8052 OTA","",
"| File | Present in latest 8052 OTA |","|---|---|"]
for name,row in result["libs"].items():lines.append("| "+name+" | "+str(row["present_ota8052"])+" |")
lines+=["","## Limits and recommended next research","",
"- Identical APKs mean identical bytes; differing hashes do not identify particular changed methods.",
"- OEM driver binary equality with factory 8054 cannot be inferred from OTA file presence alone.",
"- DTBO per-blob match with 8054 needs verified stock per-entry hashes in a later run.",
"- Never deduce physical wiring from identical firmware config hashes.",
"- Real device tests must verify Binder service permissions, bootloader/AVB enforcement, recovery and HDMI/ToF behavior.",
"- Keep separate board profiles and use device-matched installation packages until recovery and signatures are proven.",
"- 8053 is not a target hardware profile.",
""]
(a.out/"README.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print("DONE",a.out,flush=True)
