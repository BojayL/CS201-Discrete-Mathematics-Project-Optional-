import random
import math
from .gaussian_math import GaussianInt, mod_pow_gaussian, mod_inverse_gaussian

def is_prime_miller_rabin(n, k=40):
    if n == 2: return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_rational_prime(bits):
    while True:
        n = random.getrandbits(bits)
        if n % 2 == 0: n += 1
        if is_prime_miller_rabin(n):
            return n

def legendre_symbol(a, p):
    return pow(a, (p - 1) // 2, p)

def tonelli_shanks(n, p):
    # Solves x^2 = n (mod p)
    if legendre_symbol(n, p) != 1:
        return None
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return pow(n, (p + 1) // 4, p)
    for z in range(2, p):
        if p - 1 == legendre_symbol(z, p):
            c = pow(z, q, p)
            break
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    while (t - 1) % p != 0:
        t2 = (t * t) % p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r

def decompose_prime(p):
    # p = 1 mod 4. Find a+bi such that a^2+b^2=p
    # Step 1: Find r such that r^2 = -1 mod p
    r = tonelli_shanks(-1, p)
    
    # Step 2: Euclidean algorithm variant
    # reduction until remainder < sqrt(p)
    a, b = p, r
    root_p = int(p**0.5)
    while b > root_p:
        a, b = b, a % b
    
    # Now b is one component, find the other
    # p = b^2 + c^2
    c = int((p - b*b)**0.5)
    return GaussianInt(b, c)

def generate_gaussian_prime(bits):
    # Generates a Gaussian prime with norm approx 2^bits.
    # Note: If we pick p ~ 2^bits (1 mod 4), N(pi) = p ~ 2^bits.
    # If we pick p ~ 2^(bits/2) (3 mod 4), N(p) = p^2 ~ 2^bits.
    
    if random.random() < 0.5:
        # Type 3 mod 4 (Inert)
        # We need p^2 to be around 2^bits, so p around 2^(bits/2)
        p_bits = max(bits // 2, 2)
        while True:
            p = generate_rational_prime(p_bits)
            if p % 4 == 3:
                return GaussianInt(p, 0)
    else:
        # Type 1 mod 4 (Split)
        # We need p to be around 2^bits
        while True:
            p = generate_rational_prime(bits)
            if p % 4 == 1:
                return decompose_prime(p)

def generate_keypair(bits=128):
    # bits is roughly the bit length of the modulus N.
    # So pi and rho should have norm approx 2^(bits/2).
    prime_bits = bits // 2
    
    pi = generate_gaussian_prime(prime_bits)
    rho = generate_gaussian_prime(prime_bits)
    
    # Ensure distinct
    while pi == rho:
        rho = generate_gaussian_prime(prime_bits)
        
    N = pi * rho
    
    # phi(N) = (N(pi)-1)(N(rho)-1)
    phi_N = (pi.norm() - 1) * (rho.norm() - 1)
    
    e = 65537
    while math.gcd(e, phi_N) != 1:
        e += 2
        
    d = pow(e, -1, phi_N)
    
    return ((e, N), (d, N))

def encrypt(message_int, public_key):
    e, N = public_key
    return mod_pow_gaussian(message_int, e, N)

def decrypt(ciphertext_int, private_key):
    d, N = private_key
    return mod_pow_gaussian(ciphertext_int, d, N)
