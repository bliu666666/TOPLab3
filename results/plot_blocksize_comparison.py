import matplotlib.pyplot as plt

# Blocking versions block sizes
block_sizes = [8, 16, 32, 64, 128, 256, 512]

# Original version data (uniformly using LayoutLeft)
original_runtime = 1.068  # 秒
original_flops = 2.01     # GFLOP/s
original_l1_miss = 51.75  # %
original_llc_miss = 0.08  # %

# Cache blocking version data
blocked_runtime = [0.7537, 0.7685, 0.7154, 0.7256, 0.7838, 0.7283, 0.7517]
blocked_flops   = [2.17, 2.13, 2.29, 2.26, 2.09, 2.26, 2.19]
blocked_l1_miss = [25.09, 33.07, 36.64, 39.29, 41.36, 41.11, 40.99]
blocked_llc_miss= [0.10, 0.24, 0.18, 0.19, 0.30, 0.14, 0.12]

# The original data is expanded into a list for easy drawing comparison
original_runtime_list = [original_runtime] * len(block_sizes)
original_flops_list   = [original_flops] * len(block_sizes)
original_l1_list      = [original_l1_miss] * len(block_sizes)
original_llc_list     = [original_llc_miss] * len(block_sizes)

# Figure 1: Runtime comparison
plt.figure(figsize=(8, 5))
plt.plot(block_sizes, original_runtime_list, label='Original', linestyle='--', marker='s')
plt.plot(block_sizes, blocked_runtime, label='Cache Blocked', marker='o')
plt.title('Runtime vs Block Size')
plt.xlabel('Block Size')
plt.ylabel('Runtime (seconds)')
plt.legend()
plt.grid(True)
plt.savefig('runtime_comparison.png')
plt.close()

# Figure 2: FLOP/s comparison
plt.figure(figsize=(8, 5))
plt.plot(block_sizes, original_flops_list, label='Original', linestyle='--', marker='s')
plt.plot(block_sizes, blocked_flops, label='Cache Blocked', marker='o')
plt.title('FLOP/s vs Block Size')
plt.xlabel('Block Size')
plt.ylabel('FLOP/s (GFLOP/s)')
plt.legend()
plt.grid(True)
plt.savefig('flops_comparison.png')
plt.close()

# Figure 3: L1 miss rate comparison
plt.figure(figsize=(8, 5))
plt.plot(block_sizes, original_l1_list, label='Original', linestyle='--', marker='s')
plt.plot(block_sizes, blocked_l1_miss, label='Cache Blocked', marker='o')
plt.title('L1 Miss Rate vs Block Size')
plt.xlabel('Block Size')
plt.ylabel('L1 Miss Rate (%)')
plt.legend()
plt.grid(True)
plt.savefig('l1_miss_comparison.png')
plt.close()

# Figure 4: LLC miss rate comparison
plt.figure(figsize=(8, 5))
plt.plot(block_sizes, original_llc_list, label='Original', linestyle='--', marker='s')
plt.plot(block_sizes, blocked_llc_miss, label='Cache Blocked', marker='o')
plt.title('LLC Miss Rate vs Block Size')
plt.xlabel('Block Size')
plt.ylabel('LLC Miss Rate (%)')
plt.legend()
plt.grid(True)
plt.savefig('llc_miss_comparison.png')
plt.close()

print("- runtime_comparison.png")
print("- flops_comparison.png")
print("- l1_miss_comparison.png")
print("- llc_miss_comparison.png")