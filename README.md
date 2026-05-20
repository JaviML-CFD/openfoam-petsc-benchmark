# Linear Solver Benchmarking: petscFoam vs. Native OpenFOAM

This repository contains a local numerical performance benchmark comparing native OpenFOAM linear solvers against the **PETSc library (`petscFoam`)** framework. Running locally on a consumer-grade laptop via WSL2, this study evaluates solver convergence rates, wall-clock execution speedups, and memory footprint across two standard test cases: **pitzDaily** (2D) and **motorbike** (3D).

For step-by-step instructions on compiling and linking the external solver binaries locally without altering core system paths, see the accompanying [PETSc & petscFoam Installation Guide](Install_guide_petscFoam.md).

## 📊 Benchmark Test Matrix

| Case | Domain Type | Purpose | Mesh Size | Solver |
| :--- | :--- | :--- | :--- | :--- |
| **pitzDaily** | 2D Backward-Facing Step | Rapid prototyping & stability verification of PETSc options. | ~12k cells | `simpleFoam` |
| **motorbike**| 3D External Aerodynamics | Execution speed & RAM utilization benchmark. | ~350k cells | `simpleFoam` |

### Solver Configurations Evaluated

1. **Baseline (FOAM-GAMG-PCG):** Native OpenFOAM configuration. Uses a Conjugate Gradient (PCG) solver accelerated by a Geometric-Algebraic Multigrid (GAMG) preconditioner for the pressure matrix, coupled with a standard PBiCGStab solver for momentum.
2. **PETSc Hypre (PETSC-AMG-CG):** Interface configuration routing the pressure system to PETSc. Employs a Conjugate Gradient (CG) solver preconditioned via Hypre's classic algebraic multigrid wrapper (`boomeramg`), evaluating the matrix transformation over Compressed Sparse Row (CSR) storage.
3. **PETSc Hypre + Caching (PETSC-AMG-CG + Caching):** Peak optimization run using identical linear algebra solver blocks as Config 2, but utilizing the `petscCacheManager` engine to lock down preconditioner coefficients inside system RAM. This bypasses the structural assembly phase (`PCSetUp = 0s`), skipping the translation overhead for convergent flow regimes.

## 💻 Environment & Hardware Profile
* **OS:** Ubuntu via WSL2
* **Hardware:** AMD Ryzen 7 5700U with Radeon Graphics | 16GB RAM
* **Software:** OpenFOAM-v2312+ 
* **PETSc Integration:** Dynamic runtime binding via the `external-solver` module (`petscFoam.so` compiled with `-prefix=user` against PETSc release branch)

## 📈 Extracted Performance Metrics
* **ClockTime per Iteration:** Real-world seconds elapsed per SIMPLE loop.
* **Residual Convergence Rate:** Number of iterations required to hit the $10^{-6}$ target.
* **Peak Memory Footprint:** Volumetric RAM usage difference between solver libraries.