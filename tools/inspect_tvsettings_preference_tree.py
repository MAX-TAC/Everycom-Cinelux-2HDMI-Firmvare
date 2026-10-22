#!/usr/bin/env python3
"""Read-only summary of decoded TvSettingsPlus preference XML resources.

Used to find the correct Android TV "System" screen without guessing OEM ids.
Contains ONLY file names and key/title/intent metadata, not OEM layouts/values.
"""
import json
from pathlib import Path
from lxml import etree

p = Path("/tmp/tvmod/decoded/res/xml")
summary=[]
for f in sorted(p.glob("*.xml")):
    try:
        tree=etree.parse(str(f))
    except (OSError,etree.XMLSyntaxError):
        continue
    root=tree.getroot()
    ns="{http://schemas.android.com/apk/res/android}"
    attrs=[]
    for element in root.iter():
        name=element.tag.split("}")[-1]
        if name in {"PreferenceScreen","PreferenceCategory","Preference","SwitchPreference","TwoStatePreference"} or "Preference" in name:
            item={"tag":name}
            for key in ["key","title","summary","fragment","order"]:
                v=element.get(ns+key)
                if v is not None:item[key]=v
            if len(item)>1:
                attrs.append(item)
    fn=f.name.lower()
    likely=any(word in fn for word in ["main","system","device","setting","about","project","general","menu","root"])
    likely=likely or any("system" in str(x.get("key","")).lower() or "system" in str(x.get("title","")).lower() for x in attrs)
    if likely:
        summary.append({"name":f.name,"root":root.tag.split("}")[-1],"preferences":attrs[:90],"total_preferences":len(attrs)})
out=Path("/tmp/tvmod/preferences_inventory.json")
out.write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("PREFERENCE_SUMMARY_FILES="+str(len(summary)))
for entry in summary:
    print("FILE "+entry["name"]+" root="+entry["root"]+" pref="+str(entry["total_preferences"]))
    for item in entry["preferences"][:11]:
        print("   "+json.dumps(item,ensure_ascii=False))
