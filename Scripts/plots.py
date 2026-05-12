import numpy as np
import matplotlib.pyplot as pltr
from matplotlib.gridspec import GridSpec


def plotMain(time, xpositions, ypositions, dxdt, dydt, d2xdt2, d2ydt2, LiftForce, DragForce):
    fig, axes = pltr.subplots(3, 2, figsize=(12, 12))
    axes = axes.flatten()  # Flatten 2D array to make indexing easier

    # Plot 1: X Position
    axes[0].plot(time, xpositions)
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("X Position (m)")
    axes[0].set_title("X Position vs Time")

    # Plot 2: Y Position
    axes[1].plot(time, ypositions)
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Y Position (m)")
    axes[1].set_title("Y Position vs Time")

    # Plot 3: X Velocity
    axes[2].plot(time, dxdt)
    axes[2].set_xlabel("Time (s)")
    axes[2].set_ylabel("X Velocity (m/s)")
    axes[2].set_title("X Velocity vs Time")

    # Plot 4: Y Velocity
    axes[3].plot(time, dydt)
    axes[3].set_xlabel("Time (s)")
    axes[3].set_ylabel("Y Velocity (m/s)")
    axes[3].set_title("Y Velocity vs Time")

    # Plot 5: X Acceleration
    axes[4].plot(time, d2xdt2)
    axes[4].set_xlabel("Time (s)")
    axes[4].set_ylabel("X Acceleration (m/s²)")
    axes[4].set_title("X Acceleration vs Time")

    # Plot 6: Y Acceleration
    axes[5].plot(time, d2ydt2)
    axes[5].set_xlabel("Time (s)")
    axes[5].set_ylabel("Y Acceleration (m/s²)")
    axes[5].set_title("Y Acceleration vs Time")

    for ax in axes:
        ax.grid(True, linestyle='--', alpha=0.6)
    pltr.style.use('seaborn-v0_8-darkgrid')
    fig.tight_layout()


    pltr.figure()
    pltr.plot(time, LiftForce, label='Lift Force')
    pltr.plot(time, DragForce, label='Drag Force')
    pltr.xlabel('Time (s)')
    pltr.ylabel('Force (N)')
    pltr.title('Lift vs Drag Forces Over Time')
    pltr.legend()
    pltr.grid(True)
    pltr.tight_layout()
    pltr.savefig("../Figures/LiftVsTime.png", dpi=300)
    fig.savefig("../Figures/PlaneDynamics_AllPlots.png", dpi=300)

    pltr.show()


def plot_polar(polar_data, label="Dart 1", save=False):
    """
    Generate a 4-panel aerodynamic polar figure

    Graphs:
    1. CL  vs. Angle of Attack
    2. CD  vs. Angle of Attack
    3. CL  vs. CD  (the classical polar diagram)
    4. L/D vs. Angle of Attack  (efficiency curve)
    """
    aoa  = polar_data["aoa_trim"]
    CL   = polar_data["CL_trim"]
    CD   = polar_data["CD_trim"]
    LD   = polar_data["LD_trim"]

    # find the peak L/D point for annotation
    valid = ~np.isnan(LD)
    if valid.any():
        idx_best = np.nanargmax(LD[valid])
        best_aoa = aoa[valid][idx_best]
        best_LD  = LD[valid][idx_best]
        best_CL  = CL[valid][idx_best]
        best_CD  = CD[valid][idx_best]
    else:
        best_aoa = best_LD = best_CL = best_CD = None

    fig = pltr.figure(figsize=(13, 10))
    fig.suptitle("Aerodynamic Polar Analysis", fontsize=15, fontweight='bold', y=0.98) # can add in label
    gs = GridSpec(2, 2, figure=fig, hspace=0.38, wspace=0.32)

    # Graph 1: CL vs AoA
    ax1 = fig.add_subplot(gs[0, 0])
    sc1 = ax1.scatter(aoa, CL, c=aoa, cmap='plasma', s=12, alpha=0.7, zorder=3)
    ax1.axhline(0, color='k', linewidth=0.7, linestyle='--', alpha=0.4)
    ax1.axvline(0, color='k', linewidth=0.7, linestyle='--', alpha=0.4)
    ax1.set_xlabel("Angle of Attack (°)", fontsize=11)
    ax1.set_ylabel("Lift Coefficient  $C_L$", fontsize=11)
    ax1.set_title("$C_L$ vs. Angle of Attack", fontsize=12)
    ax1.grid(True, linestyle='--', alpha=0.4)
    pltr.colorbar(sc1, ax=ax1, label='AoA (°)', pad=0.02)

    # Graph 2: CD vs AoA
    ax2 = fig.add_subplot(gs[0, 1])
    sc2 = ax2.scatter(aoa, CD, c=aoa, cmap='viridis', s=12, alpha=0.7, zorder=3)
    ax2.axhline(0, color='k', linewidth=0.7, linestyle='--', alpha=0.4)
    ax2.axvline(0, color='k', linewidth=0.7, linestyle='--', alpha=0.4)
    ax2.set_xlabel("Angle of Attack (°)", fontsize=11)
    ax2.set_ylabel("Drag Coefficient  $C_D$", fontsize=11)
    ax2.set_title("$C_D$ vs. Angle of Attack", fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.4)
    pltr.colorbar(sc2, ax=ax2, label='AoA (°)', pad=0.02)

    # Graph 3: CL vs CD (polar diagram)
    ax3 = fig.add_subplot(gs[1, 0])
    # Color code by AoA so you can read the progression
    sc3 = ax3.scatter(CD, CL, c=aoa, cmap='coolwarm', s=12, alpha=0.7, zorder=3)
    if best_CL is not None:
        ax3.scatter(best_CD, best_CL, color='gold', s=80, zorder=5,
                    edgecolors='black', linewidths=0.8, label=f"Peak L/D = {best_LD:.1f}")
        # draw a tangent line from origin to best L/D point (slope = CL/CD = L/D)
        x_line = np.array([0, best_CD * 1.5])
        ax3.plot(x_line, (best_LD) * x_line, 'k--', linewidth=1, alpha=0.6, label='Best glide slope')
        ax3.legend(fontsize=9, loc='upper left')
    ax3.set_xlabel("Drag Coefficient  $C_D$", fontsize=11)
    ax3.set_ylabel("Lift Coefficient  $C_L$", fontsize=11)
    ax3.set_title("Polar Diagram  ($C_L$ vs. $C_D$)", fontsize=12)
    ax3.grid(True, linestyle='--', alpha=0.4)
    pltr.colorbar(sc3, ax=ax3, label='AoA (°)', pad=0.02)

    # Graph 4: L/D vs AoA
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(aoa[valid], LD[valid], color='steelblue', linewidth=1.4, alpha=0.8)
    ax4.scatter(aoa[valid], LD[valid], c=aoa[valid], cmap='plasma', s=10, alpha=0.6, zorder=3)
    if best_aoa is not None:
        ax4.axvline(best_aoa, color='gold', linestyle='--', linewidth=1.2,
                    label=f"Peak at AoA = {best_aoa:.1f}°\nL/D = {best_LD:.1f}")
        ax4.legend(fontsize=9, loc='upper right')
    ax4.axhline(0, color='k', linewidth=0.7, linestyle='--', alpha=0.4)
    ax4.set_xlabel("Angle of Attack (°)", fontsize=11)
    ax4.set_ylabel("Lift-to-Drag Ratio  $L/D$", fontsize=11)
    ax4.set_title("Aerodynamic Efficiency  ($L/D$)", fontsize=12)
    ax4.grid(True, linestyle='--', alpha=0.4)

    # Summary stats box
    stats = (
        f"Avg $C_L$ = {np.nanmean(CL):.3f}\n"
        f"Avg $C_D$ = {np.nanmean(CD):.3f}\n"
        f"Avg $L/D$ = {np.nanmean(LD[valid]):.2f}\n"
        f"Peak $L/D$ = {best_LD:.2f} @ {best_aoa:.1f}°"
        if best_LD is not None else ""
    )
    fig.text(0.5, 0.01, stats, ha='center', fontsize=10,
             bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.8))

    if save:
        fig.savefig("../Figures/PolarAnalysis.png", dpi=300, bbox_inches='tight')
        print("Saved: Figures/PolarAnalysis.png")

    pltr.show()