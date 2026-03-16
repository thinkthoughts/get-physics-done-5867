"""
verification.py
arXiv:2603.01575

Minimal verification scaffold for non-classical correlations.

This script computes the CHSH quantity for a supplied set of expectation
values. In local hidden-variable models, |S| <= 2. Quantum correlations
can violate this bound up to 2*sqrt(2).
"""

from __future__ import annotations

from math import sqrt


def chsh(E_ab: float, E_abp: float, E_apb: float, E_apbp: float) -> float:
    """
    Compute the CHSH combination:

        S = E(a,b) + E(a,b') + E(a',b) - E(a',b')

    Parameters
    ----------
    E_ab, E_abp, E_apb, E_apbp : float
        Correlation expectation values.

    Returns
    -------
    float
        The CHSH value S.
    """
    return E_ab + E_abp + E_apb - E_apbp


def classify_chsh(S: float) -> str:
    """
    Classify the CHSH result against classical and quantum bounds.
    """
    abs_S = abs(S)
    tsirelson = 2 * sqrt(2)

    if abs_S <= 2:
        return "Classical-compatible: no Bell violation."
    if abs_S <= tsirelson:
        return "Non-classical: Bell violation within quantum bound."
    return "Beyond Tsirelson bound: check assumptions or data."


def demo() -> None:
    """
    Example values that saturate the Tsirelson-optimal quantum pattern:
        E(a,b)   =  1/sqrt(2)
        E(a,b')  =  1/sqrt(2)
        E(a',b)  =  1/sqrt(2)
        E(a',b') = -1/sqrt(2)
    giving S = 2*sqrt(2).
    """
    v = 1 / sqrt(2)
    S = chsh(v, v, v, -v)

    print("arXiv:2603.01575 verification scaffold")
    print("-" * 40)
    print(f"Example CHSH value: {S:.6f}")
    print(f"Quantum bound 2*sqrt(2): {2 * sqrt(2):.6f}")
    print(classify_chsh(S))


if __name__ == "__main__":
    demo()
