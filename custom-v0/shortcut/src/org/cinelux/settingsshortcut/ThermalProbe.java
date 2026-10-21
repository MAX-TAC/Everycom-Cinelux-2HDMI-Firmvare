package org.cinelux.settingsshortcut;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;

/**
 * Strictly read-only thermal discovery for MT9660 Android 13.
 * No shell, no root, no writes to sysfs, no PWM/fan commands, no HAL control.
 * These generic Linux readings DO NOT identify the physical LCD or LED sensor.
 */
final class ThermalProbe {
    static final class Entry {
        final String name;
        final String value;
        Entry(String name, String value) {
            this.name = name;
            this.value = value;
        }
    }

    static final class Snapshot {
        final List<Entry> temperatures = new ArrayList<>();
        final List<Entry> fans = new ArrayList<>();
        final List<Entry> coolingStates = new ArrayList<>();
        int hiddenOrInvalid = 0;
    }

    private ThermalProbe() {}

    static Snapshot collect() {
        Snapshot s = new Snapshot();
        for (File d : directories("/sys/class/thermal", "thermal_zone")) {
            String type = readLine(new File(d, "type"));
            String temp = readLine(new File(d, "temp"));
            if (temp == null) {
                s.hiddenOrInvalid++;
                continue;
            }
            String celsius = asCelsius(temp);
            if (celsius == null) {
                s.hiddenOrInvalid++;
                continue;
            }
            s.temperatures.add(new Entry(
                    safeLabel(type, "Без названия") + " (" + d.getName() + ")", celsius));
        }

        for (File d : directories("/sys/class/hwmon", "hwmon")) {
            String hwName = safeLabel(readLine(new File(d, "name")), d.getName());
            File[] files;
            try {
                files = d.listFiles();
            } catch (SecurityException ex) {
                files = null;
            }
            if (files == null) {
                continue;
            }
            for (File f : files) {
                String n = f.getName();
                if (n.matches("temp[0-9]+_input")) {
                    String val = readLine(f);
                    String celsius = val == null ? null : asCelsius(val);
                    if (celsius != null) {
                        s.temperatures.add(new Entry(
                                hwName + " / " + n, celsius));
                    }
                } else if (n.matches("fan[0-9]+_input")) {
                    String val = readLine(f);
                    Integer rpm = positiveInt(val, 200000);
                    if (rpm != null) {
                        s.fans.add(new Entry(
                                hwName + " / " + n.replace("_input", ""), rpm + " об/мин"));
                    }
                }
            }
        }

        for (File d : directories("/sys/class/thermal", "cooling_device")) {
            Integer cur = positiveInt(readLine(new File(d, "cur_state")), 100000);
            Integer max = positiveInt(readLine(new File(d, "max_state")), 100000);
            if (cur == null || max == null || cur > max) {
                continue;
            }
            String type = safeLabel(readLine(new File(d, "type")), d.getName());
            s.coolingStates.add(new Entry(
                    type + " (" + d.getName() + ")", cur + " / " + max + " (не RPM)"));
        }

        sort(s.temperatures);
        sort(s.fans);
        sort(s.coolingStates);
        return s;
    }

    private static List<File> directories(String parent, String prefix) {
        File[] found;
        try {
            found = new File(parent).listFiles();
        } catch (SecurityException ex) {
            found = null;
        }
        if (found == null) {
            return Collections.emptyList();
        }
        List<File> result = new ArrayList<>();
        for (File item : found) {
            try {
                if (item.isDirectory() && item.getName().startsWith(prefix)) {
                    result.add(item);
                }
            } catch (SecurityException ignored) {
                // Non-privileged app may not access a particular OEM node.
            }
        }
        Collections.sort(result, Comparator.comparing(File::getName));
        return result;
    }

    private static void sort(List<Entry> entries) {
        Collections.sort(entries, Comparator.comparing(a -> a.name));
    }

    private static String safeLabel(String s, String fallback) {
        if (s == null || s.isEmpty()) {
            return fallback;
        }
        String clean = s.replaceAll("[\\p{Cntrl}]", "").trim();
        return clean.length() > 80 ? clean.substring(0, 80) : clean;
    }

    private static String readLine(File file) {
        if (!file.isFile() || !file.canRead()) {
            return null;
        }
        try (BufferedReader r = new BufferedReader(new FileReader(file))) {
            String s = r.readLine();
            if (s == null || s.length() > 120) {
                return null;
            }
            return s.trim();
        } catch (IOException | SecurityException ex) {
            return null;
        }
    }

    private static Integer positiveInt(String v, int max) {
        if (v == null || !v.matches("[0-9]{1,9}")) {
            return null;
        }
        try {
            int i = Integer.parseInt(v);
            return i <= max ? i : null;
        } catch (NumberFormatException ex) {
            return null;
        }
    }

    private static String asCelsius(String raw) {
        if (raw == null || !raw.matches("-?[0-9]{1,9}")) {
            return null;
        }
        try {
            double value = Double.parseDouble(raw);
            // Linux thermal zones and hwmon commonly use millidegrees C.
            // Some OEM endpoints use degrees C; only scale when clearly necessary.
            if (Math.abs(value) > 200.0) {
                value /= 1000.0;
            }
            if (value < -40.0 || value > 150.0) {
                return null;
            }
            return String.format(Locale.getDefault(), "%.1f °C", value);
        } catch (NumberFormatException ex) {
            return null;
        }
    }
}
