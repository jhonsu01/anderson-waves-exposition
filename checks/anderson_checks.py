"""Simulacion numerica sencilla del modelo de Anderson en redes pequenas.

Muestra el fenomeno, pero no prueba nada: las redes son pequenas y el teorema habla de redes infinitas.
Mide que fraccion de la red ocupa de verdad un estado cerca del centro de la banda (participacion).
"""
import sys

import numpy as np

SEED = 20261104


def hamiltonian(dim, side, width, rng):
    """H = suma de vecinos + V, con V uniforme en [-width/2, width/2] y bordes periodicos."""
    n = side**dim
    h = np.zeros((n, n))
    for index in range(n):
        coords = list(np.unravel_index(index, (side,) * dim))
        for axis in range(dim):
            neighbor = list(coords)
            neighbor[axis] = (coords[axis] + 1) % side
            j = np.ravel_multi_index(neighbor, (side,) * dim)
            h[index, j] = h[j, index] = 1.0
    h[np.diag_indices(n)] = rng.uniform(-width / 2, width / 2, n)
    return h


def participation(dim, side, width, samples, rng):
    """Fraccion de sitios ocupados: (1 / suma |psi|^4) / N, promediada cerca de energia cero."""
    values = []
    for _ in range(samples):
        energies, vectors = np.linalg.eigh(hamiltonian(dim, side, width, rng))
        n = side**dim
        order = np.argsort(np.abs(energies))[: max(4, n // 25)]
        ipr = np.sum(np.abs(vectors[:, order]) ** 4, axis=0)
        values.append(np.mean(1 / ipr) / n)
    return float(np.mean(values))


def wave_width(width, steps, rng, side=601):
    """Propaga un paquete en una linea y devuelve su anchura al final."""
    h = hamiltonian(1, side, width, rng)
    energies, vectors = np.linalg.eigh(h)
    start = np.zeros(side, dtype=complex)
    start[side // 2] = 1
    coeffs = vectors.T @ start
    state = vectors @ (np.exp(-1j * energies * steps) * coeffs)
    x = np.arange(side) - side // 2
    return float(np.sqrt(np.sum(x**2 * np.abs(state) ** 2)))


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    rng = np.random.default_rng(SEED)
    print("Fraccion de la red ocupada por estados cerca de energia cero (promedio)")
    cases = [(1, 1000, 2), (2, 40, 3), (3, 12, 3)]
    table = {}
    for dim, side, samples in cases:
        for width in (0.5, 2.0, 16.0, 40.0):
            value = participation(dim, side, width, samples, rng)
            table[(dim, width)] = value
            print(f"  dim {dim}, N = {side ** dim:5d}, desorden {width:5.1f}: {value:.4f}")
    print("Anchura de una onda en una linea tras t = 60")
    clean, messy = wave_width(0.0, 60, rng), wave_width(4.0, 60, rng)
    print(f"  sin desorden: {clean:.1f}   con desorden 4: {messy:.1f}")

    ok = clean > 5 * messy and table[(3, 40.0)] < table[(3, 2.0)] and table[(1, 40.0)] < table[(1, 2.0)]
    print("TODO OK" if ok else "HAY FALLOS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
