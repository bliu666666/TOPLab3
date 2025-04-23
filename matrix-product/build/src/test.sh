#!/bin/bash

export OMP_PROC_BIND=spread
export OMP_PLACES=threads

for t in 1 2 4 8 16
do
  export OMP_NUM_THREADS=$t
  echo "Running with $OMP_NUM_THREADS threads"
  ./top.matrix_product 1024 1024 1024
done