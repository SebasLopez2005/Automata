# Greedy Heuristic Solution - Knapsack / Product Selection
import time
from datasets import datasets
import matplotlib.pyplot as plt

# ── Greedy heuristic ────────────────────────────────────────────────────────
def greedy_knapsack(weights, profits, capacity):
    """
    Sort items by value-to-weight ratio (highest first) and greedily pick
    each item if it still fits.  O(n log n) time, O(n) space.
    """
    n = len(weights)
    # Pair items with their ratio and original index
    items = sorted(range(n),
                   key=lambda i: profits[i] / weights[i],
                   reverse=True)

    total_profit = 0
    remaining = capacity
    selected = []

    for i in items:
        if weights[i] <= remaining:
            selected.append(i)
            total_profit += profits[i]
            remaining  -= weights[i]

    selected.sort()          # restore original order for readability
    return total_profit, selected

# ── DP bottom-up (exact) ─────────────────────────────────────────────────────
def knapsack_dp(weights, profits, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] > w:
                dp[i][w] = dp[i-1][w]
            else:
                dp[i][w] = max(dp[i-1][w],
                               profits[i-1] + dp[i-1][w - weights[i-1]])
    w = capacity
    selected = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            selected.append(i-1)
            w -= weights[i-1]
    selected.reverse()
    return dp[n][capacity], selected

# ── Run both on the five base datasets ──────────────────────────────────────
print("=" * 65)
print(f"{'Dataset':<18} {'DP profit':>10} {'Gr profit':>10} "
      f"{'DP time(s)':>12} {'Gr time(s)':>12} {'Quality%':>9}")
print("=" * 65)

dp_times, gr_times, qualities = [], [], []
labels = []

for weights, profits, capacity in datasets:
    label = f"n={len(weights)},W={capacity}"
    labels.append(label)

    t0 = time.perf_counter()
    dp_profit, _ = knapsack_dp(weights, profits, capacity)
    dp_time = time.perf_counter() - t0

    t0 = time.perf_counter()
    gr_profit, _ = greedy_knapsack(weights, profits, capacity)
    gr_time = time.perf_counter() - t0

    quality = 100 * gr_profit / dp_profit if dp_profit else 100
    dp_times.append(dp_time)
    gr_times.append(gr_time)
    qualities.append(quality)

    print(f"{label:<18} {dp_profit:>10} {gr_profit:>10} "
          f"{dp_time:>12.6f} {gr_time:>12.6f} {quality:>8.2f}%")

# ── Large-scale experiment (greedy only – DP would be very slow) ─────────────
print("\nLarge-scale (greedy only):")
large_datasets = [
    (list(range(1, n+1)), list(range(10, 10*n+1, 10)), W)
    for n, W in [(500, 5000), (1000, 20000), (2000, 50000),
                 (5000, 100000), (10000, 200000)]
]
large_labels, large_times = [], []

for weights, profits, capacity in large_datasets:
    label = f"n={len(weights)},W={capacity}"
    large_labels.append(label)
    t0 = time.perf_counter()
    gr_profit, _ = greedy_knapsack(weights, profits, capacity)
    gr_time = time.perf_counter() - t0
    large_times.append(gr_time)
    print(f"  {label:<22}  profit={gr_profit:>12}  time={gr_time:.6f}s")

# ── Plot 1: runtime comparison on base datasets ───────────────────────────────
xs = range(len(labels))
fig, axes = plt.subplots(1, 2, figsize=(13, 4))

ax = axes[0]
ax.plot(xs, dp_times,  marker="o", label="DP (exact)",   color="steelblue", linewidth=2)
ax.plot(xs, gr_times,  marker="s", label="Greedy (heur.)",color="darkorange",linewidth=2)
ax.set_xticks(xs); ax.set_xticklabels(labels, rotation=20, ha="right")
ax.set_ylabel("Time (seconds)"); ax.set_xlabel("Dataset")
ax.set_title("Runtime: DP vs Greedy"); ax.legend(); ax.grid(axis="y", linestyle="--", alpha=0.4)

ax = axes[1]
ax.bar(xs, qualities, color="mediumseagreen", width=0.5)
ax.set_xticks(xs); ax.set_xticklabels(labels, rotation=20, ha="right")
ax.set_ylim(0, 110); ax.set_ylabel("Solution quality (% of optimal)")
ax.set_xlabel("Dataset"); ax.set_title("Greedy quality vs optimal (DP)")
ax.axhline(100, linestyle="--", color="gray", alpha=0.6)
ax.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
plt.savefig("comparison_plot.png", dpi=150)
print("\nSaved comparison_plot.png")

# ── Plot 2: greedy scalability ────────────────────────────────────────────────
lxs = range(len(large_labels))
plt.figure(figsize=(9, 4))
plt.plot(lxs, large_times, marker="o", color="darkorange", linewidth=2)
plt.xticks(lxs, large_labels, rotation=20, ha="right")
plt.ylabel("Time (seconds)"); plt.xlabel("Dataset (items n, capacity W)")
plt.title("Greedy heuristic: scalability to large inputs")
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.savefig("scalability_plot.png", dpi=150)
print("Saved scalability_plot.png")