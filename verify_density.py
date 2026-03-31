
#!/usr/bin/env python3
"""
verify_density.py

Empirically measures the density of integers n <= L such that:
- n ≡ 5 (mod 6)
- gcd(n, P_k) = 1, where P_k is the primorial of the first k primes

Output is structured JSON for reproducibility.

Example:
    python verify_density.py --k-values 1 2 3 4 5 --L-values 1000 10000 100000

Notes:
- The normalization used here is exactly:
      D_k(L) = |S_{k,L}| / (L / 6)
  matching REQUIREMENTS.md
- This version reports both:
    1. empirical density
    2. finite-k expected density from the Euler-product-style filter
- Optional comparison to a global target (default 24/25) is retained.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from typing import Any, Dict, List


DEFAULT_GLOBAL_TARGET = 24 / 25


@dataclass
class DensityResult:
    k: int
    L: int
    primorial: int
    primes_used: List[int]
    valid_count: int
    normalization_denominator: float
    empirical_density: float
    expected_density_finite_k: float
    absolute_error_vs_finite_k_expectation: float
    global_target_density: float
    absolute_error_vs_global_target: float


def first_n_primes(n: int) -> List[int]:
    """Return the first n primes."""
    if n < 0:
        raise ValueError("n must be non-negative")
    primes: List[int] = []
    candidate = 2
    while len(primes) < n:
        is_prime = True
        limit = int(candidate ** 0.5)
        for p in primes:
            if p > limit:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1 if candidate == 2 else 2
    return primes


def primorial(primes: List[int]) -> int:
    """Return the product of a list of primes."""
    product = 1
    for p in primes:
        product *= p
    return product


def count_valid_integers(L: int, Pk: int) -> int:
    """
    Count integers n <= L such that:
    - n ≡ 5 (mod 6)
    - gcd(n, Pk) = 1
    """
    if L < 1:
        return 0

    count = 0
    for n in range(5, L + 1, 6):
        if math.gcd(n, Pk) == 1:
            count += 1
    return count


def finite_k_expected_density(primes_used: List[int]) -> float:
    """
    Expected density within the progression n ≡ 5 (mod 6), under independence-style filtering.

    Since n ≡ 5 (mod 6) already guarantees coprimality with 2 and 3,
    primes 2 and 3 contribute no additional filtering here.

    For each prime p >= 5 included in P_k, the surviving fraction is (1 - 1/p).

    Therefore:
        expected_density_finite_k = ∏_{p in primes_used, p >= 5} (1 - 1/p)
    """
    value = 1.0
    for p in primes_used:
        if p >= 5:
            value *= (1.0 - 1.0 / p)
    return value


def classify_sequence(values: List[float], tolerance: float) -> str:
    """
    Lightweight empirical classification for the tested range only.
    Returns one of:
    - "convergent"
    - "oscillatory"
    - "inconclusive"
    """
    if len(values) < 3:
        return "inconclusive"

    diffs = [abs(values[i] - values[i - 1]) for i in range(1, len(values))]
    decreasing = all(diffs[i] <= diffs[i - 1] + tolerance for i in range(1, len(diffs)))
    small_tail = len(diffs) >= 2 and diffs[-1] <= tolerance and diffs[-2] <= tolerance

    center = values[-1]
    centered = [v - center for v in values[:-1]]
    sign_changes = 0
    for i in range(1, len(centered)):
        if centered[i] == 0 or centered[i - 1] == 0:
            continue
        if (centered[i] > 0) != (centered[i - 1] > 0):
            sign_changes += 1

    if decreasing and small_tail:
        return "convergent"
    if sign_changes >= 2:
        return "oscillatory"
    return "inconclusive"


def verify_density(
    k_values: List[int],
    L_values: List[int],
    global_target: float,
) -> Dict[str, Any]:
    """Compute empirical density data and return a JSON-serializable report."""
    if not k_values:
        raise ValueError("k_values must not be empty")
    if not L_values:
        raise ValueError("L_values must not be empty")
    if any(k < 0 for k in k_values):
        raise ValueError("All k values must be non-negative")
    if any(L < 1 for L in L_values):
        raise ValueError("All L values must be positive integers")

    sorted_k = sorted(dict.fromkeys(k_values))
    sorted_L = sorted(dict.fromkeys(L_values))

    experiments: List[Dict[str, Any]] = []
    sequence_summaries: List[Dict[str, Any]] = []

    for k in sorted_k:
        primes_used = first_n_primes(k)
        Pk = primorial(primes_used)
        expected_finite_k = finite_k_expected_density(primes_used)

        empirical_densities_for_k: List[float] = []

        for L in sorted_L:
            valid_count = count_valid_integers(L=L, Pk=Pk)
            normalization_denominator = L / 6.0
            empirical_density = valid_count / normalization_denominator if normalization_denominator else float("nan")

            abs_error_finite_k = abs(empirical_density - expected_finite_k)
            abs_error_global = abs(empirical_density - global_target)

            result = DensityResult(
                k=k,
                L=L,
                primorial=Pk,
                primes_used=primes_used,
                valid_count=valid_count,
                normalization_denominator=normalization_denominator,
                empirical_density=empirical_density,
                expected_density_finite_k=expected_finite_k,
                absolute_error_vs_finite_k_expectation=abs_error_finite_k,
                global_target_density=global_target,
                absolute_error_vs_global_target=abs_error_global,
            )
            experiments.append(asdict(result))
            empirical_densities_for_k.append(empirical_density)

        sequence_summaries.append(
            {
                "k": k,
                "primorial": Pk,
                "primes_used": primes_used,
                "expected_density_finite_k": expected_finite_k,
                "tested_L_values": sorted_L,
                "empirical_densities": empirical_densities_for_k,
                "classification_over_tested_range": classify_sequence(
                    empirical_densities_for_k, tolerance=1e-12
                ),
                "finite_sample_only": True,
            }
        )

    return {
        "experiment": "number_theoretic_density_verification",
        "normalization": "D_k(L) = |S_{k,L}| / (L/6), where S_{k,L} = {n <= L : n ≡ 5 (mod 6), gcd(n, P_k)=1}",
        "finite_k_expectation": "Within n ≡ 5 (mod 6), primes 2 and 3 are already excluded by the progression, so expected_density_finite_k = product over p in primes_used with p >= 5 of (1 - 1/p).",
        "parameters": {
            "k_values": sorted_k,
            "L_values": sorted_L,
            "global_target_density": global_target,
        },
        "results": experiments,
        "sequence_summaries": sequence_summaries,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Empirically verify the density D_k(L) for n ≡ 5 (mod 6) and gcd(n, P_k)=1."
    )
    parser.add_argument(
        "--k-values",
        nargs="+",
        type=int,
        default=[1, 2, 3, 4, 5],
        help="List of k values, where P_k is the primorial of the first k primes.",
    )
    parser.add_argument(
        "--L-values",
        nargs="+",
        type=int,
        default=[10**3, 10**4, 10**5],
        help="List of upper bounds L to test.",
    )
    parser.add_argument(
        "--global-target",
        type=float,
        default=DEFAULT_GLOBAL_TARGET,
        help="Optional global target density used for comparison only.",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = verify_density(
        k_values=args.k_values,
        L_values=args.L_values,
        global_target=args.global_target,
    )
    print(json.dumps(report, indent=args.indent, sort_keys=False))


if __name__ == "__main__":
    main()
