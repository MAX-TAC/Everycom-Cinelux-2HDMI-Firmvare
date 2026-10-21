package org.cinelux.settingsshortcut;

import android.app.Activity;
import android.graphics.Color;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.PowerManager;
import android.text.format.DateFormat;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import java.util.Date;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Informational diagnostics only. Explicitly exported so stock TvSettingsPlus
 * can launch this Activity from a future "System" preference without replacing
 * platform-signed Settings. For now it is available in the TV launcher.
 */
public final class ThermalInfoActivity extends Activity {
    private static final long REFRESH_MS = 10000;
    private final Handler handler = new Handler(Looper.getMainLooper());
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private LinearLayout content;
    private boolean visible;
    private boolean busy;
    private final Runnable refreshTick = new Runnable() {
        @Override public void run() {
            if (!visible) return;
            requestSnapshot();
            handler.postDelayed(this, REFRESH_MS);
        }
    };

    @Override
    public void onCreate(Bundle state) {
        super.onCreate(state);
        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackgroundColor(Color.rgb(15, 20, 28));

        content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        content.setPadding(dp(40), dp(32), dp(40), dp(32));
        scroll.addView(content);
        setContentView(scroll);
        heading(getString(R.string.thermal_title), 28);
        description(getString(R.string.thermal_warning));
        Button refresh = new Button(this);
        refresh.setText(R.string.thermal_refresh);
        refresh.setOnClickListener(view -> requestSnapshot());
        LinearLayout.LayoutParams bp = new LinearLayout.LayoutParams(dp(230), dp(64));
        bp.topMargin = dp(12);
        bp.bottomMargin = dp(12);
        content.addView(refresh, bp);
        refresh.requestFocus();
        showMessage(getString(R.string.thermal_loading));
    }

    @Override public void onResume() {
        super.onResume();
        visible = true;
        handler.removeCallbacks(refreshTick);
        handler.post(refreshTick);
    }

    @Override public void onPause() {
        visible = false;
        handler.removeCallbacks(refreshTick);
        super.onPause();
    }

    @Override public void onDestroy() {
        worker.shutdownNow();
        super.onDestroy();
    }

    private void requestSnapshot() {
        if (busy) return;
        busy = true;
        worker.execute(() -> {
            final ThermalProbe.Snapshot snapshot = ThermalProbe.collect();
            runOnUiThread(() -> {
                busy = false;
                if (isFinishing() || isDestroyed()) return;
                render(snapshot);
            });
        });
    }

    private void render(ThermalProbe.Snapshot snapshot) {
        // Preserve title, disclaimer and refresh button while replacing data rows.
        while (content.getChildCount() > 3) {
            content.removeViewAt(3);
        }
        description(getString(R.string.thermal_last_update)
                + " " + DateFormat.getTimeFormat(this).format(new Date()));
        section(getString(R.string.thermal_optical), null);
        row(getString(R.string.thermal_lcd), getString(R.string.thermal_unconfirmed));
        row(getString(R.string.thermal_led), getString(R.string.thermal_unconfirmed));

        section(getString(R.string.thermal_sensors), snapshot.temperatures);
        section(getString(R.string.thermal_fans), snapshot.fans);
        section(getString(R.string.thermal_states), snapshot.coolingStates);
        description(getString(R.string.thermal_footer) + " "
                + getString(R.string.thermal_android_state) + " "
                + androidThermalState());
    }

    private String androidThermalState() {
        if (Build.VERSION.SDK_INT < 29) return getString(R.string.thermal_unavailable);
        PowerManager pm = (PowerManager) getSystemService(POWER_SERVICE);
        if (pm == null) return getString(R.string.thermal_unavailable);
        try {
            int status = pm.getCurrentThermalStatus();
            switch (status) {
                case PowerManager.THERMAL_STATUS_NONE: return "NONE";
                case PowerManager.THERMAL_STATUS_LIGHT: return "LIGHT";
                case PowerManager.THERMAL_STATUS_MODERATE: return "MODERATE";
                case PowerManager.THERMAL_STATUS_SEVERE: return "SEVERE";
                case PowerManager.THERMAL_STATUS_CRITICAL: return "CRITICAL";
                case PowerManager.THERMAL_STATUS_EMERGENCY: return "EMERGENCY";
                case PowerManager.THERMAL_STATUS_SHUTDOWN: return "SHUTDOWN";
                default: return String.valueOf(status);
            }
        } catch (SecurityException | RuntimeException ex) {
            return getString(R.string.thermal_unavailable);
        }
    }

    private void section(String name, List<ThermalProbe.Entry> rows) {
        heading(name, 22);
        if (rows == null) return;
        if (rows.isEmpty()) {
            row(getString(R.string.thermal_no_data), getString(R.string.thermal_unavailable));
            return;
        }
        for (ThermalProbe.Entry e : rows) {
            row(e.name, e.value);
        }
    }

    private void heading(String txt, float sp) {
        TextView view = label(txt, sp, Color.WHITE);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        lp.topMargin = dp(15);
        lp.bottomMargin = dp(12);
        content.addView(view, lp);
    }

    private void description(String txt) {
        TextView view = label(txt, 15, Color.rgb(173, 188, 201));
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, LinearLayout.LayoutParams.WRAP_CONTENT);
        lp.bottomMargin = dp(8);
        content.addView(view, lp);
    }

    private void showMessage(String txt) {
        description(txt);
    }

    private void row(String key, String value) {
        LinearLayout line = new LinearLayout(this);
        line.setOrientation(LinearLayout.HORIZONTAL);
        line.setGravity(Gravity.CENTER_VERTICAL);
        line.setPadding(0, dp(7), 0, dp(7));
        TextView left = label(key, 17, Color.WHITE);
        left.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 2));
        TextView right = label(value, 17, Color.rgb(146, 186, 220));
        right.setGravity(Gravity.END);
        right.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1));
        line.addView(left);
        line.addView(right);
        content.addView(line);
    }

    private TextView label(String txt, float sp, int color) {
        TextView view = new TextView(this);
        view.setText(txt);
        view.setTextSize(sp);
        view.setTextColor(color);
        return view;
    }

    private int dp(int px) {
        return (int) (px * getResources().getDisplayMetrics().density + .5f);
    }
}
