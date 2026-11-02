# Chief — architecture (high level)

One assistant, several faces, one memory — and every action it takes passes
through a policy the owner set.

```
        ┌──────────────────── FACES ────────────────────┐
        │  Glasses (Wearables DAT) · iOS app · Deck node │
        └──────────────────────┬─────────────────────────┘
                               │ voice / photos / notes
        ┌──────────────────────▼─────────────────────────┐
        │        PERMISSION-TIER LAYER (the owner)       │
        │   Open — do it · Ask — hold for my decision    │
        │   Never — refuse · full audit trail            │
        └──────────────────────┬─────────────────────────┘
                               │
        ┌──────────────────────▼─────────────────────────┐
        │                    ROUTER                      │
        │     routes each job to the lane that fits      │
        └───────┬───────────────┬───────────────┬────────┘
                │               │               │
        ┌───────▼──────┐ ┌──────▼───────┐ ┌─────▼──────────────┐
        │ LOCAL BRAIN  │ │ MUSE SPARK   │ │ VISION TOOLS       │
        │ Qwen3.6-35B  │ │ reasoning +  │ │ Muse Image (photo  │
        │ on RTX 5080  │ │ job-photo    │ │ understanding),    │
        │ private,     │ │ understanding│ │ SAM 3.1 (chalk-    │
        │ offline-able │ │              │ │ count auditor)     │
        └──────────────┘ └──────────────┘ └─────┬──────────────┘
                                              │
                                ┌─────────────▼──────────────┐
                                │ ESTIMATOR SLICE            │
                                │ census → itemized scope →  │
                                │ verification of the        │
                                │ finished roof vs the paper │
                                └────────────────────────────┘
```

## The pieces

**Faces.** Chief is one assistant with one memory, worn three ways: Oakley
Meta Vanguard glasses (Meta Wearables DAT SDK — voice and camera, hands-free
on a roof), an iOS phone app, and a Steam Deck node with wake word and local
voice. A conversation started on one face continues on another. Devices pair
with revocable per-device tokens; no keys are baked into any app.

**The permission-tier layer.** The owner sets a single policy — per action
and per class of data — in three tiers:

- **Open** — Chief may do it without asking.
- **Ask** — Chief prepares the work, then holds it for the owner's decision.
  A held action interrupts mid-execution: Chief pauses, presents the
  decision, and resumes when the owner answers.
- **Never** — Chief does not do it, at all.

The policy is enforced at the intermediary layer, so it holds the same way no
matter which model, device, or service sits behind it — swapping a brain
never swaps the rules. Every action taken, held, or refused is written to an
audit trail.

**The router.** Jobs are routed by fit: the local model for instant, private,
everyday turns; a fast frontier lane when a job needs reach; Muse Spark when
it needs deep reasoning. The switch is per-conversation and per-job, not a
rebuild — and routing never bypasses the tier layer.

**The local brain.** Qwen3.6-35B (open weights) runs on the owner's own
workstation (RTX 5080, via Ollama) and handles routine turns entirely
on-premises — fast, free per call, and offline-capable. Private everyday work
never has to leave the house to be answered.

**Vision tools.** Job photos are read by Muse Spark and Muse Image: typed
penetration censuses, hail chalk counts, condition notes — always under the
seen-only rule (only what is actually visible is counted; ambiguity is
flagged, never guessed). SAM 3.1 works as an auditor over the human's own
marks: it boxes and counts chalked hail hits. It does not diagnose damage.

**The estimator slice.** A drone flies the roof; the vision census turns what
is on the roof into an itemized scope; pricing comes from the owner's own
numbers, never from the model. After the work is done, the same census flies
again and checks the finished roof against the written scope — estimate at
the front, verification at the back.
