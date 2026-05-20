import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('pdf')
import numpy as np

# Load exact arrays preserved by the bash script wrapper
time_baseline = np.loadtxt('logs_baseline/executionTime_0')
time_petsc = np.loadtxt('logs_petsc/executionTime_0')
ram_baseline = np.loadtxt('logs_baseline/ram_usage_0')
ram_petsc = np.loadtxt('logs_petsc/ram_usage_0')

# Joint Clock-Time Comparison Plot
plt.figure(figsize=(7, 5))
plt.plot(time_baseline[:,0], time_baseline[:,1], label='Native OpenFOAM (GAMG)', color='#1e3a5c', linewidth=1.2)
plt.plot(time_petsc[:,0], time_petsc[:,1], label='PETSc (Hypre BoomerAMG)', color='#b22222', linewidth=1.2)
plt.title('Solver Computational Throughput (Time Comparison)')
plt.xlabel('SIMPLE Iteration Step')
plt.ylabel('Cumulative Wall-Clock Time [s]')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.savefig('FIGS/joint_execution_time.png', dpi=200, bbox_inches='tight')
plt.close()

# Joint RAM Allocation Comparison Plot
plt.figure(figsize=(7, 5))
plt.plot(ram_baseline[:,0], ram_baseline[:,1], label='Native LDU Storage', color='#1e3a5c', linestyle='--')
plt.plot(ram_petsc[:,0], ram_petsc[:,1], label='PETSc CSR Allocation', color='#2e7d32', linewidth=1.2)
plt.title('Dynamic System RAM Allocation Profile')
plt.xlabel('SIMPLE Iteration Step')
plt.ylabel('Memory Consumption [GB]')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.savefig('FIGS/joint_ram_allocation.png', dpi=200, bbox_inches='tight')
plt.close()