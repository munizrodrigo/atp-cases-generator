from math import pi

from numpy import angle

from exceptions.exceptions import ImpedanceValueError


class Impedance(object):
    def __init__(self, **kwargs):
        self.R = kwargs.get("R", None)
        self.X = kwargs.get("X", None)
        self.L = kwargs.get("L", None)
        self.C = kwargs.get("C", None)
        self.Z = kwargs.get("Z", None)
        self.f = kwargs.get("f", 60)

        try:
            self.f = float(self.f)
        except ValueError as excep:
            raise ImpedanceValueError(
                message="Incorrect impedance parameters format",
                errors="The format error was: {0}".format(excep)
            )

        if self.f == 0.0:
            raise ImpedanceValueError(
                message="Value 0 not allowed for frequency",
                errors="Frequency = 0"
            )

        arg_name = ["R", "X", "L", "C", "Z"]
        passed_args = [0 if arg is None else 1 for arg in [self.R, self.X, self.L, self.C, self.Z]]
        possible_combinations = [
            [1, 1, 0, 0, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [0, 0, 0, 0, 1]
        ]

        if passed_args not in possible_combinations:
            arg_used = []
            for (name, used) in zip(arg_name, passed_args):
                if used == 1:
                    arg_used.append(name)
            raise ImpedanceValueError(
                message="Incorrect impedance parameters combination. Please, use one of the following combinations:"
                        "(R and X), (R and L or C), (Z)",
                errors="The incorrect combination was {0}".format(arg_used)
            )

        if passed_args == [1, 1, 0, 0, 0]:
            try:
                self.R = float(self.R)
                self.X = float(self.X)
            except ValueError as excep:
                raise ImpedanceValueError(
                    message="Incorrect impedance parameters format",
                    errors="The format error was: {0}".format(excep)
                )
            self.L = self.X / (2 * pi * self.f)
            try:
                self.C = - 1 / (2 * pi * self.f * self.X)
            except ZeroDivisionError:
                self.C = - float("inf")
            self.Z = complex(self.R, self.X)

        if passed_args == [1, 0, 1, 0, 0]:
            try:
                self.R = float(self.R)
                self.L = float(self.L)
            except ValueError as excep:
                raise ImpedanceValueError(
                    message="Incorrect impedance parameters format",
                    errors="The format error was: {0}".format(excep)
                )
            self.X = 2 * pi * self.f * self.L
            try:
                self.C = - 1 / (2 * pi * self.f * self.X)
            except ZeroDivisionError:
                self.C = - float("inf")
            self.Z = complex(self.R, self.X)

        if passed_args == [1, 0, 0, 1, 0]:
            try:
                self.R = float(self.R)
                self.C = float(self.C)
            except ValueError as excep:
                raise ImpedanceValueError(
                    message="Incorrect impedance parameters format",
                    errors="The format error was: {0}".format(excep)
                )
            try:
                self.X = - 1 / (2 * pi * self.f * self.C)
            except ZeroDivisionError:
                self.X = - float("inf")
            self.L = self.X / (2 * pi * self.f)
            self.Z = complex(self.R, self.X)

        if passed_args == [0, 0, 0, 0, 1]:
            try:
                self.Z = complex(self.Z)
            except ValueError as excep:
                raise ImpedanceValueError(
                    message="Incorrect impedance parameters format",
                    errors="The format error was: {0}".format(excep)
                )
            self.R = self.Z.real
            self.X = self.Z.imag
            self.L = self.X / (2 * pi * self.f)
            try:
                self.C = - 1 / (2 * pi * self.f * self.X)
            except ZeroDivisionError:
                self.C = - float("inf")

    def __add__(self, other):
        z_eq = self.to_frequency(f=self.f).Z + other.to_frequency(f=self.f).Z
        return Impedance(Z=z_eq, f=self.f)

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self, other):
        z_eq = self.to_frequency(f=self.f).Z - other.to_frequency(f=self.f).Z
        return Impedance(Z=z_eq, f=self.f)

    def __mul__(self, other):
        z_eq = self.to_frequency(f=self.f).Z * other.to_frequency(f=self.f).Z
        return Impedance(Z=z_eq, f=self.f)

    def __truediv__(self, other):
        try:
            z_eq = self.to_frequency(f=self.f).Z / other.to_frequency(f=self.f).Z
        except ZeroDivisionError:
            z_eq = complex("inf")
        return Impedance(Z=z_eq, f=self.f)

    def __floordiv__(self, other):
        try:
            z_eq = (1 / self.to_frequency(f=self.f).Z) + (1 / other.to_frequency(f=self.f).Z)
            z_eq = 1 / z_eq
        except ZeroDivisionError:
            z_eq = 0.0
        return Impedance(Z=z_eq, f=self.f)

    def __abs__(self):
        return abs(self.Z)

    def __bool__(self):
        return False if self.Z == complex(0.0, 0.0) else True

    def __eq__(self, other):
        return self.to_frequency(f=self.f).Z == other.to_frequency(f=self.f).Z

    def __lt__(self, other):
        return abs(self.to_frequency(f=self.f)) < abs(other.to_frequency(f=self.f))

    def __gt__(self, other):
        return abs(self.to_frequency(f=self.f)) > abs(other.to_frequency(f=self.f))

    def __le__(self, other):
        return abs(self.to_frequency(f=self.f)) <= abs(other.to_frequency(f=self.f))

    def __ge__(self, other):
        return abs(self.to_frequency(f=self.f)) >= abs(other.to_frequency(f=self.f))

    def __str__(self):
        return "{0}+j{1} at f = {2} Hz".format(self.R, self.X, self.f)

    def to_frequency(self, f):
        return Impedance(R=self.R, L=self.L, f=f)

    def to_polar_str(self):
        return "{0} /_ {1}{2} ".format(abs(self), angle(self.Z, deg=True), chr(176))
