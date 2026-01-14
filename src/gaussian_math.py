import math
import random

class GaussianInt:
    def __init__(self, r, i=0):
        self.real = r
        self.imag = i

    def __add__(self, other):
        if isinstance(other, int):
            return GaussianInt(self.real + other, self.imag)
        return GaussianInt(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        if isinstance(other, int):
            return GaussianInt(self.real - other, self.imag)
        return GaussianInt(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        if isinstance(other, int):
            return GaussianInt(self.real * other, self.imag * other)
        return GaussianInt(
            self.real * other.real - self.imag * other.imag,
            self.real * other.imag + self.imag * other.real
        )

    def norm(self):
        return self.real**2 + self.imag**2

    def __eq__(self, other):
        if isinstance(other, int):
            return self.real == other and self.imag == 0
        return self.real == other.real and self.imag == other.imag
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        if self.imag >= 0:
            return f"{self.real} + {self.imag}i"
        else:
            return f"{self.real} - {-self.imag}i"

    def __str__(self):
        return self.__repr__()

    def conj(self):
        return GaussianInt(self.real, -self.imag)

    def __divmod__(self, other):
        # Division in Z[i]
        # A/B = (A * B_conj) / N(B)
        # Round to nearest integer
        if isinstance(other, int):
             other = GaussianInt(other, 0)
             
        num = self * other.conj()
        denom = other.norm()
        
        # Rounding logic using integer arithmetic to avoid float overflow
        # q = round(n/d) approx (2n + d) // (2d)
        
        def round_div(n, d):
            return (2 * n + d) // (2 * d)

        q_real = round_div(num.real, denom)
        q_imag = round_div(num.imag, denom)
        
        q = GaussianInt(q_real, q_imag)
        r = self - other * q
        return q, r

    def __mod__(self, other):
        _, r = divmod(self, other)
        return r

def gcd_gaussian(a, b):
    # Ensure inputs are GaussianInt
    if isinstance(a, int): a = GaussianInt(a)
    if isinstance(b, int): b = GaussianInt(b)
    
    while b.norm() != 0:
        _, r = divmod(a, b)
        a = b
        b = r
    return a

def xgcd_gaussian(a, b):
    # Extended Euclidean Algorithm
    # Returns (g, x, y) such that ax + by = g
    if isinstance(a, int): a = GaussianInt(a)
    if isinstance(b, int): b = GaussianInt(b)

    x0, x1, y0, y1 = GaussianInt(1), GaussianInt(0), GaussianInt(0), GaussianInt(1)
    while b.norm() != 0:
        q, r = divmod(a, b)
        a, b = b, r
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def mod_pow_gaussian(base, exp, mod):
    # base^exp % mod
    if isinstance(base, int): base = GaussianInt(base)
    
    result = GaussianInt(1)
    # Handle integer exponent
    if isinstance(exp, int):
        while exp > 0:
            if exp % 2 == 1:
                result = (result * base) % mod
            base = (base * base) % mod
            exp //= 2
        return result
    else:
        raise ValueError("Exponent should be integer")

def mod_inverse_gaussian(a, m):
    # Find x such that ax = 1 (mod m)
    # ax + my = 1
    g, x, y = xgcd_gaussian(a, m)
    if g.norm() != 1:
        # Check if g is a unit (1, -1, i, -i)
        # If g is a unit, say 'u', then u * u^-1 = 1.
        # We have a*x + m*y = u.
        # Multiply by u^-1: a*(x*u^-1) + m*(y*u^-1) = 1.
        # So inverse is x * u^-1.
        if g.norm() == 1: # Unit check
             return (x * g.conj()) % m # Inverse of unit is its conjugate
        
        raise ValueError(f"Modular inverse does not exist (GCD norm = {g.norm()})")
    return x % m
