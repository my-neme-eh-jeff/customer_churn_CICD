"""Render the autoresearch trajectory plot used in the demo close.

Reads `auto_experiment/history.tsv`, writes `auto_experiment/trajectory.png`.

Design tracks `assets/autoresearch-explainer.html`:
- Dark canvas (`#0a0a0f`), soft panel (`#14141c`).
- Candidates scattered, colored by outcome (lime = improved, red = failed/rejected,
  gold = reverted). Running champion drawn as a cyan line — same hue as the
  explainer's loop arc. Baseline marker at iter 0. Stagnation annotation at the
  right edge if the tail of the run is non-improving.

Run via `make plot-trajectory` (no arguments).
"""

from __future__ import annotations

import csv
import os
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parent.parent
HISTORY = Path(
    os.environ.get("HISTORY_TSV") or ROOT / "auto_experiment" / "history.tsv"
)
OUT = Path(os.environ.get("OUT_PNG") or ROOT / "auto_experiment" / "trajectory.png")

BG = "#0a0a0f"
PANEL = "#14141c"
FG = "#f4f4f5"
MUTED = "#71717a"
CYAN = "#22d3ee"
LIME = "#84cc16"
RED = "#f87171"
GOLD = "#fbbf24"

OUTCOME_COLOR = {"improved": LIME, "failed": RED, "reverted": GOLD}


def _read_rows() -> list[dict]:
    with HISTORY.open() as f:
        return list(csv.DictReader(f, delimiter="\t"))


def _running_champion(rows: list[dict]) -> tuple[list[int], list[float]]:
    """Step function: champion AUC after each iteration."""
    xs: list[int] = []
    ys: list[float] = []
    champion = float(rows[0]["auc_before"]) if rows[0]["auc_before"] else 0.0
    xs.append(0)
    ys.append(champion)
    for r in rows:
        auc_after = float(r["auc_after"])
        if r["outcome"] == "improved" and auc_after > champion:
            champion = auc_after
        xs.append(int(r["exp_num"]))
        ys.append(champion)
    return xs, ys


def main() -> None:
    if not HISTORY.exists():
        raise SystemExit(f"history.tsv not found at {HISTORY}")

    rows = _read_rows()
    if not rows:
        raise SystemExit(
            "history.tsv has no data rows — run `make autoresearch-run` first."
        )

    fig, ax = plt.subplots(figsize=(14, 7.5), dpi=220)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(PANEL)

    baseline_auc = float(rows[0]["auc_before"])

    ax.axhline(
        baseline_auc,
        color=MUTED,
        linestyle="--",
        linewidth=1,
        alpha=0.5,
        zorder=1,
    )
    ax.text(
        0.01,
        baseline_auc,
        "baseline",
        color=MUTED,
        fontsize=10,
        va="bottom",
        ha="left",
        transform=ax.get_yaxis_transform(),
    )

    champ_x, champ_y = _running_champion(rows)
    ax.plot(
        champ_x,
        champ_y,
        color=CYAN,
        linewidth=2.4,
        drawstyle="steps-post",
        zorder=3,
        label="champion",
    )

    for r in rows:
        x = int(r["exp_num"])
        y = float(r["auc_after"])
        color = OUTCOME_COLOR.get(r["outcome"], MUTED)
        ax.scatter(
            x,
            y,
            s=110,
            color=color,
            edgecolor=BG,
            linewidth=1.5,
            zorder=4,
        )

    ax.set_xlabel("Iteration", color=FG, fontsize=12)
    ax.set_ylabel("AUC-ROC", color=FG, fontsize=12)

    for spine in ax.spines.values():
        spine.set_color(MUTED)
        spine.set_linewidth(0.6)
    ax.tick_params(colors=FG, length=4)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(True, color=MUTED, alpha=0.15, linewidth=0.5)

    ax.legend(
        handles=[
            Line2D([0], [0], color=CYAN, lw=2.4, label="Running champion"),
            Line2D(
                [0], [0], marker="o", color=LIME, lw=0, markersize=9, label="Improved"
            ),
            Line2D(
                [0], [0], marker="o", color=GOLD, lw=0, markersize=9, label="Reverted"
            ),
            Line2D([0], [0], marker="o", color=RED, lw=0, markersize=9, label="Failed"),
        ],
        loc="upper left",
        bbox_to_anchor=(0.01, 0.99),
        ncol=1,
        frameon=False,
        labelcolor=FG,
        fontsize=10,
    )

    fig.subplots_adjust(left=0.085, right=0.96, top=0.94, bottom=0.11)
    fig.savefig(OUT, facecolor=BG, edgecolor="none", dpi=220)
    try:
        display = OUT.relative_to(ROOT)
    except ValueError:
        display = OUT
    print(f"wrote {display}  ({len(rows)} iterations)")


if __name__ == "__main__":
    main()
