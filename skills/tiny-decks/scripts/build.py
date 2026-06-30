#!/usr/bin/env python3
"""
build.py — turn a deck spec (JSON) into an editable Tiny-branded .pptx.

Usage:
    python build.py <spec.json> <out.pptx>

A spec is:
    { "title": "...", "slides": [ {"layout": "...", ...}, ... ] }

Each slide dict is dispatched to a layout builder in slides.py. See
references/deck-spec.md for the full slide vocabulary.

For the data-driven board pack, generate the spec first with board_model.py
(it runs compute() over the monthly data model), then feed it here.
"""
import json
import sys
from pptx import Presentation

import theme as T
from slides import LAYOUTS, add_watermark


def build(spec, out_path):
    prs = Presentation()
    prs.slide_width = T.SLIDE_W
    prs.slide_height = T.SLIDE_H
    # Confidential watermark defaults ON for finance decks; set "watermark": false
    # in the spec to disable. Text from "watermarkText" or "CONFIDENTIAL".
    wm = spec.get("watermark", True)
    wm_text = spec.get("watermarkText", "CONFIDENTIAL")
    for i, s in enumerate(spec.get("slides", [])):
        layout = s.get("layout", "content")
        fn = LAYOUTS.get(layout)
        if fn is None:
            print(f"  [skip] slide {i}: unknown layout '{layout}'", file=sys.stderr)
            continue
        try:
            slide = fn(prs, s)
            if wm:
                add_watermark(slide, layout, wm_text)
        except Exception as e:
            print(f"  [error] slide {i} ({layout}): {e}", file=sys.stderr)
            raise
    prs.save(out_path)
    return len(spec.get("slides", []))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    spec = json.load(open(sys.argv[1]))
    n = build(spec, sys.argv[2])
    print(f"✓ {n} slides -> {sys.argv[2]}")


if __name__ == "__main__":
    main()
