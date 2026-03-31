# Get Physics Done 5867 (GPD-5867)

### Physics workflow fork for open research verification

[![CI](https://github.com/psi-oss/get-physics-done/actions/workflows/test.yml/badge.svg)](https://github.com/psi-oss/get-physics-done/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/psi-oss/get-physics-done/blob/main/LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![npm](https://img.shields.io/npm/v/get-physics-done)](https://www.npmjs.com/package/get-physics-done)
![arXiv workflow](https://img.shields.io/badge/arXiv-workflow_5867-blue)

**Get Physics Done 5867 (GPD-5867)** is a research-workflow fork of
**Get Physics Done (GPD)** from Physical Superintelligence PBC.

This fork focuses on **open verification workflows around physics papers and reproducible constraint-based derivations**, especially arXiv research discussions and reproducible derivations.

## Physics Verification Workflow

arXiv paper  
↓  
extract equations  
↓  
verification check  
↓  
research note

### Repository structure

framework/
  theory proposal

papers/
  arXiv verification notes

Primary research loop:

observe → verify → revise

Research discussions and artifacts are tracked through:

#arXiv5867

## Verified Density Systems (Constraint vs Sieve)

This repository includes a reproducible example demonstrating two distinct behaviors over:

n ≡ 5 (mod 6)

### Primorial Sieve (multiplicative filtering)

```
gcd(n, P_k) = 1
```

Reference:

```
D_k = ∏(1 - 1/p)
```

Behavior:

```
D_k → 0
```

---

### Structured Modular Constraint

```
n % m ≠ 0
```

Reference:

```
D = 1 - 1/m
```

Example:

```
m = 25 → D = 24/25 = 0.96
```

---

### Multi-Constraint System

```
n % m_i ≠ 0  for all i
```

Reference:

```
D = ∏ (1 - 1/m_i)
```

Example:

```
m = 25, 49 → D ≈ 0.940408
```

---

### Run Verification

```
python3 verify_density.py --mode primorial
python3 verify_density.py --mode mod25
python3 verify_density.py --mode multi_constraint --moduli 25 49
```

---

### Reference Derivations

```
python3 derive_density_reference.py --mode primorial
python3 derive_density_reference.py --mode mod25
```

---

### Paper

See:

```
derivation.pdf
```

---

### Core Result

Multiplicative prime filtering causes density collapse.
Finite modular constraints preserve bounded density.


## Papers (example: first executed verification)

- arXiv:2603.01575 – Intersubjectivity as a principle determining physical observables
- see PAPERS_VERIFIED.md

---

# Who This Is For

GPD-5867 is intended for:

- physicists exploring new arXiv results
- researchers verifying derivations or numerical claims
- collaborators documenting research artifacts
- open scientific discussion tied to reproducible workflows

---

# Quick Start

Install GPD:

npx -y get-physics-done

Run help:

/gpd:help

Start a project:

/gpd:new-project

---

# Differences From Upstream

This fork keeps the core GPD workflow but adds a lightweight public research layer centered around physics papers and verification loops.

Example reference geometry:

cosθ = 1/√2  
θ = 45°

---

# Active Papers

2603.01575 – intersubjective observables (notes)

---

# Original Project

https://github.com/psi-oss/get-physics-done

---

# License

Apache License 2.0
