# @category ReverseEngineering
# Post-analysis: summarize actual Ghidra XREFs and decompile key-related functions.
from ghidra.app.decompiler import DecompInterface
from ghidra.program.model.symbol import RefType
import os,json
fm=currentProgram.getFunctionManager()
refman=currentProgram.getReferenceManager()
envpath=os.getenv("GHIDRA_AVB_OUTPUT") or "/tmp/ghidra8052_report.json"
targets={
  "key_blob_start":0x1cdaac, "key_blob_inner":0x1cdb40,
  "avb_verification_failure":0x18723b,
  "avb_locked_dmverity":0x18a8d4,
  "avb_initialize_failed":0x18a830,
  "vbmeta_invalid_header":0x1a0477,
  "vbmeta_signature_error":0x1a0452,
  "developer_signature_accepted":0x19fb0f,
  "developer_signature_rejected":0x19fb46,
  "avb_init_command":0x18df01,
  "avb_verify_command":0x18ef80,
  "avb_device_locked":0x18ab9c,
  "verified_green_state":0x1843b1,
  "verified_orange_state":0x1843d5,
  "rollback_failed":0x18aa3a,
  "u_boot_avb_verification_file":0x1a0e50
}
def h(x):
    return "0x%x"%x
data={
   "image_name":str(currentProgram.getName()),
   "language":str(currentProgram.getLanguage().getLanguageID()),
   "image_base":str(currentProgram.getImageBase()),
   "boot_entry":"0x400",
   "function_count":0,
   "targets":{},
   "candidate_functions":[]
}
for f in fm.getFunctions(True):
    data["function_count"]+=1
fnmap={}
for name,pos in targets.items():
    a=toAddr(pos)
    ref_out=[]
    for ref in refman.getReferencesTo(a):
        orig=ref.getFromAddress()
        f=fm.getFunctionContaining(orig)
        if f is not None: fnmap[str(f.getEntryPoint())]=f
        if len(ref_out)<35:
            ref_out.append({"from":str(orig),"type":str(ref.getReferenceType()),
                "function":str(f.getEntryPoint()) if f is not None else None})
    data["targets"][name]={"offset":h(pos),"reference_count":len(ref_out),"references":ref_out}
print("GHIDRA_STATS",data["language"],data["image_base"],"functions",data["function_count"],"target_functions",len(fnmap))
dec=DecompInterface()
dec.openProgram(currentProgram)
# Prioritize functions containing security-sensitive diagnostic strings.
priority=[]
for label in ["key_blob_start","key_blob_inner","avb_locked_dmverity","developer_signature_accepted",
              "developer_signature_rejected","avb_verification_failure","vbmeta_invalid_header",
              "rollback_failed","avb_verify_command"]:
    for ref in data["targets"][label]["references"]:
        k=ref["function"]
        if k and k not in priority:priority.append(k)
for k in priority[:12]:
    f=fnmap.get(k)
    if f is None:continue
    item={"address":k,"name":str(f.getName()),
          "size_bytes":f.getBody().getNumAddresses(),
          "callers":[],"callees":[]}
    for ref in refman.getReferencesTo(f.getEntryPoint()):
        if len(item["callers"])>=15:break
        if ref.getReferenceType().isCall(): item["callers"].append(str(ref.getFromAddress()))
    iter_ins=currentProgram.getListing().getInstructions(f.getBody(),True)
    seen=set()
    while iter_ins.hasNext():
        instr=iter_ins.next()
        for reference in instr.getReferencesFrom():
            if reference.getReferenceType().isCall():
                dest=str(reference.getToAddress())
                if dest not in seen and len(item["callees"])<35:
                    item["callees"].append(dest);seen.add(dest)
    try:
        result=dec.decompileFunction(f,60,monitor)
        if result.decompileCompleted() and result.getDecompiledFunction() is not None:
            code=result.getDecompiledFunction().getC()
            item["decompiled_excerpt"]=code[:2400]
        else:item["decompile_error"]=str(result.getErrorMessage())
    except Exception as e:
        item["decompile_error"]=str(e)
    data["candidate_functions"].append(item)
with open(envpath,"w") as out:
    json.dump(data,out,indent=2,sort_keys=True)
print("GHIDRA_SAVED",envpath,"decompiled",len(data["candidate_functions"]))
for k in data["targets"]:
    if data["targets"][k]["references"]:
        print("XREF",k,data["targets"][k]["offset"],len(data["targets"][k]["references"]))
