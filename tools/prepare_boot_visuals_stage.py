#!/usr/bin/env python3
"""Prepare an AUDITABLE, NON-FLASHABLE visual/audio delta for CineLux 8052/8054.

This tool NEVER opens a partition for writing and NEVER creates system.img,
super.img, payload.bin, update.pkg or a bootloader image. Input directories are
read-only extracted STOCK ext4 filesystem trees. The output is merely a staged
file overlay with a manifest. Do NOT flash the output.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

from PIL import Image, ImageDraw, ImageFont

PROFILE = {
    "8052": {
        "baseline": "RUIOS.8052.1.0.4 October OTA (one HDMI)",
        "stock_1080": "453a75b9a6d37227910065a2aefb13600fcda5a855cd95e2ef92d76308d75485",
        "stock_4k": "9d161b79603b1d2ddb0c23b0fe120a013775a7995f93296014fb24fe10ff1b9c",
        "audio_sha": "0f41508a306beb457e4cf9ddd265b11d95879e5c7e82b52e07e6fed832014bf7",
    },
    "8054": {
        "baseline": "RUIOS.8054.1.0.1 September factory (two HDMI; NOT 1.0.4)",
        "stock_1080": "c61563b2580ab2a4a74cc3a958aa0c9f0b789cc19c96ecc5cddac4df7d5d56db",
        "stock_4k": "9d161b79603b1d2ddb0c23b0fe120a013775a7995f93296014fb24fe10ff1b9c",
        "audio_sha": None,  # 8054 MP3 only inventoried by size; do not invent a hash.
    },
}


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1048576), b""):
            h.update(block)
    return h.hexdigest()


def check_img(path, expected_sha, dimensions):
    assert path.is_file(), "Missing stock file: " + str(path)
    assert sha256(path) == expected_sha, "Baseline JPEG hash mismatch: " + str(path)
    with Image.open(path) as im:
        assert im.format == "JPEG" and im.size == dimensions, "Wrong stock JPEG: " + str(path)


def font_for(height):
    size = round(height * 0.115)
    for name in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                 "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"):
        if Path(name).is_file():
            return ImageFont.truetype(name, size)
    raise RuntimeError("Install fonts-dejavu-core; do not use an unverified fallback font")


def generate_boot_logo(out, width, height):
    # Reproducible project logo: neutral Android TV-inspired styling, not an OEM logo.
    im = Image.new("RGB", (width, height), (0, 0, 0))
    d = ImageDraw.Draw(im)
    font = font_for(height)
    title = "android tv"
    bounds = d.textbbox((0, 0), title, font=font)
    x = (width - (bounds[2] - bounds[0])) // 2 - bounds[0]
    y = int(height * 0.50) - (bounds[3] - bounds[1]) // 2 - bounds[1]
    d.text((x, y), title, font=font, fill=(240, 242, 244))
    dot = max(5, int(height * 0.015))
    gap = int(height * 0.027)
    colors = [(66, 133, 244), (234, 67, 53), (251, 188, 5), (52, 168, 83)]
    left = (width - (4 * dot * 2 + 3 * gap)) // 2
    dot_y = int(height * 0.37)
    for i, color in enumerate(colors):
        a = left + i * (2 * dot + gap)
        d.ellipse((a, dot_y, a + 2 * dot, dot_y + 2 * dot), fill=color)
    out.parent.mkdir(parents=True, exist_ok=True)
    im.save(out, format="JPEG", quality=94, subsampling=0, optimize=True)
    check_result = Image.open(out)
    assert check_result.format == "JPEG" and check_result.size == (width, height)


def probe_mp3(path):
    data = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries",
        "stream=codec_name,sample_rate,channels,bit_rate:format=duration",
        "-of", "json", str(path)], text=True)
    meta = json.loads(data)
    streams = [s for s in meta.get("streams", []) if s.get("codec_name") == "mp3"]
    assert len(streams) >= 1, "Original boot0.mp3 is not MP3: " + str(path)
    s = streams[0]
    return {"sample_rate": int(s["sample_rate"]),
            "channels": int(s["channels"]),
            "bitrate": int(s.get("bit_rate", 32000) or 32000),
            "duration": float(meta["format"]["duration"])}


def silent_mp3(stock_audio, out):
    params = probe_mp3(stock_audio)
    assert 1 <= params["channels"] <= 2 and 10 <= params["duration"] <= 20
    rate = params["sample_rate"]
    kbps = max(32, min(192, round(params["bitrate"] / 1000)))
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "lavfi", "-i", f"anullsrc=r={rate}:cl={'mono' if params['channels']==1 else 'stereo'}",
        "-t", str(params["duration"]), "-c:a", "libmp3lame",
        "-b:a", f"{kbps}k", "-write_xing", "0", str(out)],
        check=True, timeout=50)
    check = probe_mp3(out)
    assert check["sample_rate"] == rate and check["channels"] == params["channels"]
    assert abs(check["duration"] - params["duration"]) < 0.25
    return params


def repackage_animation(stock_zip, out, upscale=False):
    """Strip embedded audio; preserve PNG/JPG image sequence and use STORED ZIP entries."""
    assert zipfile.is_zipfile(stock_zip), "Not a bootanimation ZIP"
    with zipfile.ZipFile(stock_zip, "r") as source:
        bad = source.testzip()
        assert bad is None, "Corrupt input ZIP: " + str(bad)
        members = source.namelist()
        assert "desc.txt" in members, "Missing desc.txt"
        text = source.read("desc.txt").decode("utf-8-sig")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        header = lines[0].split()
        assert len(header) >= 3, "Bad bootanimation header"
        width, height, fps = map(int, header[:3])
        assert 1 <= width <= 3840 and 1 <= height <= 2160 and 1 <= fps <= 60
        if upscale:
            assert width * 9 == height * 16, "4K upscaling allowed only for 16:9 inputs"
            assert (width, height) != (3840, 2160), "Animation already 4K; no upscaling needed"
            target_size = (3840, 2160)
        else:
            target_size = (width, height)
        part_lines = [line for line in lines[1:] if line.split()[0] in ("p", "c", "f")]
        assert part_lines, "No animation parts"
        part_names = {parts[3] for line in part_lines for parts in [line.split()]
                      if len(parts) >= 4}
        assert len(part_names) > 0
        image_names = [n for n in members if any(
            n.startswith(part + "/") and n.lower().endswith((".png", ".jpg", ".jpeg"))
            for part in part_names)]
        assert image_names, "No matching image frames"
        # Optional trim.txt is needed for correctly displaying cropped frames.
        aux_names = [n for n in members if any(
            n == part + "/trim.txt" for part in part_names)]
        assert not (upscale and aux_names), "4K upscale of trimmed frames needs trim-coordinate migration"
        skipped = []
        out.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as dest:
            lead = " ".join([str(target_size[0]), str(target_size[1]), str(fps)] + header[3:])
            dest.writestr("desc.txt", (lead + "\n" + "\n".join(part_lines) + "\n").encode())
            for name in members:
                if name == "desc.txt" or name.endswith("/"):
                    continue
                if name not in image_names and name not in aux_names:
                    skipped.append(name)
                    continue  # Never copy audio.wav, audio.mp3, or unrecognized vendor extras.
                payload = source.read(name)
                if name in image_names:
                    with Image.open(io.BytesIO(payload)) as im:
                        assert im.size == (width, height), "Unexpected frame dimensions: " + name
                        if upscale:
                            im = im.resize(target_size, Image.Resampling.LANCZOS)
                            b = io.BytesIO()
                            if name.lower().endswith(".png"):
                                im.save(b, format="PNG", optimize=True)
                            else:
                                im.convert("RGB").save(b, format="JPEG", quality=93)
                            payload = b.getvalue()
                dest.writestr(name, payload)
    assert zipfile.ZipFile(out).testzip() is None
    return {"original_header": [width, height, fps],
            "final_resolution": list(target_size),
            "frame_count": len(image_names),
            "upscaled_not_native_4k": upscale,
            "excluded_nonframe_members": skipped,
            "upstream_zip_sha256": sha256(stock_zip)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--variant", choices=PROFILE, required=True)
    p.add_argument("--bootdata-root", type=Path, required=True,
                   help="Read-only extracted bootdata[_a] ext4 contents")
    p.add_argument("--tvconfig-root", type=Path, required=True,
                   help="Read-only extracted tvconfig[_a] ext4 contents")
    p.add_argument("--animation-zip", type=Path, required=True,
                   help="Upstream atv11 bootanimation.zip, Working and Tested variant")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--upscale-4k", action="store_true",
                   help="Explicit high-RAM experimental upscale, NOT a genuine 4K source")
    a = p.parse_args()
    cfg = PROFILE[a.variant]
    b, t = a.bootdata_root.resolve(), a.tvconfig_root.resolve()
    stock = {
        "bootdata/boot0.jpg": b / "boot0.jpg",
        "tvconfig/bsp/common/misc/boot0.jpg": t / "bsp/common/misc/boot0.jpg",
        "tvconfig/bsp/common/misc/boot0_4K.jpg": t / "bsp/common/misc/boot0_4K.jpg",
        "bootdata/boot0.mp3": b / "boot0.mp3",
        "tvconfig/bsp/common/misc/boot0.mp3": t / "bsp/common/misc/boot0.mp3",
    }
    for key in ("bootdata/boot0.jpg", "tvconfig/bsp/common/misc/boot0.jpg"):
        check_img(stock[key], cfg["stock_1080"], (1920, 1080))
    check_img(stock["tvconfig/bsp/common/misc/boot0_4K.jpg"], cfg["stock_4k"], (3840, 2160))
    audios = [stock["bootdata/boot0.mp3"], stock["tvconfig/bsp/common/misc/boot0.mp3"]]
    assert all(f.is_file() and f.stat().st_size == 59952 for f in audios), "Unknown boot audio baseline"
    assert sha256(audios[0]) == sha256(audios[1]), "Stock MP3 copies differ; audit before changing"
    if cfg["audio_sha"]:
        assert sha256(audios[0]) == cfg["audio_sha"], "Stock MP3 SHA mismatch"
    assert a.animation_zip.is_file() and a.animation_zip.stat().st_size > 0
    # Exact "Working and Tested" ZIP from khurramrizvi/atv11_bootanimation (Git blob SHA-1).
    # Do not silently substitute the different top-level bootanimation.zip.
    with a.animation_zip.open("rb") as upstream:
        payload = upstream.read()
    git_sha = hashlib.sha1(b"blob " + str(len(payload)).encode() + b"\0" + payload).hexdigest()
    assert git_sha == "3b1f39b90f7ffe28d5c4a7219190d411d3913fc5", \
        "Unexpected upstream animation source (Git blob SHA mismatch)"
    out = a.out.resolve()
    assert not (out == b or out == t or b in out.parents or t in out.parents), \
        "Refusing to write inside stock partitions"
    assert not out.exists() or not any(out.iterdir()), "Output dir must be new/empty"
    out.mkdir(parents=True, exist_ok=True)
    overlay = out / "overlay"
    generate_boot_logo(overlay / "bootdata/boot0.jpg", 1920, 1080)
    generate_boot_logo(overlay / "tvconfig/bsp/common/misc/boot0.jpg", 1920, 1080)
    generate_boot_logo(overlay / "tvconfig/bsp/common/misc/boot0_4K.jpg", 3840, 2160)
    props = silent_mp3(audios[0], overlay / "bootdata/boot0.mp3")
    audio_copy = overlay / "tvconfig/bsp/common/misc/boot0.mp3"
    audio_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(overlay / "bootdata/boot0.mp3", audio_copy)
    anim = repackage_animation(a.animation_zip, overlay / "system/media/bootanimation.zip",
                               upscale=a.upscale_4k)
    files = {str(f.relative_to(overlay)): {"sha256": sha256(f), "bytes": f.stat().st_size}
             for f in overlay.rglob("*") if f.is_file()}
    manifest = {
        "format": "CineLux boot visuals delta; NON-FLASHABLE",
        "profile": a.variant, "stock_baseline": cfg["baseline"],
        "source_stock_sha256": {k: sha256(v) for k, v in stock.items()},
        "overlay_files": files, "stock_mp3_properties": props,
        "animation": anim,
        "never_modify": ["boot", "bootloader", "kernel", "vendor", "tvservice", "dtbo",
                         "vbmeta", "PMU", "persist", "factory", "device calibration"],
        "verification_gates": [
            "Determine actual splash paths and whether bootdata/tvconfig copies are active.",
            "Confirm bootanimation priority (system/product/APEX/vendor bootvideo) on each board.",
            "Observe boot0.mp3 playback, and check any other startup-sound source via ADB.",
            "Verify AVB/rollback/SELinux/FS owner and modes and test a reversible replacement.",
            "Never flash or rename this directory to update.zip.",
        ],
        "status": "SOURCE-STAGED-ONLY; NO PARTITION IMAGE; NO INSTALLABLE PKG/BIN/OTA",
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": manifest["status"], "variant": a.variant,
                      "files": files, "animation": anim}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
