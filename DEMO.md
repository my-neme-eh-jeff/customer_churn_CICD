# Autoresearch Demo Script

> Final script for the ~5-minute demo. Local-only doc (gitignored: no — checked in so future-me has it).
> **Target cut:** ~3:30. **Hard cap:** 4:00.
> **Recording tool:** ScreenKite. Cursor positions matter (ScreenKite zooms to the cursor on movement).
> **Camera:** off. Webcam overlay disabled.

The script splits cleanly into **two energies**:
- **0:00 – 1:00 — opener.** Flashy, hook-driven, narrated against the animated explainer (`assets/autoresearch-explainer.html`). Karpathy announcement tweet (cold open) → his loop visualized → outage + the three gaps → the harness reveal. This is where you earn the viewer's attention. Don't move the cursor during this segment — ScreenKite will leave a static cursor alone.
- **1:00 – 3:30 — the walkthrough + close.** Plain, factual, technical. Cursor choreography matters here: every move triggers a ScreenKite zoom. Close on a single trajectory plot, not the MLflow runs list.

---

## 0. Pre-flight (15 min before recording)

1. **Cluster awake.** `make cluster-wake` complete. Verify:
   - `kubectl get pods -A | grep -v "Running\|Completed"` shows nothing pending.
   - `curl http://34.47.242.89/health` returns `{"status":"ok","model_loaded":true,...}`.
   - MLflow `@champion` resolves: open `http://34.180.20.197:5000/#/models/classifier` and confirm the alias is set.

2. **History.tsv reset to header-only.** Confirm with `wc -l auto_experiment/history.tsv` → `1`.

3. **No leftover autoresearch jobs.** `kubectl -n inference get jobs` should be empty or all `Complete`. Delete any stragglers.

4. **Browser tabs in order:**
   - Tab 1: `assets/autoresearch-explainer.html` (open via `open assets/autoresearch-explainer.html` then press `F` for fullscreen)
     - **Network check:** confirm tweets render — embeds depend on `platform.twitter.com/widgets.js`. Offline laptop = blank slides 2A/2B. If they don't load in 5s, retry / check VPN.
     - **Dry-run the spacebar sequence once** (without recording): 9 advances total. Verify the auto-stagnation badge fires on its own while you're still on slide 1 (don't press past stage 4 until it lands).
   - Tab 2: KFP UI → `http://34.93.2.209/#/runs`
   - Tab 3: MLflow → `http://34.180.20.197:5000/#/experiments/3` (the `auto-experiment` experiment)
   - Tab 4: MLflow Models → `http://34.180.20.197:5000/#/models/classifier`
   - Tab 5: GitHub repo PR list → `https://github.com/my-neme-eh-jeff/ML-deployment-system-for-autoresearch/pulls`
   - Tab 6: ArgoCD → `http://34.100.246.237/applications/inference-api` (logged in; password in local `NOTES.md`)
   - Tab 7 (added post-run, before close): `auto_experiment/trajectory.png` rendered fullscreen. See step 8.

5. **Terminal layout — 3 panes pre-loaded:**
   - Pane A: `kubectl get pods -A -w | grep -E --line-buffered "autoresearch|kubeflow|inference-api"` (don't run yet)
   - Pane B: `make autoresearch-run AUTORESEARCH_N=20 AUTORESEARCH_HOURS=8` (don't run yet)
   - Pane C: `make autoresearch-logs` (don't run yet — wait until the Job exists)
   - Font ≥ 18pt, dark theme, history cleared.

6. **Capture the starting state on a sticky note** so you can name the baseline accurately on tape:
   ```bash
   MLFLOW_TRACKING_URI=http://34.180.20.197:5000 uv run python -c "
   import mlflow
   c = mlflow.MlflowClient()
   v = c.get_model_version_by_alias('classifier', 'champion')
   r = c.get_run(v.run_id)
   print(f'@champion: classifier v{v.version}')
   print(f'AUC: {r.data.metrics.get(\"auc_roc\"):.4f}')
   print(f'features: {r.data.params.get(\"n_features\")}')
   "
   ```

7. **DND on.** Dock auto-hide. Menubar hide. Notifications cleared. Quiet room.

8. **Trajectory plot — generate AFTER the autoresearch run finishes, BEFORE recording the close.** `make plot-trajectory` reads `auto_experiment/history.tsv` and writes `auto_experiment/trajectory.png`.
   - Sanity-check the PNG: baseline marker visible on the left, mostly-monotonic climb, final candidate on the right. If the run never promoted (no improvement), the plot is a flat line — re-run with a longer N before the take.
   - To preview the design with synthetic data: `HISTORY_TSV=/tmp/fake_history.tsv OUT_PNG=/tmp/preview.png uv run python scripts/plot_trajectory.py`.

---

## 1. Segment-by-segment script

T+ times are final-cut timestamps.

### Segment 1 — Opener (0:00 → 1:00) · animated explainer

**Visual:** Tab 1, `assets/autoresearch-explainer.html`, fullscreen. Flow: Karpathy announcement tweet → loop animation → outage + problem cards → harness reveal. (Explainer is already reordered — stages 0–8.)

**Cursor:** Park top-right corner before pressing F for fullscreen. Don't move during the explainer — ScreenKite leaves a static cursor alone. Cmd-Tab at 1:00 (keyboard only).

| T+ | Stage | Beats to hit (improvise the line) |
|---|---|---|
| 0:00 | **Stage 0 — announcement tweet** (Andrej Karpathy + 82.8k stars marginalia). Hold ~15s. | • A little while ago Karpathy released autoresearch.  • Like everything he ships, it blew up — lots of stars, lots of forks.  • At its core it's just an infinitely running loop. |
| 0:15 | `Space` → loop slide. Stages 1→2 auto-tick metric (75→96 with one rejection at iter 3). Stop conditions reveal at stage 3. **Stage 4 auto-fires** — three non-improvements, badge flips to "stagnation detected". | • Propose, run, observe, update memory — repeat.  • Some experiments win, some get rejected by the gate.  • Runs unattended until time, threshold, or stagnation calls it.  • [land the "beautiful concept" line as the badge flips] |
| 0:42 | `Space` → outage tweet + 3 miss-cards. | • Beautiful concept — but nothing here is reproducible for you.  • Wrong hardware, single-player, stays local.  • Even Karpathy's setup blacked out when his auth dropped. |
| 0:54 | `Space` → harness reveal (stages 6→8 advance through tool grid + actors line; press through quickly). | • This project's the harness that closes those gaps. Cluster-native, GitOps-controlled, multi-player from day one. |
| 1:00 | Cmd-Tab to terminal (Pane B pre-typed). | • Here's a run. |

**Recording notes:**
- Don't read the beats verbatim — the column is a checklist, not a script. The improvised tone is the whole point of the cold open.
- Stages 1–4 auto-advance internally. **Don't press Space again until stagnation lands** — if you race it you lose the "loop calls itself" beat that mirrors the actual end-of-run.
- Tweet widgets need `widgets.js` from Twitter/X. Pre-flight §0 item 4 verifies. **Don't record offline.**

### Segment 2 — Kick off the run (1:00 → 1:15) · 15s

**Visual:** Terminal with 3 pre-typed panes (A: watch, B: make, C: logs). Cursor parks bottom-right between clicks.

| T+ | Action / cursor | Beats |
|---|---|---|
| 1:00 | Cmd-Tab landed on terminal. Cursor on Pane B prompt. | • Three commands pre-typed: watch, kick off, tail. |
| 1:04 | Click Pane A → Enter (`kubectl get pods -A -w`). Cursor returns. | • Live pod watcher. |
| 1:08 | Click Pane B → Enter (`make autoresearch-run AUTORESEARCH_N=20`). | • Submitted. 20 iters, 8h budget. In-cluster, not my laptop. |
| 1:13 | Pane A: `autoresearch-real-…` Pending → ContainerCreating. Cursor parks. | • Driver pod warming. Dataset is Kaggle IEEE-CIS — 590k transactions, 433 features. |

### Segment 3 — KFP UI (1:15 → 1:45) · 30s

**Visual:** Tab 2, KFP UI. Switch when Pane A shows the first `preprocess-…` pod going Pending → Running.

| T+ | Action / cursor | Beats |
|---|---|---|
| 1:15 | Cmd-2 (or click Tab 2). Mouse to latest run row → click. | • Every iter is its own KFP run. Fully traceable. |
| 1:23 | DAG visible: preprocess → train → evaluate. Cursor traces each node. | • Three stages, each its own pod. Crash halts the run, the loop catches it as a failed experiment. No half-broken state. |
| 1:33 | Click `train` task → Logs tab. Cursor parks. | • Real training, in-cluster. Loss streams live. |
| 1:40 | Quick hover back on DAG. | • CPU here. GPU pool is a one-line manifest. Pipeline unchanged. |

### Segment 4 — MLflow (1:45 → 2:20) · 35s

**Visual:** Tab 3, MLflow `auto-experiment` runs. Switch when train pod has been Running >10s — params log immediately.

| T+ | Action / cursor | Beats |
|---|---|---|
| 1:45 | Tab 3 → click latest run. Cursor scrolls Parameters panel. | • Run already has params, metrics, git commit, dataset hash. |
| 1:55 | Cursor highlights cost-tracking row (input/output tokens, USD). | • Loop logs its own bill. You can answer "did this experiment pay for itself." |
| 2:02 | Click Compare → pick iter 0 + this iter → click. | • Two-click diff. Side-by-side params + metrics. |
| 2:10 | Tab 4 (Models page) → click `classifier`. Cursor on `@champion` row. | • Every train registers a version. `@champion` only moves when AUC beats the current. The gate. |
| 2:18 | Anchor line. | • Tracking is non-negotiable for unattended runs. Same MLflow a human team uses — just with a non-human user. |

### Segment 5 — GitHub PR + ArgoCD (2:20 → 2:45) · 25s

| T+ | Action / cursor | Beats |
|---|---|---|
| 2:20 | Tab 5. Click latest auto-PR. Cursor on PR title (`bump classifier v… → vN+1`). | • Iter beats champion → PR opens. Signed by a GitHub App, not a human user. Audit trail. |
| 2:30 | Cursor pans to cost summary block, then green CI checks. | • PR body has cost summary. CI lint + test + Docker pass. Auto-merged. |
| 2:38 | Tab 6 → ArgoCD app. Cursor on Sync status. | • Cluster sees the merge: OutOfSync → Syncing → Synced. GitOps. No `kubectl apply`. |

### Segment 6 — The closed loop (2:45 → 3:00) · 15s

**Visual:** Terminal full-screen, big font. Cursor blinking at prompt.

| T+ | Action / cursor | Beats |
|---|---|---|
| 2:45 | Recall `curl http://34.47.242.89/predict …`. Cursor at end of line. | • Hit the live endpoint. |
| 2:52 | Enter. Response renders. Cursor highlights `"model_version": "N+1"`. | • New version serving. Loop's closed — propose, train, gate, deploy. No human touched a keyboard. |

### Segment 7 — The trajectory + close (3:00 → 3:30) · 30s

**Visual:** Tab 7. `auto_experiment/trajectory.png` fullscreen (Preview.app ⌘+F, or browser fullscreen). Generate via `make plot-trajectory` after the run finishes.

A single static plot beats scrolling the MLflow runs list — the whole story reads in one frame.

| T+ | Action / cursor | Beats |
|---|---|---|
| 3:00 | Open `trajectory.png` fullscreen. Cursor parked. | • The trajectory of the run. Iter 0 on the left — bad baseline. Cyan step line: promoted champion. Only moves when a candidate wins. |
| 3:15 | Cursor traces the flat stagnation tail. | • Loop ran until it stopped seeing improvement. Signed off by the gate, not by me. |
| 3:25 | Hold 5s. Deadpan. | • That's autoresearch. |
| 3:30 | Stop recording. | — |

---

## 2. The threading identifier — `classifier vN+1`

The visual motif: one version number, threaded across **4 surfaces** during the demo. In post, drop a 1-second cyan box (`#22d3ee`) around the version number each time it appears.

| Surface | What you see | Beat |
|---|---|---|
| MLflow Models page | `@champion → v<N+1>` | Segment 4 (T+2:10) |
| GitHub PR title/body | `bump classifier v<N> → v<N+1>` | Segment 5 (T+2:20) |
| ArgoCD sync log | image tag change visible | Segment 5 (T+2:38) |
| `curl /predict` response | `"model_version": "<N+1>"` | Segment 6 (T+2:52) |

---

## 3. Framing — words to use, words to avoid

**Use:**
- "Metric-gated promotion" (not "no human in the loop" — the iter is automated, but the metric gate exists *because* it's autonomous)
- "Only metric-winning candidates ship"
- "GitHub App, not a human user" (signed commits, audit trail)
- "Production-pattern at portfolio scale"

**Avoid:**
- "Production-grade" — overclaim
- "Claude changes any source code and it ships" — Claude proposes params + small training-code changes; arbitrary source code edits would need image rebuild
- "No human in the loop" — too sloppy; what you actually mean is no human in the *rollout* path

---

## 4. Post-production checklist

1. **Trim head + tail.** Cut everything before the first frame of the explainer's title screen. Cut everything after "That's autoresearch."
2. **Strip scratch audio.** Re-record clean voiceover against the picture cut. Studio mic, quiet room, one or two takes per sentence.
3. **Speed-ramp profile:**
   - Opener (0:00 → 1:00): 1×, no ramp. This is the hook.
   - Terminal warmup (1:00 → 1:15): 1×.
   - KFP wait stretches (between train pod start and DAG completion): **5-8× ramp** through pure waiting; drop to 1× for "row appears", "DAG completes".
   - MLflow + ArgoCD beats: 1×, no ramp — these are the payoff, viewer needs to read.
   - `/predict` proof + trajectory close: 1×.
4. **Overlays:**
   - Cyan box around the version number on each of the 4 surfaces.
   - Small "Iter N" text top-left during the iter-by-iter visualization.
5. **Captions:** auto-generate, then proofread — auto-captions mangle "MLflow", "ArgoCD", "Kubeflow", "@champion", "GitOps".
6. **Music:** sparse ambient pad at -22dB, ducked under voice. Or silence — silence works fine for a technical demo.
7. **Exports:**
   - YouTube / portfolio: 3:30 cut, 1920×1080 mp4.
   - LinkedIn 60-90s: opener (40s, animated explainer) + MLflow + ArgoCD payoff beats (20s) + `/predict` thread + trajectory close (15s). 1920×1080 mp4.
   - README GIF: 15s teaser of just the explainer's animated loop with the metric ticking. 800px wide, ≤8MB.

---

## 5. If something goes wrong mid-take

- **Iter 1 reverts (AUC under champion):** narrate it once ("the gate held — live model wasn't touched"), stop recording, re-run. A revert is great content if you have a 10-iter cut, but the 3:30 demo needs a successful promotion to land the proof beat. Re-shoot.
- **KFP run fails:** narrate it ("loop tolerated the failure — live model unaffected"), stop, re-run.
- **ArgoCD doesn't sync within 60s:** click the `Refresh` button on the App page. If still stuck, stop and check `kubectl -n argocd logs deploy/argocd-application-controller`.
- **`/predict` returns 422 or 503:** stop. Check `/health` first. The deployment may be still rolling. Better to skip the proof beat than show an error.
- **Notification pops up:** stop, clear notifications, restart take.
- **You misspeak:** keep going. Scratch audio is being stripped anyway — clean voiceover comes later.

---

## 6. One-Saturday plan

| Stage | Time | What |
|---|---|---|
| Pre-flight | 15-20 min | §0 checklist + sticky-note IDs |
| Practice run | 10-15 min | Walk the full table without recording. Confirm iter 1 timing — it might be faster or slower than 30s of KFP wait. Adjust speed-ramps in post. |
| Record | 10 min real-time, ~5 min hands-on | Press record, walk the table, stop. |
| Edit | 45-60 min | Trim, speed-ramps, overlays, captions, export. |
| Voiceover | 30-45 min, anytime later | Clean audio against picture cut. |

**Total: ~2-3 hours wall-clock, $0 stack.**

---

## 7. One-sentence summary

> An LLM iterates against a quantitative metric on Kubernetes — proposes a change, KFP trains and evaluates it, MLflow promotes only winners, a signed GitHub PR rolls them out via ArgoCD, and the live API serves the new model. Every layer of the stack agrees on which version is in production.
