package com.android.tv.settings.cinelux;

import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.Locale;

/**
 * STAGING SOURCE: read-only system temperature screen to compile INTO TvSettingsPlus.
 * No JNI, shell, root, PWM, calibration, GPIO, or thermal policy writes.
 * A sensor label is only inferred when the original kernel zone type identifies it.
 */
public final class TemperatureInfoActivity extends Activity {
    private LinearLayout rows;

    @Override
    protected void onCreate(Bundle saved) {
        super.onCreate(saved);
        LinearLayout layout = new LinearLayout(this);
        layout.setOrientation(LinearLayout.VERTICAL);
        layout.setPadding(44, 36, 44, 36);
        layout.setBackgroundColor(Color.rgb(24, 28, 34));
        TextView header = new TextView(this);
        header.setText("Температура оборудования");
        header.setTextSize(27f);
        header.setTextColor(Color.WHITE);
        layout.addView(header);
        TextView caution = new TextView(this);
        caution.setText("Только реальные показания датчиков ядра. Температура SoC не является температурой LCD или LED.");
        caution.setTextColor(Color.LTGRAY);
        caution.setTextSize(16f);
        caution.setPadding(0, 12, 0, 20);
        layout.addView(caution);
        Button reload = new Button(this);
        reload.setText("Обновить показания");
        reload.setFocusable(true);
        reload.setOnClickListener(new View.OnClickListener() {
            @Override public void onClick(View view) { refresh(); }
        });
        layout.addView(reload);
        ScrollView scroll = new ScrollView(this);
        rows = new LinearLayout(this);
        rows.setOrientation(LinearLayout.VERTICAL);
        rows.setGravity(Gravity.TOP);
        scroll.addView(rows);
        layout.addView(scroll, new LinearLayout.LayoutParams(-1, 0, 1.0f));
        setContentView(layout);
        refresh();
        reload.requestFocus();
    }

    private void refresh() {
        rows.removeAllViews();
        File base = new File("/sys/class/thermal");
        File[] zones = base.listFiles();
        int valid = 0;
        if (zones != null) {
            for (File zone : zones) {
                if (!zone.getName().startsWith("thermal_zone")) continue;
                String type = readSmallText(new File(zone, "type"));
                String temperature = readSmallText(new File(zone, "temp"));
                if (type == null || temperature == null) continue;
                try {
                    double raw = Double.parseDouble(temperature);
                    double celsius = Math.abs(raw) >= 500 ? raw / 1000.0 : raw;
                    if (celsius <= 0 || celsius > 130 || Double.isNaN(celsius)) continue;
                    addLine(label(type) + ": " + String.format(Locale.ROOT, "%.1f °C", celsius));
                    valid++;
                } catch (NumberFormatException ignored) {
                    // A disabled or unreadable thermal zone does not yield a temperature.
                }
            }
        }
        if (valid == 0) {
            addLine("Доступных показаний температуры нет. Проверьте права чтения Thermal HAL.");
        }
        addLine("LCD-матрица: датчик не подтверждён");
        addLine("LED / источник света: датчик не подтверждён");
    }

    private void addLine(String text) {
        TextView item = new TextView(this);
        item.setText(text);
        item.setTextColor(Color.WHITE);
        item.setTextSize(19f);
        item.setPadding(0, 14, 0, 14);
        rows.addView(item);
    }

    private static String label(String raw) {
        String type = raw.trim();
        if (type.equalsIgnoreCase("mtk-thermal")) return "Процессор (SoC)";
        if (type.equalsIgnoreCase("gpu-thermal")) return "Графический процессор (GPU)";
        if (type.equalsIgnoreCase("apu-thermal")) return "Нейропроцессор (APU)";
        return "Датчик " + type;
    }

    private static String readSmallText(File f) {
        if (!f.isFile() || !f.canRead()) return null;
        try (BufferedReader reader = new BufferedReader(new FileReader(f))) {
            String text = reader.readLine();
            return text == null || text.length() > 150 ? null : text.trim();
        } catch (IOException | SecurityException ignored) {
            return null;
        }
    }
}
