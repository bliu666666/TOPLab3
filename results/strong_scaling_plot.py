import matplotlib.pyplot as plt

threads = [1, 2, 4, 8, 16]

avg_times = [3.183640, 1.768867, 0.896376, 0.679870, 0.554103]
avg_gflops = [0.6747, 1.2133, 2.3967, 3.1800, 3.8733]

ideal_gflops = [avg_gflops[0] * t for t in threads]

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(threads, avg_times, marker='o', linewidth=2, label="Measured Time")
plt.xlabel("Number of Threads")
plt.ylabel("Execution Time (s)")
plt.title("Strong Scaling: Execution Time")
plt.grid(True)
plt.xticks(threads)

plt.subplot(1, 2, 2)
plt.plot(threads, avg_gflops, marker='o', linewidth=2, label="Measured GFLOP/s")
plt.xlabel("Number of Threads")
plt.ylabel("Performance (GFLOP/s)")
plt.title("Strong Scaling: Performance")
plt.grid(True)
plt.xticks(threads)
plt.legend()

plt.tight_layout()
plt.savefig("strong_scaling_plot.png")
plt.show()