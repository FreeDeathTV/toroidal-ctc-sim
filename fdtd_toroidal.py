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

# Load simulation parameters from JSON
with open('parameters.json', 'r') as f:
    params = json.load(f)

N = params['N']
dt = params['dt']
dx = params['dx']
omega_default = params['omega']
pulse_width = params['pulse_width']
pulse_center = params['pulse_center']
n_base = params['n_base']
n_mod = params['n_mod']

# Load arrival-time data from CSV
omegas = []
arrival_times = []

with open('timing_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        omegas.append(float(row[0]))
        arrival_times.append(float(row[1]))

omegas = np.array(omegas)
arrival_times = np.array(arrival_times)

def generate_figure1():
    """Generate Figure 1: Arrival Time vs Omega"""
    plt.figure(figsize=(8, 5))
    plt.plot(omegas, arrival_times, 'o-', color='navy', linewidth=2, markersize=8)
    plt.xlabel(r'$\Omega$ (1/step)', fontsize=12)
    plt.ylabel('Arrival Time (dt units)', fontsize=12)
    plt.title('Arrival Time vs. $\Omega$', fontsize=14, pad=15)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('figure1.png', dpi=200, bbox_inches='tight')
    plt.close()
    print("figure1.png created")

def fdtd_step(E, H, Omega, t):
    """One FDTD step with rotating perturbation"""
    delta_n = n_mod * np.sin(2 * np.pi * (np.arange(N) + Omega * t) / N)
    eps = n_base * (1 + delta_n)
    H[1:] = H[1:] + (dt / eps[:-1]) * (E[1:] - E[:-1])
    H[0] = H[0] + dt * (E[-1] - E[0])
    E = np.roll(E, -1)
    E[0] = E[0] + dt * (H[-1] - H[0])
    return E, H

def generate_animation(Omega):
    """Generate animation GIF"""
    theta = np.linspace(0, 2*np.pi, N)
    
    # Initialize fields
    E = np.zeros(N)
    H = np.zeros(N)
    E[pulse_center - pulse_width : pulse_center + pulse_width] = np.exp(
        -((np.arange(-pulse_width, pulse_width))**2) / (2 * 3**2)
    )
    
    frames = []
    for t in range(500):
        E, H = fdtd_step(E, H, Omega, t)
        if t % 2 == 0:
            frames.append(E.copy())
    
    # Create animation
    fig, ax = plt.subplots(figsize=(6,6), subplot_kw={'projection': 'polar'})
    ax.set_ylim(0, 1.5)
    line, = ax.plot([], [], lw=3, color='red')
    
    def animate(i):
        line.set_data(theta, 1 + 0.5 * frames[i])
        ax.set_title(f'Time: {i*2*dt:.1f} dt | Lap: {i*2*dt/N:.1f}', pad=20)
        return line,
    
    ani = FuncAnimation(fig, animate, frames=len(frames), interval=50, blit=True)
    ani.save('animation.gif', writer=PillowWriter(fps=20))
    plt.close()
    print(f"animation.gif created (Omega = {Omega})")

def main():
    parser = argparse.ArgumentParser(description="Toroidal CTC FDTD Simulation")
    parser.add_argument('--omega', type=float, default=omega_default, help='Rotation rate Omega')
    parser.add_argument('--no-fig', action='store_true', help='Skip figure generation')
    parser.add_argument('--no-anim', action='store_true', help='Skip animation')
    
    args = parser.parse_args()
    
    if not args.no_fig:
        generate_figure1()
    if not args.no_anim:
        generate_animation(args.omega)
    
    print("All done! Check figure1.png and animation.gif")

if __name__ == "__main__":
    main()
