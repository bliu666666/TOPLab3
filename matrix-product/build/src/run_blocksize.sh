#!/bin/bash

# Fixed parameters
M=1024
N=1024
K=1024
THREADS=16
OUTPUT="blocksize_results.txt"

# The blockSize value to test
BLOCK_SIZES=(8 16 32 64 128 256 512)

# Setting thread binding
export OMP_NUM_THREADS=$THREADS
export OMP_PROC_BIND=spread
export OMP_PLACES=threads

echo "BlockSize Benchmark with perf - cache metrics only" >> $OUTPUT
echo "Matrix size: ${M}x${N}x${K}, Threads: ${THREADS}" >> $OUTPUT
echo "===============================================" >> $OUTPUT

# Iterating over blockSize tests
for bs in "${BLOCK_SIZES[@]}"
do
  echo ">>> Running with blockSize = $bs" >> $OUTPUT

  # Execute and record perf performance counters
  perf stat -e cache-references,cache-misses,L1-dcache-loads,L1-dcache-load-misses,LLC-loads,LLC-load-misses \
    ./top.matrix_product $M $N $K $bs 2>> $OUTPUT

  echo "-----------------------------------------------" >> $OUTPUT
done