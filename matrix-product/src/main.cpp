#include <cassert>
#include <cstdlib>
#include <chrono>
#include <cmath>

#include <Kokkos_Core.hpp>
#include <fmt/core.h>

/*using MatrixA = Kokkos::View<double**, Kokkos::LayoutRight>;
using MatrixB = Kokkos::View<double**, Kokkos::LayoutRight>;  
using MatrixC = Kokkos::View<double**, Kokkos::LayoutRight>;*/

using MatrixA = Kokkos::View<double**, Kokkos::LayoutLeft>;
using MatrixB = Kokkos::View<double**, Kokkos::LayoutLeft>;  
using MatrixC = Kokkos::View<double**, Kokkos::LayoutLeft>;

template <class MatrixType>
auto matrix_init(MatrixType &M) -> void
{
  static_assert(2 == MatrixType::rank(), "View must be of rank 2");

  Kokkos::parallel_for(
      "init",
      M.extent(0),
      KOKKOS_LAMBDA(int i) {
        for (int j = 0; j < int(M.extent(1)); ++j)
        {
          M(i, j) = drand48();
        }
      });
}

template <class AMatrixType, class BMatrixType, class CMatrixType>
auto matrix_product_normal(double alpha, AMatrixType const &A, BMatrixType const &B, double beta, CMatrixType &C) -> void
{
  static_assert(
      AMatrixType::rank() == 2 && BMatrixType::rank() == 2 && CMatrixType::rank() == 2, "Views must be of rank 2");
  assert(A.extent(0) == C.extent(0));
  assert(B.extent(1) == C.extent(1));
  assert(A.extent(1) == B.extent(0));

  const int M = A.extent(0);
  const int N = B.extent(1);
  const int K = A.extent(1);

  // Automatically determine the traversal method based on the layout type of the output matrix
  using Layout = typename CMatrixType::array_layout;

  if constexpr (std::is_same_v<Layout, Kokkos::LayoutLeft>)
  {
    // Column-major layout (LayoutLeft): outer layer j, inner layer i (column-first traversal)
    using policy = Kokkos::TeamPolicy<>;
    using member_type = policy::member_type;

    Kokkos::parallel_for(
        "dgemm_kernel_column_major_team",
        policy(N, Kokkos::AUTO),
        KOKKOS_LAMBDA(const member_type& team) {
          const int j = team.league_rank();
          Kokkos::parallel_for(
            Kokkos::TeamThreadRange(team, M), [&](int i) {
              double acc = 0.0;
              for (int k = 0; k < K; ++k) {
                acc += alpha * A(i, k) * B(k, j);
              }
              C(i, j) *= beta + acc;
            });
        });
  }
  else
  {
    // Row-based layout (LayoutRight): outer layer i, inner layer j (row-based traversal)
    using policy = Kokkos::TeamPolicy<>;
    using member_type = policy::member_type;

    Kokkos::parallel_for(
        "dgemm_kernel_row_major_team",
        policy(M, Kokkos::AUTO),
        KOKKOS_LAMBDA(const member_type& team) {
          const int i = team.league_rank();
          Kokkos::parallel_for(
            Kokkos::TeamThreadRange(team, N), [&](int j) {
              double acc = 0.0;
              for (int k = 0; k < K; ++k) {
                acc += alpha * A(i, k) * B(k, j);
              }
              C(i, j) *= beta + acc;
            });
        });
  }
}

template <class AMatrixType, class BMatrixType, class CMatrixType>
auto matrix_product_blocked(double alpha, AMatrixType const& A, BMatrixType const& B,
                            double beta, CMatrixType& C, int blockSize) -> void {
  const int M = A.extent(0);
  const int N = B.extent(1);
  const int K = A.extent(1);

  using Layout = typename CMatrixType::array_layout;

  if constexpr (std::is_same_v<Layout, Kokkos::LayoutLeft>) {
    // LayoutLeft: outer layer j, inner layer i, column priority
    Kokkos::parallel_for("blocked_column_major", Kokkos::RangePolicy<>(0, N), KOKKOS_LAMBDA(int jj) {
      for (int ii = 0; ii < M; ii += blockSize) {
        for (int j = jj; j < jj + 1 && j < N; ++j) {
          for (int i = ii; i < ii + blockSize && i < M; ++i) {
            double acc = 0.0;
            for (int kk = 0; kk < K; kk += blockSize) {
              for (int k = kk; k < kk + blockSize && k < K; ++k) {
                acc += alpha * A(i, k) * B(k, j);
              }
            }
            C(i, j) *= beta + acc;
          }
        }
      }
    });
  } else {
    // LayoutRight: outer layer i, inner layer j, row priority order
    Kokkos::parallel_for("blocked_row_major", Kokkos::RangePolicy<>(0, M), KOKKOS_LAMBDA(int ii) {
      for (int jj = 0; jj < N; jj += blockSize) {
        for (int i = ii; i < ii + 1 && i < M; ++i) {
          for (int j = jj; j < jj + blockSize && j < N; ++j) {
            double acc = 0.0;
            for (int kk = 0; kk < K; kk += blockSize) {
              for (int k = kk; k < kk + blockSize && k < K; ++k) {
                acc += alpha * A(i, k) * B(k, j);
              }
            }
            C(i, j) *= beta + acc;
          }
        }
      }
    });
  }
}

auto main(int argc, char *argv[]) -> int
{
  if (argc < 5)
  {
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
    auto A = MatrixA("A", m, k);
    auto B = MatrixB("B", k, n);
    auto C1 = MatrixC("C1", m, n); // For the original version
    auto C2 = MatrixC("C2", m, n);  // For cache block version

    double alpha = drand48();
    matrix_init(A);
    matrix_init(B);
    double beta = drand48();
    matrix_init(C1);
    matrix_init(C2);
    Kokkos::fence();

    // When running the cache blocking version, comment out this part of the code from the normal version
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
  }
  Kokkos::finalize();
  return 0;
}