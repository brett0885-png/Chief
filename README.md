# Chief

**A voice-first AI assistant for skilled-trades owners** — glasses and phone, a private local brain, Muse Spark / Muse Image / SAM 3.1 for job-photo understanding, and an estimator that turns what Chief sees on a roof into estimate work, under owner-set permission tiers (Open / Ask / Never).

*Meta Global AI Developer Hackathon (Cerebral Valley) — Indie Dev Track, "Build for Your World." Built by Brett Roberts, owner of MOC Roofing.*

**Demo post on X — Most Viral Project Bonus entry:** https://x.com/betimbrett/status/2118571579227640013

## The problem

Skilled-trades owners don't lose money on craftsmanship — they lose it on follow-up and estimating. And the tool has to work where the work is: on a roof, hands and eyes busy, where a phone screen is useless. Estimates wait until the owner is back at a desk; follow-ups slip; the paper scope and the finished roof never get checked against each other.

## The solution

Chief listens, answers, and does real work by voice alone — captures job notes and photos, drafts customer follow-ups, checks the schedule — under privacy rules the owner sets: what it may do freely (**Open**), what it must ask first (**Ask**), and what it never does (**Never**).

- **On the glasses** — Chief lives on Oakley Meta Vanguard smart glasses, built on the Meta Wearables DAT SDK. Voice in, voice out, camera on the glasses, while the owner is standing on a roof.
- **On the phone** — the same Chief, same memory, as an iOS app. Phone and glasses are two faces of one assistant; a conversation started on one continues on the other. Devices pair with revocable per-device tokens.
- **A private local brain** — routine turns never leave the house. A local open-weights model (Qwen3.6-35B) runs on the owner's workstation (RTX 5080) as the everyday brain: fast, free per call, offline-capable.
- **A router behind the tier layer** — harder jobs route between the local model and frontier models, and every route passes behind the owner-set permission tiers. The lanes switch by job: local for instant private turns, a fast frontier lane for reach, Muse Spark for deep reasoning.
- **The Auto Estimator** — the field workflow the stack exists to run. A drone flies the roof; Chief's vision censuses what is actually on it; the estimate builds from what was seen — and the same census later verifies the finished roof against the written scope.

## How Meta AI tooling is used

- **Muse Spark** (Meta Model API) — Chief's reasoning core, and the vision engine behind the roof-penetration census in [`demo/`](demo/).
- **Muse Image** — job-photo understanding.
- **SAM 3.1** — a count auditor: it boxes and counts the hail hits a human inspector has chalk-marked. SAM doesn't read bruises; it digitizes the roofer's count.
- **Meta Wearables DAT SDK** — the glasses face of Chief, on Oakley Vanguard glasses.

## What the demo shows

Real runs, not mock-ups — the harness and results are in [`demo/`](demo/):

- **Penetration census on the owner's own job photos, scored against his own labels.** Counts right on all five labeled test photos; a plumbing vent typed exactly as a "3-in-1 pipe jack."
- **A teachable moment, kept in:** Spark first called a louvered vent an "exhaust cap." The owner corrected it — that vent is a **dryer vent** — the taxonomy was updated, and the re-run got it exactly right.
- **Hail, under a never-manufacture rule:** only damage that is actually seen is ever counted. On chalk-marked close-ups Spark's counts matched; on wide shots it undercounts by design rather than guessing.
- **Trap photos passed:** clean finished roofs came back clean — nothing invented.
- **Bird droppings vs damage, tested blind:** Spark named bird droppings cold and classified them **not damage**, every time.
- **A whole-roof drone census of a completed job,** checked against the job's written scope: 9 penetrations seen (4 pipe jacks, 3 turbines, 1 skylight, 1 round vent cap). Where census and paper disagreed, the census flagged it instead of matching the paper — and in one case the *paper* was the thing that was wrong.

## Honest limitations

- **SAM 3.1 does not read hail bruises.** It counts chalk marks a human made; determination is the inspector's.
- **Aerial counts at altitude are estimation, not usable numbers.** Counting needs roof-level photos; wide shots undercount faint chalk by design.
- **Pricing is the owner's own numbers — the tool doesn't invent them.** Chief builds the itemized scope from what it sees; dollars come from the owner's pricing.
- **Recognition, not forensics.** Tier 1 reads what is visible. Cause determination (storm vs foot traffic vs deterioration) is a designed Tier 2, not a shipped claim — see `demo/VISION-ROADMAP.md`.

## Tech stack

| Layer | What |
|---|---|
| Faces | Oakley Meta Vanguard glasses (Wearables DAT SDK), iOS app, Steam Deck node |
| Local brain | Qwen3.6-35B, open weights, on an RTX 5080 workstation (Ollama) |
| Reasoning + vision | Muse Spark and Muse Image (Meta Model API) |
| Count auditing | SAM 3.1 |
| Control | Multi-model router behind an owner-set permission-tier layer (Open / Ask / Never) |

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the high-level design and [`demo/`](demo/) for the vision test harness and results.
