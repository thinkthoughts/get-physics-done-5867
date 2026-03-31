# REQUIREMENTS.md

## Purpose

This document specifies the formal requirements for validating the constraint-first invariant framework defined in `PROJECT.md`.

A result is acceptable only if it satisfies explicit, reproducible, quantitative tests.

---

## Scope

The framework must be evaluated in four domains:

1. number theory  
2. geometric projection  
3. transformation stability  
4. constraint gating

Cross-domain extension is allowed only after the core requirements below are satisfied.

---

## Requirement 1 — Number-Theoretic Density Verification

### Statement

Let:

- P_k denote the primorial formed from the first k primes
- S_{k,L} = { n ≤ L : n ≡ 5 mod 6, gcd(n, P_k)=1 }

Define the empirical density:

D_k(L) = |S_{k,L}| / (L/6)

The implementation must verify whether D_k(L) converges to the predicted bounded value specified by the project.

### Minimum requirements

- compute D_k(L) for increasing L
- report values for multiple k
- explicitly define the normalization used
- distinguish finite-sample behavior from asymptotic claims

### Acceptance criteria

The code must:

- produce deterministic output for fixed parameters
- show the computed sequence D_k(L) for increasing L
- report absolute error against the target value
- state whether the observed sequence is:
  - convergent
  - oscillatory
  - inconclusive over tested range

### Failure conditions

This requirement fails if:

- normalization is undefined or inconsistent
- the target value is asserted without numerical evidence
- asymptotic behavior is claimed from too small a range without qualification

---

## Requirement 2 — Projection Constraint Verification

### Statement

For atomic states represented as vectors, let:

- a be an initial atomic state
- T(a) be a transformed atomic state

Define:

cos(θ) = (a · T(a)) / (||a|| ||T(a)||)

The framework requires:

θ ≤ 45°
equivalently
cos(θ) ≥ 1/√2

### Minimum requirements

- implement angle computation from vector data
- test multiple transformed states
- include edge cases:
  - exactly 45°
  - below threshold
  - above threshold

### Acceptance criteria

The code must:

- correctly classify each case as pass or fail
- report computed cosine values
- report numerical tolerance used near threshold

### Failure conditions

This requirement fails if:

- threshold logic is ambiguous
- tolerance is omitted
- zero-norm vectors are not handled explicitly

---

## Requirement 3 — Invariant Preservation Under Transformation

### Statement

Let f be a measurable scalar evaluation of atomic state.

The framework requires bounded deviation under transformation:

|f(T(a)) − f(a)| ≤ ε

for a stated tolerance ε > 0.

### Minimum requirements

- define f explicitly for each tested domain
- define T explicitly for each experiment
- state ε numerically
- test repeated application of T

### Acceptance criteria

The implementation must:

- report f(a)
- report f(T(a))
- report deviation
- report whether deviation remains bounded under iteration

### Failure conditions

This requirement fails if:

- f is undefined or changes between runs without explanation
- ε is omitted
- only one-step behavior is tested when iterative stability is claimed

---

## Requirement 4 — Constraint Gate

### Statement

A transformation is admissible only if all required checks pass.

Given atomic state a, transformation T, and evaluation f, a gate must return:

- allow if all requirements pass
- revise or block otherwise

### Minimum checks

The gate must evaluate:

1. density condition, where applicable  
2. projection condition  
3. invariant deviation condition  

### Acceptance criteria

The gate must:

- return a deterministic decision
- report the failed condition when blocking
- provide machine-readable output

### Failure conditions

This requirement fails if:

- decisions are non-deterministic
- failure reasons are omitted
- different rules are applied without documentation

---

## Requirement 5 — Reproducibility

### Statement

All experiments must be reproducible from repository contents.

### Minimum requirements

The repository must contain:

- source code
- parameter choices
- instructions for execution
- expected output format

### Acceptance criteria

A third party must be able to:

- run the code without hidden steps
- reproduce the reported values
- verify pass/fail outcomes

### Failure conditions

This requirement fails if:

- manual hidden preprocessing is required
- parameters are undocumented
- results depend on unstated environment assumptions

---

## Requirement 6 — Domain Separation

### Statement

Claims must remain separated by domain unless equivalence is explicitly demonstrated.

### Minimum requirements

- number-theoretic results must not be presented as physical laws without a stated mapping
- physical examples must not be presented as proofs of number-theoretic claims
- AI examples must not be presented as evidence for physical claims without formal justification

### Acceptance criteria

Each file must identify:

- domain
- object of study
- evaluation function
- transformation tested

### Failure conditions

This requirement fails if:

- analogy is substituted for proof
- domain shifts occur without formal declaration

---

## Requirement 7 — Output Reporting

### Statement

Every validation script must emit structured output.

### Minimum requirements

Each run must report:

- parameter values
- computed metrics
- tolerance values
- pass/fail result

### Recommended output format

{
  "experiment": "projection_test",
  "parameters": {
    "epsilon": 1e-6
  },
  "metrics": {
    "cos_theta": 0.7071068,
    "angle_degrees": 45.0
  },
  "result": "allow"
}

### Failure conditions

This requirement fails if output is only informal text or cannot be parsed consistently.

---

## Requirement 8 — Minimal File Set

The following files are required for initial validation:

- GPD/PROJECT.md
- GPD/REQUIREMENTS.md
- verify_density.py
- projection_tests.py
- constraint.py

Recommended additional files:

- derivation.tex
- cross_domain_validation.md
- README.md

---

## Requirement 9 — Acceptance Summary

The project passes initial validation only if all of the following are satisfied:

1. density computation is defined and reproducible  
2. projection threshold logic is correct and tested  
3. invariant deviation is bounded by explicit ε  
4. constraint gate returns deterministic decisions  
5. results are reproducible from repository contents  
6. domain claims remain separated unless formally connected  

If any of these conditions fail, the project remains incomplete.

---

## Next Implementation Order

1. verify_density.py  
2. projection_tests.py  
3. constraint.py  
4. derivation.tex  
5. cross_domain_validation.md
