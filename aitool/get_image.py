# -*- coding: UTF-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.ticker import MaxNLocator
from uuid import uuid4
from io import BytesIO

def plot_rating_score(data, name="小诗乃", show=False):
    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
    plt.rcParams['axes.unicode_minus'] = False
    ids = list(data.keys())
    ratings = [data[k]["rating"] for k in ids]
    scores = [data[k]["score"] for k in ids]

    x = np.arange(len(ids))
    cum_score = np.cumsum(scores)

    avg_rating = sum(ratings) / len(ratings)

    y_min = math.floor(min(ratings) / 5) * 5 if min(ratings) < 60 else 60
    y_max = 100

    # =========================
    # Figure
    # =========================
    fig, (ax1, ax2) = plt.subplots(
        2, 1,
        figsize=(14, 8),
        sharex=True,
        gridspec_kw={"height_ratios": [1, 1.3]}
    )

    # =========================
    # ⭐ Rating
    # =========================
    ax1.plot(x, ratings, marker="o", color="#1f77b4", linewidth=2)
    ax1.fill_between(x, ratings, alpha=0.08, color="#1f77b4")

    for i, v in enumerate(ratings):
        ax1.text(
            i, v + 0.25,
            f"{v:.2f}",
            ha="center",
            fontsize=8,
            color="#1f77b4",
            alpha=0.9
        )

    ax1.axhline(avg_rating, linestyle="--", alpha=0.7, color="#ff7f0e")

    ax1.text(
        len(ids) + 1, avg_rating - 1.0,
        f"AVG {avg_rating:.2f}",
        ha="left",
        va="center",
        fontsize=9,
        color="#ff7f0e"
    )

    ax1.set_ylabel("Rating")
    ax1.set_ylim(y_min, y_max)
    ax1.set_title(f"{name}的motral4.1 Rating", fontsize=12)
    ax1.grid(alpha=0.2)

    # =========================
    # ⭐ PT
    # =========================
    colors = np.where(np.array(scores) >= 0, "#2ca02c", "#d62728")

    ax2.bar(x, scores, color=colors, alpha=0.35)
    ax2.plot(x, cum_score, color="#6a5acd", linewidth=2)

    ax2.axhline(0, color="gray", linewidth=1)

    for i, v in enumerate(cum_score):
        ax2.text(
            i,
            v + (5 if v >= 0 else -5),
            f"{v:.0f}",
            ha="center",
            fontsize=8,
            color="black",
            alpha=0.85
        )

    ax2.set_ylabel("PT")
    ax2.set_title(f"{name}的近期PT点 获取趋势", fontsize=12)
    ax2.grid(alpha=0.2)

    # =========================
    # X axis
    # =========================
    # x_labels = [f"{i+1}" for i in range(len(ids))]
    x = np.arange(1, len(ids) + 1)
    ax2.xaxis.set_major_locator(MaxNLocator(nbins=15))

    plt.xlim(-0.5, len(ids) + 0.8)
    plt.tight_layout()
    if show:
        plt.show()

    buf = BytesIO()

    plt.savefig(
        buf,
        format="png",
        dpi=150,
        bbox_inches="tight"
    )

    buf.seek(0)

    image_bytes = buf.getvalue()

    plt.close(fig)

    return image_bytes

if __name__ == '__main__':
    data = {
        "__id1": {"rating": 83.54, "score": -200},
        "__id2": {"rating": 92.91, "score": 63},
        "__id3": {"rating": 84.86, "score": 57},
        "__id4": {"rating": 86.45, "score": 135},
        "__id5": {"rating": 90.43, "score": -10},
        "__id6": {"rating": 83.11, "score": 67},
        "__id7": {"rating": 87.14, "score": 134},
        "__id8": {"rating": 93.86, "score": 165},
        "__id9": {"rating": 86.46, "score": -220},
        "__id10": {"rating": 88.44, "score": 70},
        "__id11": {"rating": 91.72, "score": -2}
    }
    image_bytes = plot_rating_score(data, "小诗乃")
    with open(f"小诗乃_{uuid4().hex[:8]}.png", "wb") as f:
        f.write(image_bytes)