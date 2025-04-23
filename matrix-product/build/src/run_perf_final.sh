#!/bin/bash

M=1024
N=1024
K=1024
BS=32  # The optimal blockSize selected

echo "Strong Scaling Output (Matrix: $M x $N x $K, blockSize=$BS)"
echo "=============================================================="

for t in 1 2 4 8 16
do
  export OMP_NUM_THREADS=$t
  echo "Running with $t threads..."
  ./top.matrix_product $M $N $K $BS
  echo "--------------------------------------------------------------"
done
