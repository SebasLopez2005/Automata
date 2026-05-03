# Dynamic Programming Solution Bottom Up
import time
from datasets import datasets
import matplotlib.pyplot as plt

def knapsack(weights, profits, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    # Build DP table
    for i in range(1, n + 1):  # Items
        for w in range(capacity + 1):  # Capacity from 0 to W
            if weights[i-1] > w:  # If item is too heavy, exclude it
                dp[i][w] = dp[i-1][w]
            else:
                dp[i][w] = max(dp[i-1][w], profits[i-1] + dp[i-1][w - weights[i-1]])

    # Find selected items
    w = capacity
    selected_items = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:  # If the value changed, the item was included
            selected_items.append(i-1)  # Store item index
            w -= weights[i-1]

    selected_items.reverse()  # To get items in order

    return dp[n][capacity], selected_items

times = []

for weights, profits, capacity in datasets:
    start_time = time.time()
    max_profit, items = knapsack(weights, profits, capacity)
    end_time = time.time()
    times.append(end_time - start_time)
    print(f"Maximum Profit: {max_profit}")
    print(f"Items in Knapsack: {items}")
    print(f"Time taken: {end_time - start_time} seconds")

x_labels = [f"n={len(w)}, W={cap}" for w, _, cap in datasets]
xs = range(len(times))
plt.figure(figsize=(9, 4))
plt.plot(xs, times, marker="o", color="steelblue", linewidth=2)
plt.xticks(xs, x_labels, rotation=20, ha="right")
plt.ylabel("Time (seconds)")
plt.xlabel("Dataset (items n, capacity W)")
plt.title("DP bottom-up knapsack: wall-clock time per dataset")
plt.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
plt.show()