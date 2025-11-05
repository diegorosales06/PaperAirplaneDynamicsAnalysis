

# animations.py
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def animate_trajectory(time, xpositions, ypositions, dxdt, dydt, LiftForce, DragForce):
    x = xpositions
    y = ypositions

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x, y, color='gray', linewidth=1, alpha=0.5)
    ax.set_xlim(min(xpositions) - 0.1, max(xpositions) + 0.3)
    ax.set_ylim(min(ypositions) - 0.1, max(ypositions) + 0.3)
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title("Flight Animation")
    legend_handles = [
        plt.Line2D([0], [0], color='blue', lw=2, label='Velocity'),
        plt.Line2D([0], [0], color='green', lw=2, label='Lift'),
        plt.Line2D([0], [0], color='red', lw=2, label='Drag')
    ]
    ax.legend(handles=legend_handles, loc="upper right")

    point, = ax.plot([], [], 'ro', markersize=6)
    vel_arrow = ax.arrow(0, 0, 0, 0, color='blue', head_width=0.02)
    lift_arrow = ax.arrow(0, 0, 0, 0, color='green', head_width=0.02)
    drag_arrow = ax.arrow(0, 0, 0, 0, color='red', head_width=0.02)
    time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=10)

    def init():
        point.set_data([], [])
        return point, vel_arrow, lift_arrow, drag_arrow, time_text

    def update(frame):
        nonlocal vel_arrow, lift_arrow, drag_arrow
        for a in [vel_arrow, lift_arrow, drag_arrow]:
            a.remove()

        px, py = x[frame], y[frame]
        vx, vy = dxdt[frame], dydt[frame]
        v_mag = np.sqrt(vx**2 + vy**2)
        v_hat = np.array([vx/v_mag, vy/v_mag]) if v_mag != 0 else np.array([0, 0])
        n_hat = np.array([-v_hat[1], v_hat[0]])

        v_scale = 0.1
        f_scale = 1 / np.max(np.abs([LiftForce, DragForce]))

        vel_arrow = ax.arrow(px, py, v_scale * vx, v_scale * vy, color='blue', head_width=0.02)
        lift_arrow = ax.arrow(px, py, f_scale * LiftForce[frame] * n_hat[0],
                              f_scale * LiftForce[frame] * n_hat[1], color='green', head_width=0.02)
        drag_arrow = ax.arrow(px, py, -f_scale * DragForce[frame] * v_hat[0],
                              -f_scale * DragForce[frame] * v_hat[1], color='red', head_width=0.02)

        point.set_data(px, py)
        time_text.set_text(f"t = {time[frame]:.2f}s")

        return point, vel_arrow, lift_arrow, drag_arrow, time_text

    ani = FuncAnimation(fig, update, frames=len(time), init_func=init,
                        interval=100, blit=False, repeat=True)

    plt.tight_layout()
    plt.show()
