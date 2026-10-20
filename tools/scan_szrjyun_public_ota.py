#!/usr/bin/env python3
"""Enumerate public szrjyun MT9660 OTA JSON indexes (read-only, bounded)."""
import argparse, csv, json, random, time, urllib.request, urllib.error
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--start", type=int, required=True)
ap.add_argument("--end", type=int, required=True)
ap.add_argument("--out", type=Path, required=True)
args = ap.parse_args()
assert 1 <= args.start <= args.end <= 10000
args.out.mkdir(parents=True, exist_ok=True)
agent = {"User-Agent": "CineLux-OTA-research/1.0 (public metadata audit; rate-limited)"}
hits = []
counts = {}
processed = 0
blocked = 0
failed = 0
stop_reason = None
with (args.out / "statuses.csv").open("w", newline="", encoding="utf-8") as fp:
    writer = csv.writer(fp)
    writer.writerow(("id", "http_status", "error"))
    for code in range(args.start, args.end + 1):
        address = f"https://www.szrjyun.com/ota/android/mt9660/{code}/{code}_ota.json"
        status = 0
        err = ""
        try:
            request = urllib.request.Request(address, headers=agent)
            with urllib.request.urlopen(request, timeout=9) as response:
                status = response.status
                payload = response.read(131073)
                if len(payload) > 131072:
                    err = "large_response"
                else:
                    try:
                        data = json.loads(payload)
                        hits.append({"id": code, "url": address, "http_status": status, "metadata": data})
                        print(f"FOUND {code}: {json.dumps(data, ensure_ascii=False)[:500]}", flush=True)
                    except (UnicodeDecodeError, ValueError) as ex:
                        err = f"not_json:{type(ex).__name__}"
        except urllib.error.HTTPError as ex:
            status = ex.code
            err = f"http_{status}"
        except Exception as ex:
            err = f"{type(ex).__name__}:{str(ex)[:100]}"
        writer.writerow((code, status or "", err))
        fp.flush()
        processed += 1
        counts[str(status or "error")] = counts.get(str(status or "error"), 0) + 1
        if status in (403, 429):
            blocked += 1
        else:
            blocked = 0
        if status == 0 or status >= 500:
            failed += 1
        else:
            failed = 0
        if processed % 100 == 0:
            print(f"PROGRESS {code}/{args.end}; processed={processed}; found={len(hits)}; stats={counts}", flush=True)
        if blocked >= 3:
            stop_reason = f"access_denied_or_rate_limited_{status}"
        if failed >= 12:
            stop_reason = f"consecutive_server_or_network_errors_{failed}"
        if stop_reason:
            print(f"STOP {stop_reason} at {code}", flush=True)
            break
        time.sleep(1.25 + random.uniform(0.0, 0.35))
summary = {
    "start": args.start, "end": args.end, "checked": processed,
    "complete": processed == args.end - args.start + 1,
    "http_counts": counts, "found_ids": [r["id"] for r in hits],
    "stop_reason": stop_reason
}
(args.out / "hits.json").write_text(json.dumps(hits, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
(args.out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("RESULT", json.dumps(summary, ensure_ascii=False), flush=True)
if stop_reason:
    raise SystemExit(2)
