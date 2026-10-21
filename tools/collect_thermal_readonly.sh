#!/bin/sh
# READ ONLY: run under adb shell on MT9660. No root/writes/service restarts.
set +e
export LC_ALL=C
echo "=== BUILD / PROFILE ==="
getprop ro.product.model
getprop ro.build.display.id
getprop ro.build.fingerprint
getprop ro.boot.hardware
echo "=== ANDROID THERMAL SERVICE ==="
dumpsys thermalservice 2>&1 | head -c 20000
echo
echo "=== LINUX THERMAL ZONES ==="
for d in /sys/class/thermal/thermal_zone*; do
  [ -d "$d" ] || continue
  echo "### $d"
  for n in type temp policy mode available_policies; do
    [ -r "$d/$n" ] && { printf '%s=' "$n"; cat "$d/$n" 2>&1; }
  done
  for p in "$d"/trip_point_*_temp "$d"/trip_point_*_type "$d"/trip_point_*_hyst; do
    [ -r "$p" ] && { printf '%s=' "$(basename "$p")"; cat "$p" 2>&1; }
  done
done
echo "=== COOLING DEVICES (READ ONLY) ==="
for d in /sys/class/thermal/cooling_device*; do
  [ -d "$d" ] || continue
  echo "### $d"
  for n in type cur_state max_state; do
    [ -r "$d/$n" ] && { printf '%s=' "$n"; cat "$d/$n" 2>&1; }
  done
done
echo "=== HWMON / FAN / PWM (READ ONLY) ==="
for d in /sys/class/hwmon/hwmon*; do
  [ -d "$d" ] || continue
  echo "### $d"
  [ -r "$d/name" ] && { printf 'name='; cat "$d/name"; }
  for p in "$d"/temp*_label "$d"/temp*_input "$d"/fan*_input "$d"/fan*_label "$d"/fan*_target "$d"/pwm[0-9] "$d"/pwm*_enable "$d"/pwm*_auto_point*_temp "$d"/pwm*_auto_point*_pwm; do
    [ -r "$p" ] && { printf '%s=' "$(basename "$p")"; cat "$p" 2>&1; }
  done
done
echo "=== DREAM / IDLE ==="
settings get secure screensaver_enabled 2>&1
settings get secure screensaver_components 2>&1
dumpsys dreams 2>&1 | head -c 12000
echo
echo "=== RELEVANT PACKAGES ==="
pm list packages -f 2>&1 | grep -iE 'dream|retail|airplay|wfd|miracast|trd|factory|temp|thermal|cool|fan' | head -100
echo "=== SERVICE NAMES (FILTERED) ==="
service list 2>&1 | grep -iE 'thermal|trd|temp|fan|sensor|project' | head -100
echo "=== END ==="
