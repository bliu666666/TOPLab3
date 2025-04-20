import matplotlib.pyplot as plt

# LayoutRight data
threads = [0, 1, 2, 4, 8]  # 0 means "OMP_NUM_THREADS is not set"
times_right = [11.096884, 10.532894, 10.707770, 10.823062, 11.029951]
flops_right = [2.42e+07, 2.55e+07, 2.51e+07, 2.48e+07, 2.43e+07]

# LayoutLeft data
times_left = [6.876516,6.562161, 6.428719, 6.575440, 6.933553]
flops_left = [3.90e+07,4.09e+07, 4.18e+07, 4.08e+07, 3.87e+07]

# Figure 1: Run time vs number of threads
plt.figure()
plt.plot(threads, times_right, marker='o', label='LayoutRight')
plt.plot(threads, times_left, marker='o', label='LayoutLeft')
plt.xlabel('Number of Threads')
plt.ylabel('Elapsed Time (s)')
plt.title('Threads vs Elapsed Time')
plt.legend()
plt.grid(True)
plt.savefig('compare_time.png')

# Figure 2: FLOP/s vs number of threads
plt.figure()
plt.plot(threads, [f / 1e9 for f in flops_right], marker='o', label='LayoutRight')
plt.plot(threads, [f / 1e9 for f in flops_left], marker='o', label='LayoutLeft')
plt.xlabel('Number of Threads')
plt.ylabel('FLOP/s (GFLOP/s)')
plt.title('Threads vs FLOP/s')
plt.legend()
plt.grid(True)
plt.savefig('compare_flops.png')

# Draw LayoutLeft separately for extensibility
plt.figure()
plt.plot(threads, times_left, marker='o', color='green')
plt.xlabel('Number of Threads')
plt.ylabel('Elapsed Time (s)')
plt.title('Strong Scaling (LayoutLeft Only)')
plt.grid(True)
plt.savefig('layoutleft_scaling_time.png')

plt.figure()
plt.plot(threads, [f / 1e9 for f in flops_left], marker='o', color='green')
plt.xlabel('Number of Threads')
plt.ylabel('FLOP/s (GFLOP/s)')
plt.title('FLOP/s Scaling (LayoutLeft Only)')
plt.grid(True)
plt.savefig('layoutleft_scaling_flops.png')

plt.show()