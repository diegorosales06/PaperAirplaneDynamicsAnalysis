import numpy as np
from config import *


def computePolarData(velocityMagnitude: np.ndarray, LiftForce: np.ndarray, DragForce: np.ndarray, dxdt: np.ndarray, dydt: np.ndarray, trim_tail=10) -> dict:
    """
    Compute angle of attack, CL, CD, and L/D ratio for each timestep.

    Parameters:
    velocityMagnitude : list or array
        Speed |v| at each timestep (m/s).
    LiftForce : list or array
        Lift force magnitude at each timestep (N).
    DragForce : list or array
        Drag force magnitude at each timestep (N).
    dxdt : array
        x-component of velocity at each timestep (m/s).
    dydt : array
        y-component of velocity at each timestep (m/s).
    trim_tail : int
        Number of noisy tail-end points to exclude from averages.

    Returns
    -------
    dict with keys: aoa_deg, CL, CD, LD, aoa_trim, CL_trim, CD_trim, LD_trim
    """
    v_mag = np.array(velocityMagnitude)
    dragForce = np.array(DragForce)
    liftForce = np.array(LiftForce)

    # dyncamic pressure at each timestep
    # q = (1/2)*(pressure)*(V)^2
    q = 0.5 * RHO * v_mag**2

    # Aerodynamic coefficients
    CL = liftForce / (q * SURFACE_AREA)
    CD = dragForce / (q * AREA)

    # print(type(CL)) -> numpy.ndarray

    # lift-to-drag ratio
    # LD = L/D ratio
    with np.errstate(divide='ignore', invalid='ignore'):
        LD = np.where(np.abs(dragForce) > 1e-6, liftForce / dragForce, np.nan)


    # Angle of attack is the angle of velocity vector below/above horizontal
    # Angle of attack = arctan(vy / vx) — positive when climbing, negative when descending
    aoa_rad = np.arctan2(np.array(dydt), np.array(dxdt))
    aoa_deg = np.degrees(aoa_rad)

    # Trim data, exclude the noisy endpoints by trim_tail
    trim = slice(0, -trim_tail)
    return {
        "aoa_deg":  aoa_deg,
        "CL":       CL,
        "CD":       CD,
        "LD":       LD,
        "aoa_trim": aoa_deg[trim],
        "CL_trim":  CL[trim],
        "CD_trim":  CD[trim],
        "LD_trim":  LD[trim],
    }

def printPolarSummary(polarData, label="Dart 1") -> None:
    CL   = polarData["CL_trim"]
    CD   = polarData["CD_trim"]
    LD   = polarData["LD_trim"]
    aoa  = polarData["aoa_trim"]

    print("\nPolar Analysis Summary:")
    print(f"  AoA range       : {aoa.min():.1f}° to {aoa.max():.1f}°")
    print(f"  Avg C_L         : {np.nanmean(CL):.4f}")
    print(f"  Avg C_D         : {np.nanmean(CD):.4f}")
    print(f"  Avg L/D         : {np.nanmean(LD):.3f}")