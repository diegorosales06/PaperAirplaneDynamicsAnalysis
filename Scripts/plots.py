import numpy as np
import matplotlib.pyplot as plotter

def plot_all(time, xpositions, ypositions, dxdt, dydt, d2xdt2, d2ydt2, LiftForce, DragForce):
    fig, axes = plotter.subplots(3, 2, figsize=(12, 12))
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
    plotter.style.use('seaborn-v0_8-darkgrid')
    fig.tight_layout()


    plotter.figure()
    plotter.plot(time, LiftForce, label='Lift Force')
    plotter.plot(time, DragForce, label='Drag Force')
    plotter.xlabel('Time (s)')
    plotter.ylabel('Force (N)')
    plotter.title('Lift vs Drag Forces Over Time')
    plotter.legend()
    plotter.grid(True)
    plotter.tight_layout()
    plotter.savefig("LiftVsTime.png", dpi=300)
    fig.savefig("PlaneDynamics_AllPlots.png", dpi=300)

    plotter.show()