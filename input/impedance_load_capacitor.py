from math import sqrt, acos, sin, pi


def calculate_impedance_load(s, fp, vrms, f, n_phases):
    v = vrms if n_phases == 2 else vrms / sqrt(3)
    if n_phases == 3:
        s = float(s / 3)
    p = s * fp
    z = (v ** 2 / p) * fp
    theta = acos(fp)
    r = z * fp
    l = (z * sin(theta)) / (2 * pi * f)
    return r, l


def calculate_impedance_capacitor(q, vrms, f, n_phases):
    v = vrms if n_phases == 2 else vrms / sqrt(3)
    if n_phases == 3:
        q = float(q / 3)
    c = q / ((2 * pi * f) * v ** 2)
    return c
