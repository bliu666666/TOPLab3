#!/bin/bash

# 固定参数
M=1024
N=1024
K=1024
THREADS=16
OUTPUT="blocksize_results.txt"

# 需要测试的 blockSize 值
BLOCK_SIZES=(8 16 32 64 128 256 512)

# 设置线程绑定
export OMP_NUM_THREADS=$THREADS
export OMP_PROC_BIND=spread
export OMP_PLACES=threads

echo "BlockSize Benchmark with perf - cache metrics only" >> $OUTPUT
echo "Matrix size: ${M}x${N}x${K}, Threads: ${THREADS}" >> $OUTPUT
echo "===============================================" >> $OUTPUT

# 遍历 blockSize 测试
for bs in "${BLOCK_SIZES[@]}"
do
  echo ">>> Running with blockSize = $bs" >> $OUTPUT

  # 执行并记录 perf 性能计数器（不输出到终端）
  perf stat -e cache-references,cache-misses,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses \
    ./top.matrix_product $M $N $K $bs 2>> $OUTPUT

  echo "-----------------------------------------------" >> $OUTPUT
done