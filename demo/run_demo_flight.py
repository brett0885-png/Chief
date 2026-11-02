#!/usr/bin/env python3
"""Demo-flight census (Nov 2): run the run_pipes.py penetration prompt over
8 DJI drone photos of a completed MOC Roofing job in Texas. Reuses PROMPT + auth from run_pipes.py;
writes per-photo outputs under demo-flight-nov2/ (does not overwrite prior runs).
"""
import base64
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request, read_json_response
from run_pipes import PROMPT

HOST = "api.meta.ai"
URL = f"https://{HOST}/v1/chat/completions"
MODEL = "muse-spark-1.3"
MAX_TOKENS = 12000

FILES = Path.home() / "workspace" / "user" / "files"
PHOTOS = [
    ("photo1-wide-a", "CE3D383C-457E-4175-BDD8-CC047355DF7C-photo-71CF6E9C-293E-4869-9FC8-85D7405CE86E.jpg"),
    ("photo2-wide-b", "3E880DB9-19F8-452A-8226-F9F707B5C3D8-photo-FD91551A-C9BA-4AFF-8BC6-4FED3E8C71BF.jpg"),
    ("photo3-wide-c", "1972E097-AF59-4F44-B378-F61BEA9568D8-photo-037CC616-55C1-427A-A9EB-09524BEAB847.jpg"),
    ("photo4-slope-closeup", "BBF08EBE-DC4A-4C23-AA5E-0F5BFB29AF41-photo-6E42CB26-B87D-43DB-AF6B-37C36799A068.jpg"),
    ("photo5-oblique-a", "8180532D-BA0A-4C76-9805-94A647668B44-photo-BCD311A8-EA4E-441D-ABB7-3125EE3F39DC.jpg"),
    ("photo6-north-topdown", "CD521C15-8E6F-4DFF-BF21-C8632D6BD7FE-photo-89E1448D-D3B2-46CB-98C4-AF767BBADA29.jpg"),
    ("photo7-close-topdown", "A6F78E92-C1B5-40B5-8BE4-06EF11848938-photo-0F2E035E-A6C8-46A6-9BA8-D1DD433E868E.jpg"),
    ("photo8-oblique-b", "F3BAE201-1D54-4ED0-9307-4E6C9C5F9C2A-photo-FC32AEFA-0E91-4411-B79E-D065AACC6C22.jpg"),
]


def run_one(slug, filename, out_dir):
    img_path = FILES / filename
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
    out_dir = Path(__file__).parent / "demo-flight-nov2"
    out_dir.mkdir(exist_ok=True)
    only = sys.argv[1:] or None
    for slug, filename in PHOTOS:
        if only and slug not in only:
            continue
        try:
            run_one(slug, filename, out_dir)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:800]
            print(f"[{slug}] HTTP {e.code}: {detail}")


if __name__ == "__main__":
    main()
