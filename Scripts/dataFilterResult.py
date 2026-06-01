import numpy as np
from scipy.signal import savgol_filter
from config import *


data = np.genfromtxt(CSV_PATH, delimiter=",")

# Extract columns
time = data[:, 0]
xpositions = data[:, 1]
ypositions = data[:, 2]

# filterSize = min(51, len(time) // 5)  # must be odd
# if filterSize % 2 == 0:
#     filterSize += 1
# xpositions = savgol_filter(xpositions, filterSize, 4)
# ypositions = savgol_filter(ypositions, filterSize, 4)


dt = time[1] - time[0]

# VELOCITYYY


# differentiation for velocity
dxdt_raw = np.gradient(xpositions, dt)
dydt_raw = np.gradient(ypositions, dt)

# choose filter size (must be odd)
filterSize = min(51, len(time) // 5)

if filterSize % 2 == 0:
    filterSize += 1

if filterSize <= 4:
    filterSize = 5

# filter velocity
dxdt_filtered = savgol_filter(dxdt_raw, filterSize, 4)
dydt_filtered = savgol_filter(dydt_raw, filterSize, 4)

# velocity noise measurements
velocity_noise_before = np.std(dxdt_raw)
velocity_noise_after = np.std(dxdt_filtered)

velocity_noise_reduction = (
    1 - (velocity_noise_after / velocity_noise_before)
) * 100

# RMS difference for velocity
velocity_rms_x = np.sqrt(
    np.mean((dxdt_raw - dxdt_filtered) ** 2)
)

velocity_rms_y = np.sqrt(
    np.mean((dydt_raw - dydt_filtered) ** 2)
)

# accelerationnnnnn

# differentiation for acceleration
ax_raw = np.gradient(dxdt_raw, dt)
ay_raw = np.gradient(dydt_raw, dt)

# filter for acceleration
ax_filtered = savgol_filter(ax_raw, filterSize, 4)
ay_filtered = savgol_filter(ay_raw, filterSize, 4)

# Acceleration noise
acceleration_noise_before = np.std(ax_raw)
acceleration_noise_after = np.std(ax_filtered)

acceleration_noise_reduction = (
    1 - (acceleration_noise_after / acceleration_noise_before)
) * 100

# RMS difference
acceleration_rms_x = np.sqrt(
    np.mean((ax_raw - ax_filtered) ** 2)
)

acceleration_rms_y = np.sqrt(
    np.mean((ay_raw - ay_filtered) ** 2)
)




print("VELOCITY ANALYSIS")
print(f"Noise Before: {velocity_noise_before}")
print(f"Noise After: {velocity_noise_after}")
print(f"Noise Reduction: {velocity_noise_reduction:.2f}%")
print(f"RMS Difference X Velocity: {velocity_rms_x}")
print(f"RMS Difference Y Velocity: {velocity_rms_y}")

print("\nACCELERATION ANALYSIS")
print(f"Noise Before: {acceleration_noise_before}")
print(f"Noise After: {acceleration_noise_after}")
print(f"Noise Reduction: {acceleration_noise_reduction:.2f}%")
print(f"RMS Difference X Acceleration: {acceleration_rms_x}")
print(f"RMS Difference Y Acceleration: {acceleration_rms_y}")

