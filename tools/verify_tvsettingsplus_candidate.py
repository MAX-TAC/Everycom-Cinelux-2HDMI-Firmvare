#!/usr/bin/env python3
"""Fail-closed round-trip verification of rebuilt, signed experimental TvSettingsPlus.

Compare original decoded system APK manifest against decoded candidate manifest:
- original exported Activities and services/receivers/providers unchanged
- permissions and sharedUserId unchanged
- new CineLux user interface intents actually present after aapt2 resource rebuild
- all four OEM system menu flavors actually contain working target intents
No Android system operations and no installation.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from lxml import etree

ANDROID = "{http://schemas.android.com/apk/res/android}"
MAIN = "com.android.tv.settings.MainSettings"
NEW = {"com.android.tv.settings.cinelux.TemperatureInfoActivity",
       "com.android.tv.settings.cinelux.LegacySettingsRouterActivity"}
SCREENS = ("device.xml","device_two_panel.xml","device_vendor.xml","device_x.xml")
ROUTES = {
 "cinelux_projector_panel":("com.android.tv.settings","com.android.tv.settings.uicustom.MainActivity"),
 "cinelux_temperature":("com.android.tv.settings","com.android.tv.settings.cinelux.TemperatureInfoActivity"),
 "cinelux_brightness":("com.coolux.source","com.coolux.source.activity.BrightActivity"),
 "cinelux_sound":("com.coolux.source","com.coolux.source.activity.VoiceActivity"),
 "cinelux_boot_source":("com.coolux.source","com.coolux.source.activity.BootSoureActivity"),
 "cinelux_power_mode":("com.coolux.source","com.coolux.source.activity.PoweronModeActivity"),
 "cinelux_orientation":("com.coolux.source","com.coolux.source.activity.ProjectModelActivity"),
 "cinelux_keystone":("com.coolux.source","com.coolux.source.activity.KeystoneActivity"),
 "cinelux_ota":("com.rjpj.yunota","com.rjpj.yunota.OTASystemNetworkUpdateActivity"),
}

def elements(m, section):
    app = m.getroot().find("application")
    return {(el.tag, el.get(ANDROID+"name")):el for el in app if el.tag in section}

def verify(original: Path,candidate_dir: Path)->None:
    base=etree.parse(str(original))
    built=etree.parse(str(candidate_dir/"AndroidManifest.xml"))
    expected_package="com.android.tv.settings"
    assert base.getroot().get("package") == expected_package
    assert built.getroot().get("package") == expected_package
    for field in ("sharedUserId","sharedUserMaxSdkVersion","installLocation"):
        assert base.getroot().get(ANDROID+field) == built.getroot().get(ANDROID+field), field+" changed"
    base_permissions={x.get(ANDROID+"name") for x in base.getroot() if x.tag.startswith("uses-permission")}
    built_permissions={x.get(ANDROID+"name") for x in built.getroot() if x.tag.startswith("uses-permission")}
    assert base_permissions == built_permissions, "Original package permissions changed"
    names={"activity","service","receiver","provider"}
    existing=elements(base,names);updated=elements(built,names)
    missing=set(existing)-set(updated)
    assert not missing,"Lost OEM components: "+str(missing)
    for key,old in existing.items():
        new=updated[key]
        for field in ("exported","enabled","permission","process"):
            assert old.get(ANDROID+field)==new.get(ANDROID+field),f"Changed OEM {key} {field}"
    assert {(tag,name) for tag,name in updated.keys()-existing.keys()} == {
        ("activity",x) for x in NEW}, "Unexpected extra Manifest components"
    main=updated[("activity",MAIN)]
    actions={a.get(ANDROID+"name") for filt in main.findall("intent-filter")
              for a in filt.findall("action")}
    assert "android.settings.SETTINGS" in actions,"MainSettings no ACTION_SETTINGS"
    for file in SCREENS:
        screen=etree.parse(str(candidate_dir/"res"/"xml"/file))
        root=screen.getroot()
        prefs={x.get(ANDROID+"key"):x for x in root.iter() if x.tag=="Preference"}
        for key, target in ROUTES.items():
            assert key in prefs,f"Missing {key} in {file}"
            intents=prefs[key].findall("intent")
            assert len(intents)==1,(file,key,"expected one intent")
            i=intents[0]
            assert (i.get(ANDROID+"targetPackage"),i.get(ANDROID+"targetClass"))==target,(file,key,"bad intent target")
    print(f"PASSED: {len(existing)} stock AndroidManifest components retained, {len(base_permissions)} permissions retained,")
    print("        original sharedUserId intact, 2 new CineLux Activities and 9 routes x 4 TV screen flavors visible after rebuild.")
    print("LIMIT: Static resource validation; live package update, privilege grants and interaction NOT tested.")

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("original_manifest",type=Path)
    ap.add_argument("candidate_decoded",type=Path)
    x=ap.parse_args()
    verify(x.original_manifest,x.candidate_decoded)

if __name__=="__main__":
    main()
