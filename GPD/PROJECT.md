# Project: Constraint-Structured Density vs Primorial Sieve

## Summary

This project defines and verifies two distinct density systems over the progression:

n ≡ 5 (mod 6)

1. **Primorial sieve (multiplicative filtering)**
2. **Structured modular constraints (finite exclusions)**

The objective is to demonstrate that:

- multiplicative prime filtering produces density decay
- structured modular constraints preserve bounded density

---

## Domain Definition

All measurements are taken over:

S_L = { n ≤ L : n ≡ 5 (mod 6) }

Normalization:

D(L) = |S_L| / (L / 6)

---

## System 1 — Primorial Sieve

### Definition

Let:

P_k = product of first k primes

Filter:

gcd(n, P_k) = 1

### Reference Density

Only primes p ≥ 5 contribute within n ≡ 5 (mod 6), so:

D_k = ∏_{p ≥ 5, p ∈ primes_used} (1 - 1/p)

### Verified Behavior

- k=3 → 0.8  
- k=4 → 0.685714...  
- k=5 → 0.623376...  

As k increases:

D_k → 0

---

## System 2 — Structured Modular Constraint

### Definition

Fix modulus m such that gcd(m, 6) = 1

Filter:

n % m ≠ 0

### Reference Density

D = 1 - 1/m

### Verified Case

m = 25:

D = 24/25 = 0.96

Empirical verification:

- L=1,000 → 0.96  
- L=10,000 → 0.96  
- L=100,000 → 0.96  

---

## System 3 — Multi-Constraint (Finite Structured Product)

### Definition

Given moduli m₁, m₂, ..., m_k such that:

- gcd(m_i, 6) = 1
- moduli are pairwise coprime

Filter:

n % m_i ≠ 0 for all i

### Reference Density

D = ∏ (1 - 1/m_i)

### Verified Case

m₁ = 25, m₂ = 49:

D = (24/25)(48/49) ≈ 0.940408...

Empirical:

- L=1,000 → 0.942  
- L=10,000 → 0.9402  
- L=100,000 → 0.94038  

---

## Key Result

Two distinct density behaviors exist:

### Multiplicative sieve

D_k = ∏ (1 - 1/p) → 0

### Structured constraints

D = ∏ (1 - 1/m_i) → bounded constant

---

## Interpretation

- Primorial filtering introduces **unbounded constraint accumulation**
- Structured modular constraints introduce **finite constraint structure**

Therefore:

> Density collapse is not inherent to filtering — it is specific to multiplicative prime accumulation.

---

## Implementation

### Empirical

verify_density.py

Modes:

- primorial
- mod25
- custom_mod
- multi_constraint

### Reference

derive_density_reference.py

Outputs:

- symbolic expressions
- exact numeric values

---

## Success Criteria

The project is validated if:

1. empirical densities converge to reference densities in all modes  
2. primorial mode exhibits monotonic decay  
3. modular constraint modes remain bounded  
4. multi-constraint mode matches finite product reference  

---

## Position

This project establishes:

- a reproducible distinction between multiplicative sieve systems and structured constraint systems  
- a framework for analyzing density preservation under finite constraints  

---

## Next Steps

- extend structured constraints beyond simple modulus exclusion  
- analyze interaction between residue classes and constraint sets  
- formalize derivations in derivation.tex
