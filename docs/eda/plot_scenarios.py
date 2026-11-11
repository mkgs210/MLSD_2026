import json
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402


def main():
    root = Path(__file__).resolve().parent
    rows = sorted(
        json.loads((root / "scenario_counts.json").read_text(encoding="utf-8")),
        key=lambda row: row[1],
        reverse=True,
    )
    total = sum(count for _, count in rows)
    top5 = sum(count for _, count in rows[:5]) / total
    labels = [textwrap.fill(label, 40) for label, _ in rows]
    values = [count for _, count in rows]

    fig, ax = plt.subplots(figsize=(11, 8.4))
    fig.patch.set_facecolor("white")
    ax.barh(labels, values, color=["#146A72"] * 5 + ["#A7B8C7"] * (len(rows) - 5))
    ax.invert_yaxis()
    ax.set_xlabel("Уникальные звонки с исходной меткой", labelpad=12)
    ax.set_xlim(0, max(values) * 1.25)
    ax.grid(axis="x", color="#DDE6EC", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", length=0, pad=8)
    for i, n in enumerate(values):
        ax.text(n + 65, i, f"{n:,}".replace(",", " "), va="center", color="#233341")
    fig.text(
        0.04, 0.966, "Сценарии мошеннических звонков людям", fontsize=19, weight="bold"
    )
    subtitle = f"Размеченные звонки: {total:,}".replace(",", " ") + (
        f"   •   Пять крупнейших тем: {top5:.1%}".replace(".", ",")
    )
    fig.text(0.04, 0.926, subtitle, fontsize=12, color="#486070")
    fig.subplots_adjust(left=0.35, right=0.96, bottom=0.10, top=0.89)
    fig.savefig(root / "scenario_coverage.png", dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    main()
