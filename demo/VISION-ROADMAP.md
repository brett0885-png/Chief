# MOC vision roadmap (Brett, 2026-10-31)

## Standing rule
Never manufacture damage. Only damage/items actually SEEN are counted.
Recognition, not forensics: zebra vs horse — some horses have spots, and you go
by what you can see. (Baked into run_pipes.py, run_hail.py, run_flat.py prompts.)

## Tier 1 — Recognition (NOW; ships in the estimator demo)
- Input: normal slope / drone / roof-level photos.
- Jobs: typed penetration census (pipe jacks, dryer vents, turbines, flues,
  static vents), hail chalk-mark counts from close-ups, ridge/field damage ID,
  commercial census (HVAC, stacks, hatches, drains) from roof-level photos.
- Proven so far: counts right on every close/standard photo; vents typed to
  Brett's taxonomy (dryer-vent correction taught and held); trap photos (clean
  roofs) came back clean — nothing invented.
- Known limits: high-altitude aerial counts are estimation, NOT usable numbers;
  faint chalk at distance undercounts BY DESIGN under the rule.

## Tier 2 — Forensics (LATER, post-hackathon; Brett: "we could do forensics too")
**Doctrine (Brett, 2026-10-31):** the same sleuthing used to determine whether a
crime victim is a victim of a crime, applied to a roof: determine whether the
roof IS a victim, and of what. The "determination" in the
size/scope/determination trio is that verdict, reached from evidence:
pattern, trail, size, and scope must be consistent with the claimed cause.
**Cause set (Brett's correction, 2026-10-31):** "person" is WRITTEN OUT as a
category — people do not purposely damage roofs (nobody is up there with a
hammer; a rubric exists for that rare edge case only). Shingles are simply
susceptible material, and determination assigns CAUSE, never blame:
- **Storm (hail/wind)** — most of the time, it is hail.
- **Foot traffic** — the tool's main incidental-human read: traffic patterns
  and trails from people walking the roof.
- **Deterioration** — sometimes it is just deteriorating; that is the call.
- Other natural/material causes (blister, defect, wear, animal) as they come.
The tool's real work: separate foot traffic and deterioration from actual
storm damage, and say where the storm damage actually came from.
Design (Brett, 2026-10-31): two layers.
- **Pattern layer (the WHOLE PIECE, assembled):** the grid frames are stitched
  into one composite of the entire slope and the pattern read runs on the
  assembled whole — never frame-by-frame (Brett, 2026-10-31: "Look at the whole
  piece together because you have to see the trails"). Detect the spatial
  arrangement of damage. Random scatter = consistent with hail. A LINEAR TRAIL
  of hits = a different cause (something dragged, dropped, or tracked along a
  line) — the trail is the named first pattern; it only exists at whole-slope
  scale, so per-photo analysis cannot see it by definition.
- **Close-up layer:** everything else is size, scope, and determination from
  close-ups — hit size (diameter), scope (density/extent, e.g. hits per test
  square), and the determination call (hail fracture vs blister vs mechanical
  vs wear) made on close-up evidence only.
- Requires: (1) close-up photos, (2) deeper training.
- **Acquisition spec (Brett, 2026-10-31):** a picture every 1–2 square feet as
  it passes over the slope — a dense grid of close-ups that builds a really
  deep file per slope. Each frame does double duty: a close-up for the
  size/scope/determination layer AND a position tile for the pattern layer
  (a trail only becomes visible when the frames connect across the slope).
  Scale feel: a 10x10 test square at that density = ~50–100 frames; whole
  slopes = a disciplined low drone pass or walked grid.
- Ground truth needed from Brett (same pattern as the Oct 31 session):
  close-up sets labeled by class — true hail fracture, blister, scuff/mechanical,
  wear/aging, manufacturing defect — plus any trail/linear-pattern examples.
  Start collecting whenever Brett sends them; file under
  spark-roofing/forensics/ with his labels verbatim.
- Until trained and verified on his labels, the system does NOT make forensic
  calls — Tier 1 rule governs.
- Seed note: the Oct 31 hail batch already seeds both layers (close-ups for
  size/determination; the LS 4-12 test-square shot for scope). No linear trail
  appeared in that batch — all scatter.
