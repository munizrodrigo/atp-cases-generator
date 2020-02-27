from math import sqrt, acos, sin, pi


def calculate_impedance_load(s, fp, vrms, f, n_phases):
    v = vrms / sqrt(3) if n_phases == 1 else vrms
    p = s * fp
    z = (v ** 2 / p) * fp
    theta = acos(fp)
    r = z * fp
    l = (z * sin(theta)) / (2 * pi * f)
    return r, l