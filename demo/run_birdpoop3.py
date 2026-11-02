#!/usr/bin/env python3
"""Bird-poop test, round 3 (Nov 2): NATIVE frames from the actual video
segment (…109 low close pass, frame ~4.25s) — no screenshot chain. The
valley-line mark Brett photographed is present at native res. Spark gets
the full frame and the native crop COLD with the same blind prompt
(imported unchanged from run_birdpoop.py) and must name the mark itself.
"""
import base64
import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response
from run_birdpoop import PROMPT

HOST = "api.meta.ai"
URL = f"https://{HOST}/v1/chat/completions"
MODEL = "muse-spark-1.3"
MAX_TOKENS = 12000

BASE = Path(__file__).parent / "demo-flight-nov2"
ITEMS = [
    ("birdpoop-native-full", BASE / "birdpoop-native-full.jpg"),
    ("birdpoop-native-crop", BASE / "birdpoop-native-crop.jpg"),
]


def run_one(slug, img_path, out_dir):
    b64 = base64.b64encode(img_path.read_bytes()).decode()
    body = json.dumps({
        "model": MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            ],
        }],
        "max_tokens": MAX_TOKENS,
    }).encode("utf-8")
    req = urllib.request.Request(URL, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    add_surrogate_to_request(req, "custom.meta-model-api", allowed_hosts=[HOST])
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = read_json_response(resp)
    (out_dir / f"{slug}-raw.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    choice = (data.get("choices") or [{}])[0]
    content = (choice.get("message") or {}).get("content") or ""
    (out_dir / f"{slug}.answer.md").write_text(content, encoding="utf-8")
    print(f"[{slug}] finish={choice.get('finish_reason')} usage={data.get('usage')}")
    print(content)
    print("=" * 70)
    return content


def main():
    out_dir = BASE
    out_dir.mkdir(exist_ok=True)
    for slug, path in ITEMS:
        try:
            run_one(slug, path, out_dir)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:800]
            print(f"[{slug}] HTTP {e.code}: {detail}")


if __name__ == "__main__":
    main()
