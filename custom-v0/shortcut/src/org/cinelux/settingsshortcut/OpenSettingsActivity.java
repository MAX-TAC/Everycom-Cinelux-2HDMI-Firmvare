package org.cinelux.settingsshortcut;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.os.Bundle;

/** Non-privileged, explicit Activity shortcut; no persistent system settings writes. */
public final class OpenSettingsActivity extends Activity {
  @Override
  public void onCreate(Bundle state) {
    super.onCreate(state);
    Intent target = new Intent(Intent.ACTION_MAIN);
    target.setClassName("com.android.tv.settings",
                        "com.android.tv.settings.MainSettings");
    target.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
    try {
      startActivity(target);
      finish();
    } catch (ActivityNotFoundException | SecurityException exception) {
      new AlertDialog.Builder(this)
          .setMessage(R.string.settings_not_found)
          .setPositiveButton(R.string.ok, (dialog, which) -> finish())
          .setOnCancelListener(dialog -> finish())
          .show();
    }
  }
}
