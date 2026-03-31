
#!/usr/bin/env python3
"""
derive_density_reference.py

Computes exact (symbolic) and numeric reference densities for:

- primorial mode
- custom_mod / mod25 mode
- multi_constraint mode

This pairs with verify_density.py by providing the "theoretical side"
of each experiment in a clean, reproducible form.

Examples:

    python3 derive_density_reference.py --mode primorial --k-values 1 2 3 4 5

    python3 derive_density_reference.py --mode mod25

    python3 derive_density_reference.py --mode custom_mod --modulus 25

    python3 derive_density_reference.py --mode multi_constraint --moduli 25 49
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Dict, List


def first_n_primes(n: int) -> List[int]:
    primes = []
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


def finite_k_product(primes: List[int]) -> float:
    value = 1.0
    filtered = []
    for p in primes:
        if p >= 5:
            value *= (1 - 1/p)
            filtered.append(p)
    return value, filtered


def validate_modulus(m: int):
    if m <= 0:
        raise ValueError("modulus must be positive")
    if math.gcd(m, 6) != 1:
        raise ValueError("modulus must be coprime to 6")


def product_moduli(moduli: List[int]) -> float:
    value = 1.0
    for m in moduli:
        value *= (1 - 1/m)
    return value


def pairwise_coprime(moduli: List[int]) -> bool:
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if math.gcd(moduli[i], moduli[j]) != 1:
                return False
    return True


def derive_primorial(k_values: List[int]) -> Dict:
    results = []
    for k in k_values:
        primes = first_n_primes(k)
        value, filtered = finite_k_product(primes)

        results.append({
            "k": k,
            "primes_used": primes,
            "primes_contributing": filtered,
            "symbolic": " * ".join([f"(1 - 1/{p})" for p in filtered]) if filtered else "1",
            "numeric": value
        })

    return {
        "mode": "primorial",
        "definition": "product over primes p >= 5 of (1 - 1/p)",
        "results": results
    }


def derive_modulus(m: int, mode: str) -> Dict:
    validate_modulus(m)

    return {
        "mode": mode,
        "modulus": m,
        "symbolic": f"(1 - 1/{m})",
        "numeric": 1 - 1/m
    }


def derive_multi(moduli: List[int]) -> Dict:
    unique = sorted(set(moduli))

    for m in unique:
        validate_modulus(m)

    if not pairwise_coprime(unique):
        raise ValueError("moduli must be pairwise coprime")

    value = product_moduli(unique)

    symbolic = " * ".join([f"(1 - 1/{m})" for m in unique])

    return {
        "mode": "multi_constraint",
        "moduli": unique,
        "symbolic": symbolic,
        "numeric": value
    }


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--mode",
        choices=["primorial", "mod25", "custom_mod", "multi_constraint"],
        required=True
    )

    parser.add_argument("--k-values", nargs="+", type=int, default=[1,2,3,4,5])
    parser.add_argument("--modulus", type=int, default=25)
    parser.add_argument("--moduli", nargs="+", type=int, default=[25,49])

    return parser.parse_args()


def main():
    args = parse_args()

    if args.mode == "primorial":
        result = derive_primorial(args.k_values)

    elif args.mode == "mod25":
        result = derive_modulus(25, "mod25")

    elif args.mode == "custom_mod":
        result = derive_modulus(args.modulus, "custom_mod")

    else:
        result = derive_multi(args.moduli)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
