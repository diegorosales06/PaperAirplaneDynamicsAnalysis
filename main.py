# main.py
from data_processing import time, xpositions, ypositions, dxdt, dydt, d2xdt2, d2ydt2, LiftForce, DragForce
from plots import plot_all
from animations import animate_trajectory


if __name__ == "__main__":
    #plot_all(time, xpositions, ypositions, dxdt, dydt, d2xdt2, d2ydt2, LiftForce, DragForce)
    animate_trajectory(time, xpositions, ypositions, dxdt, dydt, LiftForce, DragForce)

