#!/usr/bin/env python3
"""Unit tests for fail-closed decoded TvSettingsPlus manifest route patch."""
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from patch_tvsettingsplus_manifest import patch_manifest

SAMPLE = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
 package="com.android.tv.settings"><application>
<activity android:name=".MainSettings" android:exported="true">
<intent-filter><action android:name="android.intent.action.MAIN"/>
<category android:name="android.intent.category.LEANBACK_SETTINGS"/></intent-filter>
</activity></application></manifest>
"""


class ManifestRouteTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.f = Path(self.tmp.name) / "AndroidManifest.xml"
        self.f.write_text(SAMPLE, encoding="utf-8")

    def test_dry_run_is_read_only(self):
        before = self.f.read_bytes()
        self.assertIn("DRY RUN", patch_manifest(self.f, False))
        self.assertEqual(self.f.read_bytes(), before)

    def test_patch_and_idempotence(self):
        self.assertIn("PATCHED", patch_manifest(self.f, True))
        self.assertIn("ALREADY PRESENT", patch_manifest(self.f, True))
        self.assertTrue(self.f.with_suffix(".xml.before-cinelux").is_file())
        self.assertEqual(
            self.f.with_suffix(".xml.before-cinelux").read_text(encoding="utf-8"), SAMPLE
        )
        t = self.f.read_text(encoding="utf-8")
        self.assertEqual(t.count("android.settings.SETTINGS"), 1)

    def test_wrong_package_is_blocked(self):
        self.f.write_text(SAMPLE.replace("com.android.tv.settings", "com.bad.pkg"), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Unexpected APK package"):
            patch_manifest(self.f, True)

    def test_unexported_activity_is_blocked(self):
        self.f.write_text(SAMPLE.replace('android:exported="true"', 'android:exported="false"'), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unsafe baseline"):
            patch_manifest(self.f, True)

    def test_backup_never_overwritten(self):
        self.f.with_suffix(".xml.before-cinelux").write_text("important backup", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "backup"):
            patch_manifest(self.f, True)
        self.assertEqual(self.f.read_text(encoding="utf-8"), SAMPLE)


if __name__ == "__main__":
    unittest.main()
