# toroidal-ctc-sim

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Zenodo](https://zenodo.org/badge/DOI/10.5281/zenodo.17592350.svg)

**Desktop analogue for closed timelike curves using spin-biased FDTD waves**  
📄 arXiv preprint endorsement pending: [https://arxiv.org/auth/endorse?x=HL87OS](https://arxiv.org/auth/endorse?x=HL87OS)


---

## 🌀 Toroidal CTC Simulation via Rotating Perturbation Drag

This repository contains a Python-based finite-difference time-domain (FDTD) simulation of directional delay in a closed-loop waveguide. It models synthetic time-of-flight shifts induced by a rotating refractive index perturbation—serving as a desktop analogue for closed timelike curve (CTC) behavior in classical wave systems.

Developed for the concept paper:  
**"Synthetic Time-Loop Analogue via Rotating Perturbation Drag in a Toroidal FDTD System"**  
Author: Daniel McCoy  
Date: November 2025

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17592350.svg)](https://doi.org/10.5281/zenodo.17592350)

---

## 🧠 What It Does

- Simulates electromagnetic wave propagation in a 1D toroidal waveguide  
- Applies rotating index perturbation to induce directional bias  
- Measures arrival-time shifts across multiple Ω values  
- Outputs reproducible timing data, plots, and animations  
- Explores implications for delay-based logic, recursive computation, and analogue metaphysics  

---

## 📁 Repository Contents

| File                        | Description                                                  |
|-----------------------------|--------------------------------------------------------------|
| `fdtd_toroidal.py`          | Main simulation script with CLI and modular pipeline         |
| `parameters.json`           | All simulation settings (grid, pulse, perturbation, sweep)   |
| `timing_data.csv`           | Arrival-time results across Ω values                         |
| `figure1.png`               | Arrival time vs. Ω plot                                      |
| `animation.gif`             | Field evolution animation (polar view)                       |
| `concept_paper.pdf`         | Academic write-up                                            |
| `white_paper_commercial.pdf`| Commercial roadmap and prototype strategy                    |
| `main.tex`                  | LaTeX source for concept paper                               |
| `LICENSE`                   | MIT license                                                  |
| `README.md`                 | Project overview and usage guide                             |
| `CITATION.cff`              | Citation metadata with ORCID                                 |

---

## 🚀 How to Run

### Requirements
- Python 3.8+
- `numpy`, `matplotlib`

### Installation
```bash
pip install numpy matplotlib
```

### Run the Simulation
```bash
python fdtd_toroidal.py
```

This will:
- Sweep over all Ω values in `parameters.json`
- Compute arrival times and write `timing_data.csv`
- Generate `figure1.png` and `animation.gif`

### CLI Options
```bash
python fdtd_toroidal.py --omega 0.005 --no-csv --no-fig --no-anim
```

- `--omega`: override Ω for animation  
- `--no-csv`: skip timing sweep  
- `--no-fig`: skip figure generation  
- `--no-anim`: skip animation  

---

## 📊 Parameters

All simulation settings are defined in [`parameters.json`](parameters.json), including:

- `N`, `dx`, `dt`: grid and resolution  
- `delta_n`: perturbation amplitude  
- `omega_values`: rotation rates to test  
- `pulse_position`, `pulse_sigma`: injection profile  
- `injection_duration`, `detection_threshold`: arrival detection logic  
- `circulations`, `simulation_steps`, `averaging_runs`: control flow  

---

## 📄 Documentation

- **Concept Paper** — `concept_paper.pdf`  
- **White Paper** — `white_paper_commercial.pdf`  
- **Citation Metadata** — `CITATION.cff` (ORCID: [0009-0003-1486-0749](https://orcid.org/0009-0003-1486-0749))  

---

## 🙋 Contact

For questions, collaborations, or citations:  
**Daniel McCoy**  
📧 Email: deathbyanyothername@mail.co.uk  
🐙 GitHub: [FreeDeathTV](https://github.com/FreeDeathTV)

---
