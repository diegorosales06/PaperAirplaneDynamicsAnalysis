import numpy as np
import matplotlib.pyplot as plotter
from scipy.signal import savgol_filter

# load time, x_position, and y_position data
data=np.genfromtxt("/Users/diegorosales/PycharmProjects/PaperAirplaneDynamicsAnalysis/PlaneData.csv",delimiter=",")


# turn selected column of data into an array
time=data[:,0]
xpositions=data[:,1]
ypositions=data[:,2]

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
velocityAcc = []
for Ax, Ay in zip(d2xdt2, d2ydt2):
    magnitude = np.sqrt(Ax ** 2 + Ay ** 2)
    velocityMagnitude.append(magnitude)
    unitVectorVelocity.append([Ax, Ay]/magnitude)

# find normal vector of velocity
unitVectorNormal=[]
for unitVector in unitVectorVelocity:
    unitVectorNormal.append([-unitVector[1],unitVector[0]])

# X Velocity
plotter.figure()
plotter.plot(time, dxdt)
plotter.xlabel("Time (s)")
plotter.ylabel("X Velocity (m/s)")
plotter.title("X Velocity vs Time")

# Y Velocity
plotter.figure()
plotter.plot(time, dydt)
plotter.xlabel("Time (s)")
plotter.ylabel("Y Velocity (m/s)")
plotter.title("Y Velocity vs Time")

plotter.show()

