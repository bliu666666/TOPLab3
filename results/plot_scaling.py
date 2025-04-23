import matplotlib.pyplot as plt

threads = [1, 2, 4, 8, 16]

# LayoutRight data
times_right = [14.830967, 13.751729, 6.835002, 3.359703, 1.762930]
flops_right = [1.45e+08, 1.56e+08, 3.14e+08, 6.39e+08, 1.22e+09]

# LayoutLeft data
times_left = [13.654579, 13.429957, 6.780749, 3.437970, 1.768286]
flops_left = [1.57e+08, 1.60e+08, 3.17e+08, 6.25e+08, 1.21e+09]

# Final performance comparison of array layout
times_right_perf = [14.858851, 12.830513, 6.646810, 3.328559, 3.087749]
flops_right_perf = [1.45e+08, 1.67e+08, 3.23e+08, 6.45e+08, 6.95e+08]

times_left_perf = [14.532644, 12.745199, 6.635249, 3.311722, 1.755507]
flops_left_perf = [1.48e+08, 1.68e+08, 3.24e+08, 6.48e+08, 1.22e+09]

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

# Figure: Run time vs number of threads(before perf)
plt.figure()
plt.plot(threads, times_right, marker='o', label='LayoutRight')
plt.plot(threads, times_left, marker='o', label='LayoutLeft')
plt.xlabel('Number of Threads')
plt.ylabel('Elapsed Time (s)')
plt.title('Threads vs Elapsed Time')
plt.legend()
plt.grid(True)
plt.savefig('compare_time_origin.png')

# Figure: FLOP/s vs number of threads(before perf)
plt.figure()
plt.plot(threads, [f / 1e9 for f in flops_right], marker='o', label='LayoutRight')
plt.plot(threads, [f / 1e9 for f in flops_left], marker='o', label='LayoutLeft')
plt.xlabel('Number of Threads')
plt.ylabel('FLOP/s (GFLOP/s)')
plt.title('Threads vs FLOP/s')
plt.legend()
plt.grid(True)
plt.savefig('compare_flops_origin.png')

# Figure: Run time vs number of threads(after perf)
plt.figure()
plt.plot(threads, times_right_perf, marker='o', label='LayoutRight')
plt.plot(threads, times_left_perf, marker='o', label='LayoutLeft')
plt.xlabel('Number of Threads')
plt.ylabel('Elapsed Time (s)')
plt.title('Threads vs Elapsed Time')
plt.legend()
plt.grid(True)
plt.savefig('compare_time.png')

# Figure: FLOP/s vs number of threads(after perf)
plt.figure()
plt.plot(threads, [f / 1e9 for f in flops_right_perf], marker='o', label='LayoutRight')
plt.plot(threads, [f / 1e9 for f in flops_left_perf], marker='o', label='LayoutLeft')
plt.xlabel('Number of Threads')
plt.ylabel('FLOP/s (GFLOP/s)')
plt.title('Threads vs FLOP/s')
plt.legend()
plt.grid(True)
plt.savefig('compare_flops.png')

plt.show()