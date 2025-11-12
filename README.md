# toroidal-ctc-sim

**Desktop analogue for closed timelike curves using spin-biased FDTD waves**  
arXiv preprint: [https://arxiv.org/auth/endorse?x=HL87OS](https://arxiv.org/auth/endorse?x=HL87OS)

---

## Toroidal CTC Simulation via Rotating Perturbation Drag

This repository contains a Python-based finite-difference time-domain (FDTD) simulation of directional wave delay in a toroidal geometry. It models synthetic time-of-flight shifts induced by a rotating refractive index perturbation—serving as an analogue for closed timelike curve (CTC) behavior in classical wave systems.

Developed as part of the concept paper:  
**"Synthetic Time-Loop Analogue via Rotating Perturbation Drag in a Toroidal FDTD System"**  
Author: Daniel McCoy  
Date: October 2025

---

## 🧠 Project Overview

- Simulates electromagnetic wave propagation in a 1D toroidal waveguide using FDTD.
- Introduces a rotating index perturbation to induce directional bias.
- Measures arrival-time shifts of circulating pulses across multiple Ω values.
- Visualises the effect via plots and animations.
- Explores implications for delay-based computation, recursive logic, and analogue metaphysics.

---

## 📦 Repository Contents

| File               | Description                                                  |
|--------------------|--------------------------------------------------------------|
| `fdtd_toroidal.py` | Main simulation script (FDTD core + pulse injection + arrival-time measurement) |
| `figure1.png`      | Arrival time vs. Ω plot                                      |
| `animation.gif`    | Field evolution animation                                    |
| `main.tex`         | LaTeX source for the concept paper                           |
| `LICENSE`          | MIT license                                                  |
| `README.md`        | Project overview and instructions                            |

---

## 🚀 How to Run

### Requirements
- Python 3.8+
- `numpy`
- `matplotlib`

### Installation
```bash
pip install numpy matplotlib

python fdtd_toroidal.py

This will:
- Run the FDTD simulation for multiple Ω values
- Print arrival times
- Generate `figure1.png` and `animation.gif`

### 📊 Parameters

Key variables defined in `fdtd_toroidal.py`:
- `N`: Number of spatial cells
- `dx`, `dt`: Spatial and temporal resolution
- `delta_n`: Refractive index perturbation amplitude
- `omega_values`: Rotation rates to test
- `pulse_position`, `pulse_sigma`: Injection profile
- `detection_threshold`: Arrival detection cutoff

### 📄 Documentation

- Concept Paper (PDF) — *concept_paper.pdf*
- White Paper: Commercial Applications — *white_paper_commercial.pdf*

### 🙋 Contact

For questions, collaborations, or citations:  
**Daniel McCoy**  
📧 Email: deathbyanyothername@mail.co.uk  
🐙 GitHub: [FreeDeathTV](https://github.com/FreeDeathTV)


