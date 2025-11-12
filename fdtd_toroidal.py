"""
Toroidal CTC Sim: Spin-Biased FDTD Wave Propagation
Author: Daniel McCoy (@FreeDeathTV)
Date: November 2025
Paper: Synthetic Time-Loop Analogue via Spin-Biased Wave Propagation in a Toroidal FDTD System
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import argparse
import json
import csv
import os
from pathlib import Path

# ----------------------------------------------------------------------
# 1. Load parameters (exactly the JSON you supplied)
# ----------------------------------------------------------------------
JSON_PATH = Path('parameters.json')
with open(JSON_PATH, 'r') as f:
    p = json.load(f)

N                = p['N']                     # cells around the ring
dx               = p['dx']
dt               = p['dt']
delta_n          = p['delta_n']               # perturbation amplitude
omega_vals       = p['omega_values']          # list of rotation rates to test
pulse_pos        = p['pulse_position']        # injection index
pulse_sigma      = p['pulse_sigma']           # Gaussian width (cells)
inj_dur          = p['injection_duration']    # timesteps the source is on
detect_thr       = p['detection_threshold']   # amplitude to count as "arrival"
circulations     = p['circulations']          # how many laps to wait for
boundary         = p['boundary_condition']    # "periodic"
pert_profile     = p['perturbation_profile']  # "sinusoidal"
pert_rot         = p['perturbation_rotation'] # "clockwise"
sim_steps        = p['simulation_steps']      # safety cap per Omega
avg_runs         = p['averaging_runs']        # statistical averaging
output_files     = p['output_files']

# Derived constants
c0 = 1.0                     # speed of light in vacuum (normalised)
n_base = 1.0                 # baseline index (can be changed later)
eps0 = n_base**2

# ----------------------------------------------------------------------
# 2. Helper: one Yee FDTD step with rotating sinusoidal perturbation
# ----------------------------------------------------------------------
def fdtd_step(E, H, Omega, t):
    """Yee update with rotating Δn = delta_n * sin(2π (k + Ωt)/N)"""
    # rotating index perturbation
    phase = 2 * np.pi * (np.arange(N) + Omega * t) / N
    delta_n_local = delta_n * np.sin(phase)
    eps = eps0 * (1 + delta_n_local)

    # H-update (H is at half-cell)
    H[1:] = H[1:] + (dt / (eps[:-1] * dx)) * (E[1:] - E[:-1])
    H[0]   = H[0]   + (dt / (eps[-1]  * dx)) * (E[0]   - E[-1])   # periodic

    # E-update (E is at integer cells)
    E[:-1] = E[:-1] + (dt / (eps[:-1] * dx)) * (H[:-1] - H[1:])
    E[-1]  = E[-1]  + (dt / (eps[-1]  * dx)) * (H[-1]  - H[0])    # periodic

    return E, H

# ----------------------------------------------------------------------
# 3. Run a single Omega and return arrival time (or NaN)
# ----------------------------------------------------------------------
def run_one_omega(Omega, verbose=False):
    E = np.zeros(N)
    H = np.zeros(N)

    # Gaussian pulse (centered at pulse_pos)
    pulse = np.exp(-0.5 * ((np.arange(N) - pulse_pos) / pulse_sigma) ** 2)
    E = pulse.copy()                     # initial E-field

    # Source injection for the first `inj_dur` steps
    source_on_until = inj_dur

    arrival_step = None
    target_laps = circulations
    laps_completed = 0

    for t in range(sim_steps):
        # inject source while needed
        if t < source_on_until:
            E[pulse_pos] += np.exp(-0.5 * ((t - inj_dur/2) / (inj_dur/4)) ** 2)

        E, H = fdtd_step(E, H, Omega, t)

        # Detect when the pulse **returns** to the injection point
        if E[pulse_pos] > detect_thr and arrival_step is None:
            # count a lap each time we cross the threshold after the first
            laps_completed += 1
            if laps_completed >= target_laps:
                arrival_step = t
                break

    if arrival_step is None:
        if verbose:
            print(f"  Omega={Omega:.4f} → no detection within {sim_steps} steps")
        return np.nan
    else:
        arrival_time = arrival_step * dt
        if verbose:
            print(f"  Omega={Omega:.4f} → arrival at step {arrival_step} (t={arrival_time:.2f})")
        return arrival_time

# ----------------------------------------------------------------------
# 4. Full sweep over omega_vals + averaging
# ----------------------------------------------------------------------
def compute_timing_table():
    results = []
    for omega in omega_vals:
        times = []
        for _ in range(avg_runs):
            t = run_one_omega(omega)
            if not np.isnan(t):
                times.append(t)
        if times:
            mean_t = np.mean(times)
            results.append((omega, mean_t))
        else:
            results.append((omega, np.nan))
    return results

# ----------------------------------------------------------------------
# 5. Write CSV (overwrites old file – safe because we just computed it)
# ----------------------------------------------------------------------
def write_csv(data):
    csv_path = Path('timing_data.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Omega (1/step)', 'Arrival Time (dt units)',
                         'Delta t vs. Omega=0', 'Delta t Fraction (%)'])
        if data:
            t0 = data[0][1]                     # reference (Omega=0)
            for omega, t in data:
                delta = t - t0
                frac  = 100 * delta / t0 if t0 != 0 else 0.0
                writer.writerow([f"{omega:.3f}", f"{t:.2f}", f"{delta:.2f}", f"{frac:.2f}"])
    print(f"{csv_path} written")

# ----------------------------------------------------------------------
# 6. Figure 1 (uses the freshly written CSV)
# ----------------------------------------------------------------------
def plot_figure1():
    # Re-read CSV to guarantee consistency
    omegas, arrivals = [], []
    with open('timing_data.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)                     # skip header
        for row in reader:
            omegas.append(float(row[0]))
            arrivals.append(float(row[1]))

    plt.figure(figsize=(8, 5))
    plt.plot(omegas, arrivals, 'o-', color='navy', linewidth=2, markersize=8)
    plt.xlabel(r'$\Omega$ (1/step)', fontsize=12)
    plt.ylabel('Arrival Time (dt units)', fontsize=12)
    plt.title('Arrival Time vs. $\Omega$', fontsize=14, pad=15)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figure1.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("figure1.png created")

# ----------------------------------------------------------------------
# 7. Animation (polar plot) – one Omega at a time
# ----------------------------------------------------------------------
def make_animation(Omega):
    E = np.zeros(N)
    H = np.zeros(N)

    # Initial Gaussian pulse
    pulse = np.exp(-0.5 * ((np.arange(N) - pulse_pos) / pulse_sigma) ** 2)
    E = pulse.copy()

    frames = []
    record_every = 2                     # keep GIF size reasonable
    for t in range(sim_steps):
        if t < inj_dur:
            E[pulse_pos] += np.exp(-0.5 * ((t - inj_dur/2) / (inj_dur/4)) ** 2)
        E, H = fdtd_step(E, H, Omega, t)
        if t % record_every == 0:
            frames.append(E.copy())

    # Polar plot
    theta = np.linspace(0, 2*np.pi, N, endpoint=False)
    fig, ax = plt.subplots(figsize=(6,6), subplot_kw={'projection': 'polar'})
    ax.set_ylim(0, 1.5)
    line, = ax.plot([], [], lw=3, color='red')

    def animate(i):
        line.set_data(theta, 1 + 0.5 * frames[i])
        ax.set_title(f'Time: {i*record_every*dt:.2f} dt | Lap: {i*record_every*dt/N:.2f}',
                     pad=20)
        return line,

    ani = FuncAnimation(fig, animate, frames=len(frames), interval=50, blit=True)
    ani.save('animation.gif', writer=PillowWriter(fps=20))
    plt.close()
    print(f"animation.gif created (Ω = {Omega})")

# ----------------------------------------------------------------------
# 8. CLI
# ----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Toroidal CTC FDTD Simulation")
    parser.add_argument('--omega', type=float, default=omega_vals[0],
                        help='Single rotation rate for animation (default: first in list)')
    parser.add_argument('--no-csv', action='store_true', help='Skip CSV generation')
    parser.add_argument('--no-fig', action='store_true', help='Skip Figure 1')
    parser.add_argument('--no-anim', action='store_true', help='Skip animation')
    args = parser.parse_args()

    if not args.no_csv:
        data = compute_timing_table()
        write_csv(data)

    if not args.no_fig:
        plot_figure1()

    if not args.no_anim:
        make_animation(args.omega)

    print("All done! Check the repo for figure1.png, animation.gif, timing_data.csv")

if __name__ == "__main__":
    main()
