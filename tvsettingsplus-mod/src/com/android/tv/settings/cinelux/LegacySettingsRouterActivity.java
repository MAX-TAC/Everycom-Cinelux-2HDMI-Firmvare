package com.android.tv.settings.cinelux;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.ComponentName;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;

/**
 * STAGING SOURCE ONLY. Must be built into the original TvSettingsPlus package,
 * not installed as a standalone APK. Hardware backends remain in their OEM APKs.
 *
 * Only whitelisted USER-FACING legacy implicit actions are forwarded.
 * Explicit external calls to com.my.settings are NOT solved by this class.
 * Unsupported or factory actions are deliberately not redirected.
 */
public final class LegacySettingsRouterActivity extends Activity {
    private static final String TAG = "CineLuxLegacyRoute";
    private static final String TV = "com.android.tv.settings";
    private static final String SOURCE = "com.coolux.source";
    private static final String OTA = "com.rjpj.yunota";

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        final String action = getIntent() == null ? null : getIntent().getAction();
        final ComponentName component = componentFor(action);
        if (component == null) {
            Log.w(TAG, "Unsupported OEM action; not opening a factory or destructive screen: " + action);
            finish();
            return;
        }
        try {
            Intent target = new Intent(Intent.ACTION_MAIN);
            target.setComponent(component);
            target.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            startActivity(target);
        } catch (ActivityNotFoundException | SecurityException error) {
            Log.e(TAG, "Target unavailable for action " + action + ": " + component, error);
        } finally {
            finish();
        }
    }

    /**
     * Derived from 8052 OTA manifest and jadx intent call names. Each route
     * still requires a live 8052+8054 test before the original app is disabled.
     */
    private static ComponentName componentFor(String action) {
        if (action == null) return null;
        switch (action) {
            case "android.settings.SETTINGS":
                return new ComponentName(TV, TV + ".MainSettings");
            case "android.settings.WIFI_SETTINGS":
                return new ComponentName(TV, TV + ".connectivity.NetworkActivity");
            case "android.settings.BLUETOOTH_SETTINGS":
                return new ComponentName(TV, TV + ".accessories.BluetoothAccessoryActivity");
            case "android.settings.AUTO_BLUETOOTH":
                return new ComponentName(TV, TV + ".accessories.AddAccessoryActivity");
            case "android.settings.DATETIME_SETTINGS":
                return new ComponentName(TV, TV + ".system.DateTimeActivity");
            case "android.settings.LAUGUAGE_SETTINGS":
            case "android.settings.LAUGUAGE_LOCAL_SETTINGS":
                // Original OEM actions contain the misspelling LAUGUAGE.
                return new ComponentName(TV, TV + ".system.LanguageActivity");
            case "android.settings.ALLAPPS":
                return new ComponentName(TV, TV + ".device.apps.AllAppsActivity");
            case "android.settings.PROJECTABOUT_SETTINGS":
                return new ComponentName(TV, TV + ".about.AboutActivity");
            case "android.settings.BRIGHT_SETTINGS":
                return new ComponentName(SOURCE, SOURCE + ".activity.BrightActivity");
            case "android.settings.VOICE_SETTINGS":
                return new ComponentName(SOURCE, SOURCE + ".activity.VoiceActivity");
            case "android.settings.PROJECTMODEL_SETTINGS":
                return new ComponentName(SOURCE, SOURCE + ".activity.ProjectModelActivity");
            case "android.settings.BOOTSOURE_SETTINGS":
                // Preserve the vendor's unusual original spelling BOOTSOURE.
                return new ComponentName(SOURCE, SOURCE + ".activity.BootSoureActivity");
            case "android.settings.POWERMODE_SETTINGS":
                return new ComponentName(SOURCE, SOURCE + ".activity.PoweronModeActivity");
            case "android.settings.KEYSTONE_SETTINGS":
                return new ComponentName(SOURCE, SOURCE + ".activity.KeystoneActivity");
            case "android.settings.SYSTEMUPDATE":
                return new ComponentName(OTA, OTA + ".OTASystemNetworkUpdateActivity");
            // SCREENSHOT_SETTINGS: unsupported until ScreenServices equivalent implemented.
            // Do not expose factory calibration, flash, reset, raw I2C or motor commands.
            default:
                return null;
        }
    }
}
