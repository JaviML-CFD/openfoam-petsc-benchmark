# High-Performance PETSc & OpenFOAM Module Installation Guide

This guide details the steps to build and link a highly optimized version of **PETSc** (including **Hypre**) with an existing **OpenFOAM** installation without needing to recompile the core OpenFOAM directories.

---

## Prerequisites

### 1. Install System Linear Algebra Dependencies

Install Ubuntu's optimized BLAS and LAPACK development libraries:

```bash
sudo apt update
sudo apt install -y libblas-dev liblapack-dev
```

### 2. Clone the External Solver Module and PETSc

```bash
# Step into your OpenFOAM directory
cd ~/OpenFOAM

# Clone the OpenFOAM external solver module
git clone https://develop.openfoam.com/modules/external-solver.git

# Create ThirdParty directory and clone PETSc stable release
mkdir -p ThirdParty
cd ThirdParty
git clone -b release https://gitlab.com/petsc/petsc.git petsc
cd petsc
```

---

## Installation Steps

### Step 1: Configure PETSc

Source your OpenFOAM environment first to expose MPI compiler wrappers, then configure PETSc with optimisation flags and Hypre:

```bash
source /usr/lib/openfoam/openfoam2312/etc/bashrc

./configure --with-debugging=0 \
  COPTFLAGS="-O3 -march=native" \
  CXXOPTFLAGS="-O3 -march=native" \
  FOPTFLAGS="-O3 -march=native" \
  --download-hypre=1 \
  --download-fblaslapack=1 \
  --with-precision=double \
  --with-clanguage=C
```

### Step 2: Build and Compile PETSc

Run the exact `make` commands printed at the bottom of your configure output. They will closely mirror something like :

```bash
# Compile (takes 5–15 minutes depending on CPU)
make PETSC_DIR=$HOME/OpenFOAM/ThirdParty/petsc PETSC_ARCH=arch-linux-c-opt all

# Verify the build is healthy
make PETSC_DIR=$HOME/OpenFOAM/ThirdParty/petsc PETSC_ARCH=arch-linux-c-opt check
```

### Step 3: Set Environment Variables in `~/.bashrc`

Open your shell config:

```bash
nano ~/.bashrc
```

Add the following **after** the OpenFOAM source line:

```bash
# OpenFOAM (must come first)
source /usr/lib/openfoam/openfoam2312/etc/bashrc

# PETSc
export PETSC_DIR=$HOME/OpenFOAM/ThirdParty/petsc
export PETSC_ARCH=arch-linux-c-opt
export PETSC_ARCH_PATH=$PETSC_DIR          # point to root, not arch subfolder
export LD_LIBRARY_PATH=$PETSC_DIR/$PETSC_ARCH/lib:$LD_LIBRARY_PATH
# eval $(foamEtcFile -sh -config petsc -- -force) only if needed
```

> **Note:** `PETSC_ARCH_PATH` must point to `$PETSC_DIR` (the root), **not** `$PETSC_DIR/$PETSC_ARCH`. The `petsc.h` header lives in `$PETSC_DIR/include/`, and the build scripts look for it relative to `PETSC_ARCH_PATH`.

Press `Ctrl+O` then `Enter` to save, and `Ctrl+X` to exit nano.

### Step 4: Build the OpenFOAM–PETSc Interface Module

```bash
source ~/.bashrc

cd ~/OpenFOAM/external-solver

# Use -prefix=user to install into your user directory (avoids permission errors)
./Allwmake -prefix=user
```

> **Important:** Use `-prefix=user`, **not** `-prefix=openfoam`. The `openfoam` prefix targets the system-wide OpenFOAM directory (`/usr/lib/openfoam/...`) which requires root access and will fail with a permission denied error during linking.

---

## Verification

Once the build completes, confirm OpenFOAM can load the library:

```bash
foamHasLibrary -verbose petscFoam
```

Expected output:

```
Can load "petscFoam"
```

---

## Using PETSc Solvers in a Case

Add to `system/controlDict`:

```c++
libs (petscFoam);
```

Configure a solver in `system/fvSolution`:

```c++
solvers
{
    p
    {
        solver          petsc;
        preconditioner  petsc;
        tolerance       1e-6;
        relTol          0.01;

        petsc
        {
            options
            {
                ksp_type    cg;
                pc_type     bjacobi;
                sub_pc_type icc;
            }

            caching
            {
                matrix
                {
                    update always;
                }

                preconditioner
                {
                    update always;
                }
            }
        }
    }
}
```

To use Hypre as the preconditioner, replace the `options` block with:

```c++
options
{
    ksp_type  cg;
    pc_type   hypre;
    pc_hypre_type boomeramg;
}
```