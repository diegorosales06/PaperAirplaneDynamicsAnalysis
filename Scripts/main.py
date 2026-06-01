
from computeLiftDrag import *
from plots import plotMain, plot_polar
from animations import animate_trajectory
from computePolar import computePolarData, printPolarSummary


if __name__ == "__main__":
    # Static kinematics and force plots
    values = computeLiftDrag(xpositions, ypositions, time)
    plotMain(values["time"], values["xpositions"], values["ypositions"], values["dxdt"],
             values["dydt"], values["d2xdt2"], values["d2ydt2"], values["liftForce"], values["dragForce"])

    printDragLift(values["dragForce"], values["dragForce"], values["velMagnitude"])
    # Flight animation with live force vectors
    # animate_trajectory(time, xpositions, ypositions, dxdt, dydt, LiftForce, DragForce)

    # Aerodynamic polar analysis
    polarData = computePolarData(values["velMagnitude"], values["liftForce"], values["dragForce"], values["dxdt"], values["dydt"])
    printPolarSummary(polarData, label="Dart 1")
    # plot_polar(polarData, label="Dart 1", save=True)