#include <cassert>
#include <cstdlib>
#include <chrono>
#include <cmath>

#include <Kokkos_Core.hpp>
#include <fmt/core.h>

// using Matrix = Kokkos::View<double**, Kokkos::LayoutRight>;
using Matrix = Kokkos::View<double**, Kokkos::LayoutLeft>;

template <class MatrixType>
auto matrix_init(MatrixType& M) -> void {
  static_assert(2 == MatrixType::rank(), "View must be of rank 2");

  Kokkos::parallel_for(
    "init",
    M.extent(0),
    KOKKOS_LAMBDA(int i) {
      for (int j = 0; j < int(M.extent(1)); ++j) {
        M(i, j) = drand48();
      }
    }
  );
}

template <class AMatrixType, class BMatrixType, class CMatrixType>
auto matrix_product_normal(double alpha, AMatrixType const& A, BMatrixType const& B, double beta, CMatrixType& C) -> void {
  static_assert(
    AMatrixType::rank() == 2 && BMatrixType::rank() == 2 && CMatrixType::rank() == 2, "Views must be of rank 2"
  );
  assert(A.extent(0) == C.extent(0));
  assert(B.extent(1) == C.extent(1));
  assert(A.extent(1) == B.extent(0));

  Kokkos::parallel_for(
    "dgemm_kernel",
    A.extent(0),
    KOKKOS_LAMBDA(int i) {
      for (int j = 0; j < int(B.extent(1)); ++j) {
        double acc = 0.0;
        for (int k = 0; k < int(A.extent(1)); ++k) {
          acc += alpha * A(i, k) * B(k, j);
        }
        C(i, j) = beta * C(i, j) + acc;
      }
    }
  );
}

template <class AMatrixType, class BMatrixType, class CMatrixType>
auto matrix_product_blocked(double alpha, AMatrixType const& A, BMatrixType const& B, double beta, CMatrixType& C, int blockSize) -> void {
  const int M = A.extent(0);
  const int N = B.extent(1);
  const int K = A.extent(1);

  Kokkos::parallel_for("dgemm_blocked", Kokkos::RangePolicy<>(0, M), KOKKOS_LAMBDA(int ii) {
    for (int jj = 0; jj < N; jj += blockSize) {
      for (int j = jj; j < jj + blockSize && j < N; ++j) {
        double acc = 0.0;
        for (int kk = 0; kk < K; kk += blockSize) {
          for (int k = kk; k < kk + blockSize && k < K; ++k) {
            acc += alpha * A(ii, k) * B(k, j);
          }
        }
        C(ii, j) = beta * C(ii, j) + acc;
      }
    }
  });
}



auto main(int argc, char* argv[]) -> int {
  if (argc < 5) {
    fmt::print("Usage: {} <M> <N> <K> <blockSize>\n", argv[0]);
    return -1;
  }
  int m = std::atoi(argv[1]);
  int n = std::atoi(argv[2]);
  int k = std::atoi(argv[3]);
  int blockSize=std::atoi(argv[4]); // Block size
  double flops;
  double flops_per_sec;


  // Known seed for deterministic RNG
  srand48(42);

  Kokkos::initialize(argc, argv);
  {
    auto A = Matrix("A", m, k);
    auto B = Matrix("B", k, n);
    auto C1 = Matrix("C1", m, n);  // For the original version
    auto C2 = Matrix("C2", m, n);  // For cache block version

    double alpha = drand48();
    matrix_init(A);
    matrix_init(B);
    double beta = drand48();
    Kokkos::deep_copy(C1, 0.0);
    Kokkos::deep_copy(C2, 0.0);
    Kokkos::fence();

    // Start the timer 
    auto start_normal = std::chrono::high_resolution_clock::now();

    matrix_product_normal(alpha, A, B, beta, C1);
    Kokkos::fence();

    auto end_normal = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed_normal = end_normal - start_normal;

    // Calculate FLOPs
    flops = 2.0 * m * n * k;
    flops_per_sec = flops / elapsed_normal.count();

    fmt::print("Elapsed time of normal version : {:.6f} seconds\n", elapsed_normal.count());
    fmt::print("Estimated FLOP/s of normal version : {:.2e}\n", flops_per_sec);
    

    // Start the timer
    auto start_cache_blocked = std::chrono::high_resolution_clock::now();

    matrix_product_blocked(alpha, A, B, beta, C2, blockSize);
    Kokkos::fence();

    auto end_cache_blocked = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed_cache_blocked = end_cache_blocked - start_cache_blocked;

    // Calculate FLOPs
    flops = 2.0 * m * n * k;
    flops_per_sec = flops / elapsed_cache_blocked.count();
 
    fmt::print("Elapsed time of cache-blocked version : {:.6f} seconds\n", elapsed_cache_blocked.count());
    fmt::print("Estimated FLOP/s of cache-blocked version : {:.2e}\n", flops_per_sec);

    fmt::print(">>> Now comparing C1 and C2...\n");

    // Compare the original and blocked versions to see if the results are consistent(<1e-10)
    double max_diff = 0.0;
    Kokkos::parallel_reduce("diff_check", Kokkos::RangePolicy<>(0, m * n),
      KOKKOS_LAMBDA(const int idx, double& local_max) {
        int i = idx / n;
        int j = idx % n;
        double diff = fabs(C1(i, j) - C2(i, j));
        if (diff > local_max) local_max = diff;
      }, Kokkos::Max<double>(max_diff)
    );
    Kokkos::fence();
    fmt::print("Maximum element-wise difference: {:.12f}\n", max_diff);
    
  }
  Kokkos::finalize();
  return 0;
}