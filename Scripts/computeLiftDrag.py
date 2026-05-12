import numpy as np
from scipy.signal import savgol_filter
from config import *

# -----------------------------------------------
# 1. Load and process position data
# -----------------------------------------------

# load time, x_position, and y_position data
data=np.genfromtxt(CSV_PATH,delimiter=",")


# turn selected column of data into an array
time=data[:,0]
xpositions=data[:,1]
ypositions=data[:,2]


# creates odd sized length of the filter window
# filter fluctuations in data, smooths noisy data while preserving shape

def computeLiftDrag(xpositions: np.ndarray, ypositions: np.ndarray, time: np.ndarray) -> dict:
    filterSize = min(51, len(time) // 5)  # must be odd
    if filterSize % 2 == 0:
        filterSize += 1

    xpositions = savgol_filter(xpositions, filterSize, 4)
    ypositions = savgol_filter(ypositions, filterSize, 4)
    dt = time[1] - time[0] # find step in time between data points

    # create velocity vectors from position data, take first derivative
    dxdt = np.gradient(xpositions, dt)
    dydt = np.gradient(ypositions, dt)


    filterSize=len(time)-1*((len(time)+1)%2) # creates odd sized length of the filter window

    # filter fluctuations in data, smooths noisy data while preserving shape


    dxdt = savgol_filter(dxdt, filterSize, 4)
    dydt = savgol_filter(dydt, filterSize, 4)

    # create acceleration vectors from velocity data, derivative of velocity
    d2xdt2=np.gradient(dxdt,dt)
    d2ydt2=np.gradient(dydt,dt)

    # filter acceleration data
    d2ydt2 = savgol_filter(d2ydt2, filterSize, 4)
    d2xdt2 = savgol_filter(d2xdt2, filterSize, 4)

    # -----------------------------------------------
    # 2. Compute velocity and acceleration data
    # -----------------------------------------------

    # create array to store unit vector of velocity/acceleration,
    # and create array to store magnitude of velocity/acceleration
    # unit vector stores direction

    unitVectorVelocity = []
    velocityMagnitude = []

    for Vx, Vy in zip(dxdt, dydt):
        magnitude = np.sqrt(Vx**2 + Vy**2)
        velocityMagnitude.append(magnitude)
        unitVectorVelocity.append([Vx, Vy]/magnitude) # unit vector: vector components/magnitude

    unitVectorAcc = []
    accMagnitude = []

    for Ax, Ay in zip(d2xdt2, d2ydt2):
        magnitude = np.sqrt(Ax**2 + Ay**2)
        accMagnitude.append(magnitude)
        unitVectorAcc.append([Ax/magnitude, Ay/magnitude])

    # unit vector perpendicular to velocity, direction of lift
    unitVectorNormal=[]
    for unitVector in unitVectorVelocity:
        unitVectorNormal.append([-unitVector[1],unitVector[0]]) # assumes plane is flying to the right



    # -----------------------------------------------
    # 3. Compute compenents of Lift, Drag, and Weight
    # -----------------------------------------------


    # computing how acceleration, velocity, and gravity project along the lift and drag directions of the airplane
    # Dot product is a measure how much two vectors point in the same direction
    cosLift = [] # how much acceleration points along the lift direction(a*n)
    cosDrag = [] # how much acceleration points along the opposite of velocity direction()
    cosWeightN = [] # gravity onto the normal direction
    cosWeightV = [] # gravity onto the velocity direction



    for normals, unitVelocity, unitAcc in zip(unitVectorNormal, unitVectorVelocity, unitVectorAcc):
        # normals: unit vector perpendicular to velocity, direction of lift
        # velocity normals: unit vector along velocity, direction of drag
        # acceleration normal: unit vector along net acceleration
        cosLift.append(np.dot(normals, unitAcc)) # cosine of angle between lift and acceleration normal
        cosDrag.append(np.dot(-unitVelocity, unitAcc)) # cosine of angle between drag and acceleration normal
        cosWeightN.append(np.dot(normals, [0, -1])) # gravity on lift force
        cosWeightV.append(np.dot(-unitVelocity, [0, -1])) # gravity on direction of drag force

    LiftForce = []
    DragForce = []

    for liftCosine, dragCosine, weightNCosine, weightVCosine, a in zip(cosLift, cosDrag, cosWeightN, cosWeightV,
                                                                       accMagnitude):
        # LiftForce = (component of net acceleration along lift) − (component of gravity along lift
        LiftForce.append(MASS * a * liftCosine - MASS * G * weightNCosine)
        # DragForce = (component of net acceleration along drag) − (component of gravity along drag)
        DragForce.append(MASS * a * dragCosine - MASS * G * weightVCosine)

    result ={"liftForce":LiftForce,
             "dragForce":DragForce,
             "velMagnitude": velocityMagnitude,
             "accMagnitude": accMagnitude,
             "dxdt":dxdt,
             "dydt":dydt,
             "d2ydt2":d2ydt2,
             "d2xdt2":d2xdt2,
             "xpositions":xpositions,
             "ypositions": ypositions,
             "time": time
             }

    return result


def printDragLift(dragForce: np.ndarray, liftForce: np.ndarray, velocityMagnitude:np.ndarray) -> None:
    c_D = round(np.average(dragForce[0:-10]/(1/2*RHO*(SURFACE_AREA)*np.power(velocityMagnitude[0:-10],2))), 3)
    c_L = round(np.average(liftForce[0:-10] / (0.5 * RHO * 0.01365 * np.power(velocityMagnitude[0:-10], 2))), 3)
    print("\n--- Flight Analysis Summary ---")
    print("Average Drag Coefficent:")
    print(c_D)
    print("Average Lift Coefficent:")
    print(c_L)
