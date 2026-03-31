
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
- This script reports the empirical value relative to a configurable target.
- It does not claim convergence beyond the tested range.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from typing import Any, Dict, List


DEFAULT_TARGET = 24 / 25


@dataclass
class DensityResult:
    k: int
    L: int
    primorial: int
    primes_used: List[int]
    valid_count: int
    normalization_denominator: float
    density: float
    absolute_error_vs_target: float


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
        candidate += 1 if candidate == 2 else 2  # after 2, test odd integers only
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
    start = 5
    step = 6
    for n in range(start, L + 1, step):
        if math.gcd(n, Pk) == 1:
            count += 1
    return count


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

    sign_changes = 0
    target = values[-1]
    centered = [v - target for v in values[:-1]]
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


def verify_density(k_values: List[int], L_values: List[int], target: float) -> Dict[str, Any]:
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

        densities_for_k: List[float] = []

        for L in sorted_L:
            valid_count = count_valid_integers(L=L, Pk=Pk)
            normalization_denominator = L / 6.0
            density = valid_count / normalization_denominator if normalization_denominator else float("nan")
            abs_error = abs(density - target)

            result = DensityResult(
                k=k,
                L=L,
                primorial=Pk,
                primes_used=primes_used,
                valid_count=valid_count,
                normalization_denominator=normalization_denominator,
                density=density,
                absolute_error_vs_target=abs_error,
            )
            experiments.append(asdict(result))
            densities_for_k.append(density)

        sequence_summaries.append(
            {
                "k": k,
                "primorial": Pk,
                "primes_used": primes_used,
                "tested_L_values": sorted_L,
                "densities": densities_for_k,
                "target_density": target,
                "classification_over_tested_range": classify_sequence(
                    densities_for_k, tolerance=1e-12
                ),
                "finite_sample_only": True,
            }
        )

    return {
        "experiment": "number_theoretic_density_verification",
        "normalization": "D_k(L) = |S_{k,L}| / (L/6), where S_{k,L} = {n <= L : n ≡ 5 (mod 6), gcd(n, P_k)=1}",
        "parameters": {
            "k_values": sorted_k,
            "L_values": sorted_L,
            "target_density": target,
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
        "--target",
        type=float,
        default=DEFAULT_TARGET,
        help="Target density used for absolute-error reporting.",
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
        target=args.target,
    )
    print(json.dumps(report, indent=args.indent, sort_keys=False))


if __name__ == "__main__":
    main()
