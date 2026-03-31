
#!/usr/bin/env python3
"""
verify_density.py

Empirically measures the density of integers n <= L such that:
- n ≡ 5 (mod 6)
- and a selectable filter condition holds

Supported modes:
- primorial:
    gcd(n, P_k) = 1, where P_k is the primorial of the first k primes
- mod25:
    n % 25 != 0
- custom_mod:
    n % m != 0 for a user-supplied modulus m
- multi_constraint:
    n % m != 0 for every user-supplied modulus m in a finite list

Output is structured JSON for reproducibility.

Examples:
    python3 verify_density.py --mode primorial --k-values 1 2 3 4 5 --L-values 1000 10000 100000
    python3 verify_density.py --mode mod25 --L-values 1000 10000 100000
    python3 verify_density.py --mode custom_mod --modulus 25 --L-values 1000 10000 100000
    python3 verify_density.py --mode multi_constraint --moduli 25 49 --L-values 1000 10000 100000
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


DEFAULT_GLOBAL_TARGET = 24 / 25


@dataclass
class DensityResult:
    mode: str
    k: Optional[int]
    L: int
    primorial: Optional[int]
    primes_used: Optional[List[int]]
    modulus: Optional[int]
    moduli: Optional[List[int]]
    valid_count: int
    normalization_denominator: float
    empirical_density: float
    expected_density_reference: float
    absolute_error_vs_reference: float
    global_target_density: float
    absolute_error_vs_global_target: float


def first_n_primes(n: int) -> List[int]:
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
    product = 1
    for p in primes:
        product *= p
    return product


def count_valid_primorial(L: int, Pk: int) -> int:
    if L < 1:
        return 0
    count = 0
    for n in range(5, L + 1, 6):
        if math.gcd(n, Pk) == 1:
            count += 1
    return count


def count_valid_modulus_exclusion(L: int, modulus: int) -> int:
    if L < 1:
        return 0
    if modulus <= 0:
        raise ValueError("modulus must be a positive integer")
    count = 0
    for n in range(5, L + 1, 6):
        if n % modulus != 0:
            count += 1
    return count


def count_valid_multi_constraint(L: int, moduli: List[int]) -> int:
    if L < 1:
        return 0
    if not moduli:
        raise ValueError("moduli must not be empty")
    for m in moduli:
        if m <= 0:
            raise ValueError("all moduli must be positive integers")

    count = 0
    for n in range(5, L + 1, 6):
        if all(n % m != 0 for m in moduli):
            count += 1
    return count


def finite_k_expected_density(primes_used: List[int]) -> float:
    """
    Within n ≡ 5 (mod 6), primes 2 and 3 are already excluded by the progression.
    So the finite-k reference density is:
        ∏_{p in primes_used, p >= 5} (1 - 1/p)
    """
    value = 1.0
    for p in primes_used:
        if p >= 5:
            value *= (1.0 - 1.0 / p)
    return value


def validate_modulus_for_progression(modulus: int) -> None:
    if modulus <= 0:
        raise ValueError("modulus must be a positive integer")
    if math.gcd(modulus, 6) != 1:
        raise ValueError(
            "modulus must be coprime to 6 for the simple reference 1 - 1/modulus to apply cleanly within n ≡ 5 (mod 6)."
        )


def expected_density_modulus_exclusion(modulus: int) -> float:
    """
    For the restricted progression n ≡ 5 (mod 6), if gcd(modulus, 6)=1 then
    multiples of modulus appear with density 1/modulus inside the progression.
    So the reference density is:
        1 - 1/modulus
    """
    validate_modulus_for_progression(modulus)
    return 1.0 - 1.0 / modulus


def pairwise_coprime(values: List[int]) -> bool:
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if math.gcd(values[i], values[j]) != 1:
                return False
    return True


def expected_density_multi_constraint(moduli: List[int]) -> float:
    """
    For a finite list of pairwise-coprime moduli, each also coprime to 6,
    the excluded classes behave independently within n ≡ 5 (mod 6), so:

        expected_density_reference = ∏ (1 - 1/m)

    This keeps the interpretation precise and avoids accidental overlap errors.
    """
    if not moduli:
        raise ValueError("moduli must not be empty")
    unique_moduli = sorted(dict.fromkeys(moduli))
    for m in unique_moduli:
        validate_modulus_for_progression(m)
    if not pairwise_coprime(unique_moduli):
        raise ValueError(
            "multi_constraint reference currently requires pairwise-coprime moduli."
        )

    value = 1.0
    for m in unique_moduli:
        value *= (1.0 - 1.0 / m)
    return value


def classify_sequence(values: List[float], tolerance: float = 1e-12) -> str:
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


def verify_density_primorial(
    k_values: List[int],
    L_values: List[int],
    global_target: float,
) -> Dict[str, Any]:
    if not k_values:
        raise ValueError("k_values must not be empty for primorial mode")
    if any(k < 0 for k in k_values):
        raise ValueError("All k values must be non-negative")

    sorted_k = sorted(dict.fromkeys(k_values))
    sorted_L = sorted(dict.fromkeys(L_values))

    experiments: List[Dict[str, Any]] = []
    sequence_summaries: List[Dict[str, Any]] = []

    for k in sorted_k:
        primes_used = first_n_primes(k)
        Pk = primorial(primes_used)
        expected_ref = finite_k_expected_density(primes_used)

        empirical_densities_for_k: List[float] = []

        for L in sorted_L:
            valid_count = count_valid_primorial(L=L, Pk=Pk)
            denominator = L / 6.0
            empirical_density = valid_count / denominator if denominator else float("nan")

            experiments.append(
                asdict(
                    DensityResult(
                        mode="primorial",
                        k=k,
                        L=L,
                        primorial=Pk,
                        primes_used=primes_used,
                        modulus=None,
                        moduli=None,
                        valid_count=valid_count,
                        normalization_denominator=denominator,
                        empirical_density=empirical_density,
                        expected_density_reference=expected_ref,
                        absolute_error_vs_reference=abs(empirical_density - expected_ref),
                        global_target_density=global_target,
                        absolute_error_vs_global_target=abs(empirical_density - global_target),
                    )
                )
            )
            empirical_densities_for_k.append(empirical_density)

        sequence_summaries.append(
            {
                "mode": "primorial",
                "k": k,
                "primorial": Pk,
                "primes_used": primes_used,
                "expected_density_reference": expected_ref,
                "tested_L_values": sorted_L,
                "empirical_densities": empirical_densities_for_k,
                "classification_over_tested_range": classify_sequence(empirical_densities_for_k),
                "finite_sample_only": True,
            }
        )

    return {
        "experiment": "number_theoretic_density_verification",
        "mode": "primorial",
        "normalization": "D_k(L) = |S_{k,L}| / (L/6), where S_{k,L} = {n <= L : n ≡ 5 (mod 6), gcd(n, P_k)=1}",
        "reference_density": "Within n ≡ 5 (mod 6), primes 2 and 3 are already excluded by the progression, so expected_density_reference = product over p in primes_used with p >= 5 of (1 - 1/p).",
        "parameters": {
            "k_values": sorted_k,
            "L_values": sorted_L,
            "global_target_density": global_target,
        },
        "results": experiments,
        "sequence_summaries": sequence_summaries,
    }


def verify_density_modulus(
    mode: str,
    modulus: int,
    L_values: List[int],
    global_target: float,
) -> Dict[str, Any]:
    sorted_L = sorted(dict.fromkeys(L_values))
    expected_ref = expected_density_modulus_exclusion(modulus)

    experiments: List[Dict[str, Any]] = []
    empirical_densities: List[float] = []

    for L in sorted_L:
        valid_count = count_valid_modulus_exclusion(L=L, modulus=modulus)
        denominator = L / 6.0
        empirical_density = valid_count / denominator if denominator else float("nan")

        experiments.append(
            asdict(
                DensityResult(
                    mode=mode,
                    k=None,
                    L=L,
                    primorial=None,
                    primes_used=None,
                    modulus=modulus,
                    moduli=None,
                    valid_count=valid_count,
                    normalization_denominator=denominator,
                    empirical_density=empirical_density,
                    expected_density_reference=expected_ref,
                    absolute_error_vs_reference=abs(empirical_density - expected_ref),
                    global_target_density=global_target,
                    absolute_error_vs_global_target=abs(empirical_density - global_target),
                )
            )
        )
        empirical_densities.append(empirical_density)

    return {
        "experiment": "number_theoretic_density_verification",
        "mode": mode,
        "normalization": "D(L) = |S_L| / (L/6), where S_L = {n <= L : n ≡ 5 (mod 6), n % modulus != 0}",
        "reference_density": "For modulus coprime to 6, expected_density_reference = 1 - 1/modulus within the progression n ≡ 5 (mod 6).",
        "parameters": {
            "modulus": modulus,
            "L_values": sorted_L,
            "global_target_density": global_target,
        },
        "results": experiments,
        "sequence_summary": {
            "mode": mode,
            "modulus": modulus,
            "expected_density_reference": expected_ref,
            "tested_L_values": sorted_L,
            "empirical_densities": empirical_densities,
            "classification_over_tested_range": classify_sequence(empirical_densities),
            "finite_sample_only": True,
        },
    }


def verify_density_multi_constraint(
    moduli: List[int],
    L_values: List[int],
    global_target: float,
) -> Dict[str, Any]:
    unique_moduli = sorted(dict.fromkeys(moduli))
    sorted_L = sorted(dict.fromkeys(L_values))
    expected_ref = expected_density_multi_constraint(unique_moduli)

    experiments: List[Dict[str, Any]] = []
    empirical_densities: List[float] = []

    for L in sorted_L:
        valid_count = count_valid_multi_constraint(L=L, moduli=unique_moduli)
        denominator = L / 6.0
        empirical_density = valid_count / denominator if denominator else float("nan")

        experiments.append(
            asdict(
                DensityResult(
                    mode="multi_constraint",
                    k=None,
                    L=L,
                    primorial=None,
                    primes_used=None,
                    modulus=None,
                    moduli=unique_moduli,
                    valid_count=valid_count,
                    normalization_denominator=denominator,
                    empirical_density=empirical_density,
                    expected_density_reference=expected_ref,
                    absolute_error_vs_reference=abs(empirical_density - expected_ref),
                    global_target_density=global_target,
                    absolute_error_vs_global_target=abs(empirical_density - global_target),
                )
            )
        )
        empirical_densities.append(empirical_density)

    return {
        "experiment": "number_theoretic_density_verification",
        "mode": "multi_constraint",
        "normalization": "D(L) = |S_L| / (L/6), where S_L = {n <= L : n ≡ 5 (mod 6), and n % m != 0 for every m in moduli}",
        "reference_density": "For pairwise-coprime moduli, each coprime to 6, expected_density_reference = product over m in moduli of (1 - 1/m).",
        "parameters": {
            "moduli": unique_moduli,
            "L_values": sorted_L,
            "global_target_density": global_target,
        },
        "results": experiments,
        "sequence_summary": {
            "mode": "multi_constraint",
            "moduli": unique_moduli,
            "expected_density_reference": expected_ref,
            "tested_L_values": sorted_L,
            "empirical_densities": empirical_densities,
            "classification_over_tested_range": classify_sequence(empirical_densities),
            "finite_sample_only": True,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Empirically verify density over n ≡ 5 (mod 6) with selectable filters."
    )
    parser.add_argument(
        "--mode",
        choices=["primorial", "mod25", "custom_mod", "multi_constraint"],
        default="primorial",
        help="Filter mode to test.",
    )
    parser.add_argument(
        "--k-values",
        nargs="+",
        type=int,
        default=[1, 2, 3, 4, 5],
        help="List of k values for primorial mode.",
    )
    parser.add_argument(
        "--L-values",
        nargs="+",
        type=int,
        default=[10**3, 10**4, 10**5],
        help="List of upper bounds L to test.",
    )
    parser.add_argument(
        "--modulus",
        type=int,
        default=25,
        help="Modulus used in custom_mod mode. Default 25.",
    )
    parser.add_argument(
        "--moduli",
        nargs="+",
        type=int,
        default=[25, 49],
        help="Finite list of moduli used in multi_constraint mode.",
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

    if any(L < 1 for L in args.L_values):
        raise ValueError("All L values must be positive integers")

    if args.mode == "primorial":
        report = verify_density_primorial(
            k_values=args.k_values,
            L_values=args.L_values,
            global_target=args.global_target,
        )
    elif args.mode == "mod25":
        report = verify_density_modulus(
            mode="mod25",
            modulus=25,
            L_values=args.L_values,
            global_target=args.global_target,
        )
    elif args.mode == "custom_mod":
        report = verify_density_modulus(
            mode="custom_mod",
            modulus=args.modulus,
            L_values=args.L_values,
            global_target=args.global_target,
        )
    else:
        report = verify_density_multi_constraint(
            moduli=args.moduli,
            L_values=args.L_values,
            global_target=args.global_target,
        )

    print(json.dumps(report, indent=args.indent, sort_keys=False))


if __name__ == "__main__":
    main()
