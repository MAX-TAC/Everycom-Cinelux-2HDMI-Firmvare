#!/usr/bin/env python3
"""Read only factory bootdata_a and tvconfig_a ext4 assets, and export boot artwork.
Images are originals, no generated replacement logos. No hardware modifications.
Input is the decrypted vendor REE binary and the matching original upgrade_script.
"""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import subprocess,re,hashlib,argparse,json,collections,zipfile,os
p=argparse.ArgumentParser()
p.add_argument("--variant",choices=["8052","8054"],required=True)
p.add_argument("--plain",type=Path,required=True)
p.add_argument("--script",type=Path,required=True)
p.add_argument("--out",type=Path,required=True)
a=p.parse_args()
work=Path("/tmp/boot-assets-work")/a.variant
work.mkdir(parents=True,exist_ok=True)
a.out.mkdir(parents=True,exist_ok=True)
lines=a.script.read_text().splitlines()
parts={}
for i,line in enumerate(lines):
 if not line.startswith("filepartload "):continue
 cols=line.split()
 following=[]
 for s in lines[i+1:]:
  if s.startswith("filepartload "):break
  following.append(s)
 for kind in ["bootdata_a","tvconfig_a"]:
  if kind not in parts and any(re.search(r"\bpartition write mmc 0 "+kind+r"\b",e) for e in following):
   parts[kind]={"offset":int(cols[4],16),"compressed_size":int(cols[3],16)}
assert set(parts)=={"bootdata_a","tvconfig_a"},parts
report={"variant":a.variant,"baseline":{"8052":"8052 factory 2026-08-13","8054":"8054 factory 2026-09-30"}[a.variant],
        "partitions":parts,"artworks":[],"other_media_files":[],"boot_audio_candidates":[],"warnings":[]}
def sh(args,timeout=240):
 proc=subprocess.run(args,capture_output=True,text=True,errors="replace",timeout=timeout)
 if proc.returncode:raise RuntimeError(" ".join(args[:3])+" "+proc.stderr[-450:])
 return proc.stdout
def sha(path):
 h=hashlib.sha256()
 with open(path,"rb") as stream:
  for block in iter(lambda:stream.read(1024*1024),b""):h.update(block)
 return h.hexdigest()
for kind,entry in parts.items():
 compressed=work/(kind+".lz4")
 with a.plain.open("rb") as inp,compressed.open("wb") as out:
  inp.seek(entry["offset"]-4096)
  remain=entry["compressed_size"]
  while remain:
   chunk=inp.read(min(remain,8*1024*1024))
   if not chunk:raise EOFError(kind)
   out.write(chunk);remain-=len(chunk)
 image=work/(kind+".img")
 sh(["lz4","-q","-d","-f",str(compressed),str(image)])
 compressed.unlink(missing_ok=True)
 entry["bytes"]=image.stat().st_size
 entry["sha256"]=sha(image)
 fsdir=work/(kind+"_contents")
 fsdir.mkdir(exist_ok=True)
 sh(["debugfs","-R",f"rdump / {fsdir}",str(image)],timeout=300)
 files=[f for f in fsdir.rglob("*") if f.is_file()]
 entry["file_count"]=len(files)
 matched=[f for f in files if f.name.lower()=="boot0.jpg"]
 for f in matched:
  try:
   img=Image.open(f)
   img.load()
   assert img.format in ("JPEG","PNG")
   assert 1<=img.width<=8192 and 1<=img.height<=8192
  except Exception as e:
   report["warnings"].append(str(f)+": image decode failed "+str(e));continue
  dest=a.out/f"{a.variant}_{kind}_{f.name}"
  dest.write_bytes(f.read_bytes())
  report["artworks"].append({"partition":kind,"original_path":f.relative_to(fsdir).as_posix(),
    "export":dest.name,"width":img.width,"height":img.height,
    "bytes":f.stat().st_size,"sha256":sha(f),"format":img.format})
 for f in files:
  name=f.name.lower()
  rel=f.relative_to(fsdir).as_posix()
  if any(tag in name for tag in ("boot","logo","start","splash","poweron","power_on","welcome")):
   report["other_media_files"].append({"partition":kind,"path":rel,"size":f.stat().st_size})
  if f.suffix.lower() in (".wav",".ogg",".mp3",".aac",".m4a",".flac",".mid",".amr"):
   report["boot_audio_candidates"].append({"partition":kind,"path":rel,"size":f.stat().st_size})
 print("SCANNED",a.variant,kind,len(files),"images",len(matched),flush=True)
# To avoid exposing any factory private data, export only specifically named public boot images.
thumbs=[]
for a0 in report["artworks"]:
 im=Image.open(a.out/a0["export"]).convert("RGB")
 thumbs.append((im.copy(),a0))
if thumbs:
 w=640; panel_h=390
 board=Image.new("RGB",(w,len(thumbs)*panel_h),(18,22,29))
 draw=ImageDraw.Draw(board)
 for k,(im,meta) in enumerate(thumbs):
  im.thumbnail((w-24,panel_h-55))
  xx=(w-im.width)//2
  yy=k*panel_h+14
  board.paste(im,(xx,yy))
  draw.text((12,(k+1)*panel_h-33),
    f"{meta['partition']}/{meta['original_path']}  |  {meta['width']} x {meta['height']}",
    fill=(230,234,240))
 output=a.out/f"{a.variant}_boot0_preview.jpg"
 board.save(output,quality=88)
report_path=a.out/f"{a.variant}_boot_artwork_inventory.json"
report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
print("ARTWORK",json.dumps(report["artworks"],ensure_ascii=False),flush=True)
print("AUDIO",report["boot_audio_candidates"],flush=True)
