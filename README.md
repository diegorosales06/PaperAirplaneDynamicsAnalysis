# Paper Airplane Dynamics Analysis

A Python-based experimental aerodynamics study that extracts lift and drag forces, and their coefficients, from raw position tracking data of a paper airplane in flight.

---

## Overview

This project uses video tracked 2D position data (x, y vs. time) from a paper airplane throw to reconstruct the full flight kinematics and compute aerodynamic forces. The result is an experimental measurement of **lift coefficient (C_L)** and **drag coefficient (C_D)** for the specific paper airplane design, along with animated and static visualizations of the flight.

---

## Physics Derivation

### Forces Acting on a Paper Airplane

At any moment in flight, three forces act on the plane:

1. **Gravity** — straight down: **F_g** = m**g**, where **g** = (0, −9.81) m/s²
2. **Drag** — opposing the direction of motion: **F_D** = −½ C_D A ρ |**v**|² **v̂**
3. **Lift** — perpendicular to the direction of motion: **F_L** = ½ C_L S ρ |**v**|² **n̂**

where:
- ρ = 1.225 kg/m³ (air density at sea level)
- A = wing area for drag (m²)
- S = wing area for lift (m²)
- **v̂** = unit vector in the direction of velocity
- **n̂** = unit vector perpendicular to velocity (pointing toward the "top" of the plane)

By Newton's second law, the net force equals mass times acceleration:

```
m·a = F_g + F_D + F_L
```

### Step 1 — Extract Kinematics from Position Data

Position data (x(t), y(t)) is loaded from CSV and smoothed using a **Savitzky-Golay filter**, which suppresses measurement noise while preserving the physical shape of the trajectory.

Velocity components are obtained by numerical differentiation:

```
vx = dx/dt,   vy = dy/dt
```

Acceleration components are obtained by differentiating velocity:

```
ax = d²x/dt²,   ay = d²y/dt²
```

Both passes are filtered again to suppress noise amplification from numerical differentiation.

### Step 2 — Construct Unit Vectors

The **velocity unit vector** (direction of drag):

```
v̂ = (vx, vy) / |v|
```

The **normal unit vector** (direction of lift, perpendicular to velocity):

```
n̂ = (−vy, vx) / |v|
```

This choice of **n̂** places it 90° counterclockwise from **v̂**, pointing toward the "top" of the plane when flying right-side up. (If the plane is inverted, the computed lift coefficient will be negative, which is physically meaningful.)

The **acceleration unit vector**:

```
â = (ax, ay) / |a|
```

### Step 3 — Project Forces Along Lift and Drag Directions

The net force equation m**a** = **F_g** + **F_L** + **F_D** is projected along two orthogonal directions to isolate each aerodynamic force.

#### Projection along **n̂** (lift direction):

```
m · |a| · (â · n̂) = F_L + m·g · (ĝ · n̂)
```

Solving for lift:

```
F_L = m · |a| · cos(θ_L) − m·g · cos(θ_wN)
```

where:
- `cos(θ_L)` = `â · n̂` — how much of the net acceleration points along the lift direction
- `cos(θ_wN)` = `(0,−1) · n̂` — how much gravity projects along the lift direction

#### Projection along **−v̂** (drag direction, opposite to motion):

```
m · |a| · (â · (−v̂)) = F_D + m·g · (ĝ · (−v̂))
```

Solving for drag:

```
F_D = m · |a| · cos(θ_D) − m·g · cos(θ_wV)
```

where:
- `cos(θ_D)` = `â · (−v̂)` — how much of the net acceleration opposes motion (drag direction)
- `cos(θ_wV)` = `(0,−1) · (−v̂)` — how much gravity projects along the drag direction

This decomposition correctly isolates each aerodynamic force independently, regardless of flight orientation.

### Step 4 — Compute Aerodynamic Coefficients

Once lift and drag forces are known at every timestep, the coefficients follow from the standard aerodynamic force equations:

**Drag coefficient:**

```
C_D = F_D / (½ · ρ · A · |v|²)
```

**Lift coefficient:**

```
C_L = F_L / (½ · ρ · S · |v|²)
```

Average values are computed over the flight, excluding the noisy final frames (last 10 data points).

---

## Project Structure

```
PaperAirplaneDynamicsAnalysis/
├── main.py              # Entry point — runs plots or animation
├── config.py            # Physical constants and file path
├── data_processing.py   # Kinematics extraction + force computation
├── plots.py             # Static matplotlib figures (6-panel + lift/drag)
├── animations.py        # Animated trajectory with force vectors
├── PlaneData/
│   └── Dart1Data.csv    # Raw position tracking data (time, x, y)
└── Figures/             # Output plots
```

---

## Configuration

All physical parameters are set in `config.py`:

| Parameter | Value | Description |
|-----------|-------|-------------|
| `RHO`     | 1.225 kg/m³ | Air density at sea level |
| `MASS`    | 0.0048 kg | Paper airplane mass |
| `AREA`    | 0.01365 m² | Wing reference area |
| `G`       | 9.81 m/s² | Gravitational acceleration |

---

## Usage

```bash
pip install numpy scipy matplotlib
python main.py
```

Toggle between the static plots and animation in `main.py` by commenting/uncommenting:

```python
plot_all(...)           # 6-panel kinematics + lift/drag over time
animate_trajectory(...) # Animated flight with live force vectors
```

---

## Output

- **6-panel plot** — x/y position, x/y velocity, and x/y acceleration vs. time
- **Lift vs. Drag force plot** — both forces over the full flight duration
- **Flight animation** — real-time trajectory with velocity (blue), lift (green), and drag (red) vectors rendered at each timestep
- **Console output** — average C_L and C_D printed on run

---

## Physical Assumptions

- The analysis is **2D** (planar flight in the x-y plane)
- Air density is treated as constant (sea-level standard)
- The plane is treated as a **point mass** — rotational dynamics are not modeled
- **n̂** is chosen to point toward the "top" of the plane (counterclockwise from **v̂**); flights where the plane is inverted will produce negative lift coefficients
- The Savitzky-Golay filter is applied to suppress noise from video-based position tracking; window size is automatically tuned to the dataset length

---

## Data Collection

Position data was obtained by video-tracking a paper airplane (Dart design) in flight. Frames were extracted and x-y coordinates logged at uniform time intervals into `PlaneData/Dart1Data.csv` (columns: time, x, y). All length units are in meters, time in seconds.
