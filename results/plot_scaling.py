import matplotlib.pyplot as plt

# LayoutRight data
threads = [0, 1, 2, 4, 8, 16]  # 0 means "OMP_NUM_THREADS is not set"
times_right = [13.801513, 13.582204, 13.635906, 13.773747, 13.669578, 13.786554]
flops_right = [1.56e+08, 1.58e+08, 1.57e+08, 1.56e+08, 1.57e+08, 1.56e+08]

# LayoutLeft data
times_left = [13.516428, 13.620299, 13.368721, 13.659939, 13.738099, 13.384597]
flops_left = [1.59e+08, 1.58e+08, 1.61e+08, 1.57e+08, 1.56e+08, 1.60e+08]

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

# Draw LayoutRight separately for extensibility
plt.figure()
plt.plot(threads, times_right, marker='o',color='green')
plt.xlabel('Number of Threads')
plt.ylabel('Elapsed Time (s)')
plt.title('Strong Scaling (LayoutRight Only)')
plt.grid(True)
plt.savefig('layoutright_scaling_time.png')

plt.figure()
plt.plot(threads, [f / 1e9 for f in flops_right], marker='o',color='green') 
plt.xlabel('Number of Threads')
plt.ylabel('FLOP/s (GFLOP/s)')
plt.title('FLOP/s Scaling (LayoutRight Only)')
plt.grid(True)
plt.savefig('layoutright_scaling_flops.png')

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