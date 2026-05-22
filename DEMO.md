# Autoresearch Demo Script

> Final script for the ~5-minute demo. Local-only doc (gitignored: no — checked in so future-me has it).
> **Target cut:** ~5:15.
> **Recording tool:** screen recorder (ScreenKite, OBS, QuickTime — anything that captures full screen).
> **Camera:** off. Webcam overlay disabled.

The script splits cleanly into **two energies**:
- **0:00 – 1:00 — opener.** Flashy, hook-driven, narrated against the animated explainer (`assets/autoresearch-explainer.html`). This is where you earn the viewer's attention.
- **1:00 – 5:15 — the walkthrough.** Plain, factual, technical. "This is what's happening, here's why it matters." Don't try to be flashy — the system is the proof.

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
   - Tab 2: KFP UI → `http://34.93.2.209/#/runs`
   - Tab 3: MLflow → `http://34.180.20.197:5000/#/experiments/3` (the `auto-experiment` experiment)
   - Tab 4: MLflow Models → `http://34.180.20.197:5000/#/models/classifier`
   - Tab 5: GitHub repo PR list → `https://github.com/my-neme-eh-jeff/ML-deployment-system-for-autoresearch/pulls`
   - Tab 6: ArgoCD → `http://34.100.246.237/applications/inference-api` (logged in; password in local `NOTES.md`)

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

---

## 1. Segment-by-segment script

T+ times are final-cut timestamps.

### Segment 1 — Opener (0:00 → 0:55) · animated explainer

**Visual:** Tab 1, `assets/autoresearch-explainer.html`, fullscreen.

| T+ | Action (key press) | What to say |
|---|---|---|
| 0:00 | Stage 0 — title only on screen. | *"Karpathy gave the talk. He showed an LLM running on a Mac mini farm in his apartment — proposing experiments, observing outcomes, iterating until it found something better. It was beautiful. And it was completely irreproducible for anyone watching."* |
| 0:08 | Press `Space` → loop arc draws in. Nodes fade in. | *"This is what autoresearch is. You give an agent a problem, a quantitative metric, and let it loop. It proposes a change, runs the experiment, observes the metric, updates its memory."* |
| 0:18 | Press `Space` → dot starts moving, AUC counter starts ticking 0.749 → 0.812. | *"Every iteration is one trip around. The metric improves — or doesn't."* |
| 0:24 | Press `Space` → right-side title + lede appear. | *"You let it run unattended until something tells it to stop."* |
| 0:30 | Press `Space` → bullet 1: time budget. | *"It runs out of time —"* |
| 0:33 | Press `Space` → bullet 2: threshold. | *"hits the metric threshold you set —"* |
| 0:36 | Press `Space` → bullet 3: stagnation. | *"or stagnates with no improvement for N iterations."* |
| 0:42 | Press `Space` → dot freezes, AUC value glows accent gold. Hold for 5s. | *"But here's the thing. Karpathy ran it on hardware most of us don't have. The state-of-the-art models people actually want to use are too big to fit on your laptop. And every demo of agent-driven research shows one agent in a single notebook — no system for multiple agents and humans collaborating on the same problem without duplicating each other's work."* |
| 0:55 | Cut to terminal tab. | *"This project is that system."* |

**Recording note:** The explainer's `Space` advances are baked into the visual cuts. Practice the timing once so the keypresses sync with your sentences — there should be no awkward pause between "the metric" and the dot starting to move.

### Segment 2 — Kick off the run (0:55 → 1:25)

**Visual:** Terminal with 3 panes (A: watch, B: make, C: logs). All pre-typed, nothing executed.

| T+ | Action | What to say |
|---|---|---|
| 0:55 | Show the 3 pre-typed commands. | *"Three commands. First, watch the cluster — every pod that spins up, I see it. Second, kick off the loop — 20 iterations, 8-hour budget. Third, tail the driver logs."* |
| 1:05 | Run pane A (watch). | *"Right now: 2 inference pods serving the baseline. AUC 0.749, a one-feature decision tree. Intentionally bad — I want Claude to have room to improve."* |
| 1:12 | Run pane B (make autoresearch-run). | *"Job submitted. Runs in the cluster, not on my laptop."* |
| 1:18 | Pane A: `autoresearch-real-<timestamp>` pod appears as Pending → ContainerCreating → Running. | *"There it is. The driver pod. While it warms up — about five seconds — we're on Kaggle's IEEE-CIS fraud detection. Five-hundred-and-ninety-thousand transactions, four-hundred-and-thirty-three features."* |

### Segment 3 — KFP UI (1:25 → 2:30)

**Visual:** Tab 2, KFP UI. The autoresearch-driven pipeline run will appear at the top of the runs list ~30s after job start.

**When to switch tabs:** as soon as Pane A shows the first `preprocess-...` pod transition from Pending → Running. That means Claude has finished proposing and the KFP run is submitted.

| T+ | Action | What to say |
|---|---|---|
| 1:25 | Tab to KFP UI. Click into the latest run. | *"Kubeflow Pipelines. Every iteration is its own KFP run, fully traceable."* |
| 1:35 | Show the DAG: preprocess → train → evaluate. Point at each box. | *"Three-stage pipeline — preprocess, train, evaluate. Each one is its own pod. If train crashes, the run halts and the loop catches it as a failed experiment. No half-broken state."* |
| 1:50 | Click into the `train` task → Input/Output tab. | *"Here are the params Claude proposed this iteration — the model class, the features added, the hyperparams. The atomic record of one experiment."* |
| 2:05 | Click `train` → Logs tab. Show streaming Python output. | *"Real training, real data, in-cluster. You can read the loss go down in real time."* |
| 2:18 | Throwaway line still on KFP. | *"By the way — we're CPU only. The model's small. But that's a one-line manifest change to request a GPU and point at a GPU node pool. The pipeline above doesn't change."* |

### Segment 4 — MLflow (2:30 → 3:30)

**Visual:** Tab 3, MLflow `auto-experiment` runs page → click latest run.

**Trigger to switch:** the train pod has gone Running for >10s. `train.py` calls `mlflow.start_run()` and logs params immediately. So even during training, MLflow already has the run with params + streaming metrics.

| T+ | Action | What to say |
|---|---|---|
| 2:30 | Tab to MLflow → click latest auto-experiment run. | *"While evaluate finishes up, MLflow already has the run. Every metric, every param, the git commit Claude is on, the dataset hash — all logged."* |
| 2:42 | Scroll the Parameters panel. Point at the cost-tracking metrics. | *"Input tokens, output tokens, the dollar cost of the Anthropic call. The loop logs its own cost. So you can answer: did this experiment pay for itself."* |
| 2:55 | Click `Compare` → select iter-0 baseline + current iter → click. | *"Two-click diff. Params side-by-side, metrics side-by-side. You see exactly what changed and what it did to AUC."* |
| 3:10 | Tab 4 (MLflow Models page) → click `classifier`. | *"Every training run registers a new version. The `@champion` alias only moves if the new AUC beats the current champion. That's the promotion gate. No regression makes it past this."* |
| 3:20 | The "why this matters" line. | *"An autoresearch loop without experiment tracking is just an LLM thrashing in the dark. This is the same MLflow a human data scientist uses — same UI, same primitives. We just have a non-human user. When the agent runs 20 unattended experiments, you need to know what was tried, what worked, and why. Tracking is non-negotiable."* |

### Segment 5 — GitHub PR + ArgoCD (3:30 → 4:15)

**Visual:** Tab 5 (GitHub PRs) → click the new auto-PR. Then Tab 6 (ArgoCD).

| T+ | Action | What to say |
|---|---|---|
| 3:30 | Tab to GitHub PR. Show PR body. | *"When an iteration beats the champion, the loop opens a pull request — signed by a GitHub App, not a human user. Proper service identity, fully traceable in the audit log."* |
| 3:40 | Point at: cost summary block, the diff (usually `configs/params.yaml` or `src/train.py`), the green CI checks. | *"PR body has the cost summary. Diff is one file change. CI ran — lint, tests, Docker build, image push. PR auto-merged to main."* |
| 3:55 | Tab to ArgoCD. | *"ArgoCD watches `k8s/` on main. The PR bumped the inference-api image tag. ArgoCD picks it up — OutOfSync, then Syncing, then Synced."* |
| 4:05 | Point at the sync history / app health. | *"GitOps means the cluster is whatever git says it is. No `kubectl apply` from a laptop. No drift."* |

### Segment 6 — The closed loop (4:15 → 4:45)

**Visual:** Terminal full-screen, big font.

| T+ | Action | What to say |
|---|---|---|
| 4:15 | Type or recall: `curl -X POST http://34.47.242.89/predict -H 'content-type: application/json' -d '{"data": {"TransactionAmt": 100.0, "ProductCD": "W"}}'` | *"And the inference endpoint is serving the new champion."* |
| 4:22 | Run it. Response renders with `"model_version": "<N+1>"`. | *"`model_version` field tells you which one. The loop is closed — Claude proposed, the cluster trained and evaluated, the registry promoted, GitOps deployed, real traffic hits the new model. No human touched a keyboard."* |

### Segment 7 — The trajectory + close (4:45 → 5:15)

**Visual:** Tab 3, MLflow `auto-experiment` runs list, sorted by start time descending.

| T+ | Action | What to say |
|---|---|---|
| 4:45 | Tab to MLflow runs list. Scroll slowly from top to iter 0. | *"And here's the trajectory. Iteration 0 — AUC 0.749, the bad baseline. Iteration N — whatever Claude got to. Every experiment logged, every one reproducible, every one signed off by the cluster, not by me."* |
| 5:08 | Hold on the iter-0 row for 2 seconds. Deadpan close. | *"That's autoresearch."* |
| 5:15 | Stop recording. | — |

---

## 2. The threading identifier — `classifier vN+1`

The visual motif: one version number, threaded across **4 surfaces** during the demo. In post, drop a 1-second cyan box (`#22d3ee`) around the version number each time it appears.

| Surface | What you see | Beat |
|---|---|---|
| MLflow Models page | `@champion → v<N+1>` | Segment 4 |
| GitHub PR title/body | `bump classifier v<N> → v<N+1>` | Segment 5 |
| ArgoCD sync log | image tag change visible | Segment 5 |
| `curl /predict` response | `"model_version": "<N+1>"` | Segment 6 |

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
   - Opener (0:00 → 0:55): 1×, no ramp. This is the hook.
   - Terminal warmup (0:55 → 1:25): 1×.
   - KFP wait stretches (between train pod start and DAG completion): **5-8× ramp** through pure waiting; drop to 1× for "row appears", "DAG completes".
   - MLflow + ArgoCD beats: 1×, no ramp — these are the payoff, viewer needs to read.
   - Prove + trajectory close: 1×.
4. **Overlays:**
   - Cyan box around the version number on each of the 4 surfaces.
   - Small "Iter N" text top-left during the iter-by-iter visualization.
5. **Captions:** auto-generate, then proofread — auto-captions mangle "MLflow", "ArgoCD", "Kubeflow", "@champion", "GitOps".
6. **Music:** sparse ambient pad at -22dB, ducked under voice. Or silence — silence works fine for a technical demo.
7. **Exports:**
   - YouTube / portfolio: 5:15 cut, 1920×1080 mp4.
   - LinkedIn 60-90s: opener (20s, animated explainer) + terminal kickoff (10s) + MLflow + ArgoCD payoff beats (30s) + `/predict` thread (10s). 1920×1080 mp4.
   - README GIF: 15s teaser of just the explainer's animated loop with the AUC counter ticking. 800px wide, ≤8MB.

---

## 5. If something goes wrong mid-take

- **Iter 1 reverts (AUC under champion):** narrate it once ("the gate held — live model wasn't touched"), stop recording, re-run. A revert is great content if you have a 10-iter cut, but the 5-min demo needs a successful promotion to land the proof beat. Re-shoot.
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
