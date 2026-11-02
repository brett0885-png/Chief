#!/usr/bin/env python3
"""Ground test set 2 (Nov 2): 6 more photos from Brett on the roof —
slopes and ridges, unlabeled. Identical blind prompt as run_groundtest.py
(imported unchanged): deposits on any surface + dents in any metal vent.
Brett holds ground truth and reveals it after the run.
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
from run_groundtest import PROMPT

HOST = "api.meta.ai"
URL = f"https://{HOST}/v1/chat/completions"
MODEL = "muse-spark-1.3"
MAX_TOKENS = 12000

FILES = Path.home() / "workspace" / "user" / "files"
ITEMS = [
    ("h1-slope-wide", FILES / "BA7F8C1D-0134-4F4E-B04E-8A2EAE97E44F-photo-EC9AAEB9-CCC2-4E69-9903-44B9B8F16BE6.jpg"),
    ("h2-ridge-a", FILES / "E27CA8CE-5846-457C-AEEF-15E4D5BC34F6-photo-360A2291-2BDD-4006-96FF-5858968455A8.jpg"),
    ("h3-ridge-b", FILES / "33A68773-685D-4DEB-8C8B-52B3CC9395DB-photo-64A4AC3E-0142-44E4-A205-A6FCCD4AFE40.jpg"),
    ("h4-ridge-dome-far", FILES / "4CDA46AF-AF3C-4AC9-A986-435C2863B59D-photo-85EAB59F-9868-4795-A923-A7D44275DC2E.jpg"),
    ("h5-field-down", FILES / "E0135E82-86A2-4B9E-A412-8232FC377477-photo-379687A3-36B0-4B30-BA92-C824F9226BE2.jpg"),
    ("h6-ridge-run", FILES / "464FC169-3CB3-4079-9889-76F31103D00A-photo-EE05D70F-3108-417C-A486-0CE26E6DB7E8.jpg"),
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
    (out_dir / f"ground-{slug}-raw.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    choice = (data.get("choices") or [{}])[0]
    content = (choice.get("message") or {}).get("content") or ""
    (out_dir / f"ground-{slug}.answer.md").write_text(content, encoding="utf-8")
    print(f"[{slug}] finish={choice.get('finish_reason')} usage={data.get('usage')}")
    print(content)
    print("=" * 70)
    return content


def main():
    out_dir = Path(__file__).parent / "demo-flight-nov2"
    out_dir.mkdir(exist_ok=True)
    for slug, path in ITEMS:
        try:
            run_one(slug, path, out_dir)
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:800]
            print(f"[{slug}] HTTP {e.code}: {detail}")


if __name__ == "__main__":
    main()
