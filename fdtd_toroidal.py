"""
Toroidal CTC Sim: Spin-Biased FDTD Wave Propagation
Author: Daniel McCoy (@FreeDeathTV)
Date: October 2025
Paper: Desktop Closed Timelike Curves
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import argparse

# Default parameters
N = 400           # Grid cells
dt = 0.5          # Time step
c = 1.0           # Speed of light (normalized)
eps0 = 1.0        # Base permittivity

# Data from paper table
omegas = np.array([0.000, 0.001, 0.002, 0.005, 0.010])
arrival_times = np.array([400.00, 398.50, 396.80, 392.10, 384.20])

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
    delta_n = 0.1 * np.sin(2 * np.pi * (np.arange(N) + Omega * t) / N)
    eps = eps0 * (1 + delta_n)
    H[1:] = H[1:] + (dt / eps[:-1]) * (E[1:] - E[:-1])
    H[0] = H[0] + dt * (E[-1] - E[0])
    E = np.roll(E, -1)
    E[0] = E[0] + dt * (H[-1] - H[0])
    return E, H

def generate_animation(Omega=0.005):
    """Generate animation GIF"""
    theta = np.linspace(0, 2*np.pi, N)
    
    # Initialize fields
    E = np.zeros(N)
    H = np.zeros(N)
    pulse_center = N//4
    E[pulse_center-10:pulse_center+10] = np.exp(-((np.arange(-10,10))**2)/(2*3**2))
    
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
        ax.set_title(f'Time: {i*2*dt:.1f} dt | Lap: {i*2*dt/400:.1f}', pad=20)
        return line,
    
    ani = FuncAnimation(fig, animate, frames=len(frames), interval=50, blit=True)
    ani.save('animation.gif', writer=PillowWriter(fps=20))
    plt.close()
    print(f"animation.gif created (Omega = {Omega})")

def main():
    parser = argparse.ArgumentParser(description="Toroidal CTC FDTD Simulation")
    parser.add_argument('--omega', type=float, default=0.005, help='Rotation rate Omega')
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
