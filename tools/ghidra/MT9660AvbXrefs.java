// @category ReverseEngineering
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import com.google.gson.GsonBuilder;
import java.io.FileWriter;
import java.util.*;

public class MT9660AvbXrefs extends GhidraScript {
    @Override protected void run() throws Exception {
        FunctionManager fm=currentProgram.getFunctionManager();
        ReferenceManager rm=currentProgram.getReferenceManager();
        LinkedHashMap<String,Object> report=new LinkedHashMap<String,Object>();
        report.put("image",currentProgram.getName());
        report.put("language",currentProgram.getLanguage().getLanguageID().toString());
        report.put("image_base",currentProgram.getImageBase().toString());
        report.put("boot_entry", "0x400");
        int funcs=0;
        FunctionIterator fit=fm.getFunctions(true);
        while(fit.hasNext()){fit.next();funcs++;}
        report.put("function_count",funcs);
        LinkedHashMap<String,Long> targets=new LinkedHashMap<String,Long>();
        targets.put("root_key_start",0x1cdaacL);
        targets.put("root_key_interior",0x1cdb40L);
        targets.put("avb_verification_failure",0x18723bL);
        targets.put("avb_locked_dmverity",0x18a8d4L);
        targets.put("avb_initialize_failed",0x18a830L);
        targets.put("vbmeta_invalid_header",0x1a0477L);
        targets.put("vbmeta_signature_error",0x1a0452L);
        targets.put("developer_signature_accepted",0x19fb0fL);
        targets.put("developer_signature_rejected",0x19fb46L);
        targets.put("avb_init_command",0x18df01L);
        targets.put("avb_verify_command",0x18ef80L);
        targets.put("verified_green_state",0x1843b1L);
        targets.put("verified_orange_state",0x1843d5L);
        targets.put("rollback_failed",0x18aa3aL);
        LinkedHashMap<String,Object> resultTargets=new LinkedHashMap<String,Object>();
        LinkedHashMap<String,Function> candidates=new LinkedHashMap<String,Function>();
        for(Map.Entry<String,Long> ent: targets.entrySet()){
            Address a=toAddr(ent.getValue());
            List<Object> refs=new ArrayList<Object>();
            ReferenceIterator it=rm.getReferencesTo(a);
            int total=0;
            while(it.hasNext()){
                Reference ref=it.next();
                total++;
                Address from=ref.getFromAddress();
                Function f=fm.getFunctionContaining(from);
                if(f!=null)candidates.put(f.getEntryPoint().toString(),f);
                if(refs.size()<35){
                    LinkedHashMap<String,Object> one=new LinkedHashMap<String,Object>();
                    one.put("from",from.toString());
                    one.put("type",ref.getReferenceType().toString());
                    one.put("function",f==null?null:f.getEntryPoint().toString());
                    refs.add(one);
                }
            }
            LinkedHashMap<String,Object> summary=new LinkedHashMap<String,Object>();
            summary.put("offset",String.format("0x%x",ent.getValue()));
            summary.put("reference_count",total);
            summary.put("references",refs);
            resultTargets.put(ent.getKey(),summary);
            println("MT9660_XREF "+ent.getKey()+" count "+total);
        }
        report.put("targets",resultTargets);
        List<Object> selected=new ArrayList<Object>();
        DecompInterface dec=new DecompInterface();
        dec.openProgram(currentProgram);
        int count=0;
        for(Map.Entry<String,Function> ent: candidates.entrySet()){
            if(count++>=18)break;
            Function f=ent.getValue();
            LinkedHashMap<String,Object> fi=new LinkedHashMap<String,Object>();
            fi.put("address",f.getEntryPoint().toString());
            fi.put("name",f.getName());
            fi.put("bytes",f.getBody().getNumAddresses());
            List<String> callers=new ArrayList<String>();
            ReferenceIterator incoming=rm.getReferencesTo(f.getEntryPoint());
            while(incoming.hasNext()){
                Reference ref=incoming.next();
                if(ref.getReferenceType().isCall() && callers.size()<25)
                    callers.add(ref.getFromAddress().toString());
            }
            fi.put("callers",callers);
            List<String> callees=new ArrayList<String>();
            InstructionIterator instrs=currentProgram.getListing().getInstructions(f.getBody(),true);
            while(instrs.hasNext()){
                Instruction instr=instrs.next();
                for(Reference rr: instr.getReferencesFrom())
                    if(rr.getReferenceType().isCall() && !callees.contains(rr.getToAddress().toString()) && callees.size()<55)
                        callees.add(rr.getToAddress().toString());
            }
            fi.put("callees",callees);
            try{
                DecompileResults d=dec.decompileFunction(f,45,monitor);
                if(d.decompileCompleted() && d.getDecompiledFunction()!=null){
                    String c=d.getDecompiledFunction().getC();
                    fi.put("decompiled_excerpt",c.substring(0,Math.min(c.length(),2400)));
                }else{fi.put("decompile_error",d.getErrorMessage());}
            }catch(Exception e){fi.put("decompile_error",e.toString());}
            selected.add(fi);
        }
        report.put("candidate_functions",selected);
        String output=System.getenv("GHIDRA_AVB_OUTPUT");
        if(output==null || output.isEmpty())output="/tmp/ghidra_avb.json";
        FileWriter fw=new FileWriter(output);
        try{fw.write(new GsonBuilder().setPrettyPrinting().create().toJson(report));}
        finally{fw.close();}
        println("MT9660_REPORT_SAVED "+output+" functions "+funcs+" candidates "+selected.size());
    }
}
