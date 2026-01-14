import time
import sys
import os

# Add parent directory to path to import src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rsa_core import generate_keypair as gen_gauss, encrypt as enc_gauss, generate_rational_prime
from src.gaussian_math import GaussianInt

# Trivial Integer RSA for comparison
def gen_rsa(bits):
    p = generate_rational_prime(bits // 2)
    q = generate_rational_prime(bits // 2)
    while p == q:
        q = generate_rational_prime(bits // 2)
    n = p * q
    phi = (p-1)*(q-1)
    e = 65537
    try:
        d = pow(e, -1, phi)
    except ValueError:
        # If gcd(e, phi) != 1, just regenerate (lazy way for benchmark)
        return gen_rsa(bits)
    return (e, n), (d, n)

def enc_rsa(m, pk):
    e, n = pk
    return pow(m, e, n)

def run():
    print("Gaussian RSA vs Standard RSA Benchmark")
    print("======================================")
    
    bits_list = [64, 128, 256]
    
    for bits in bits_list:
        print(f"\n--- Bit Length: {bits} ---")
        
        # Gaussian
        start = time.time()
        pk_g, _ = gen_gauss(bits)
        t_gen_g = time.time() - start
        
        # Standard
        start = time.time()
        pk_s, _ = gen_rsa(bits)
        t_gen_s = time.time() - start
        
        print(f"Key Generation:")
        print(f"  Gaussian: {t_gen_g:.4f}s")
        print(f"  Standard: {t_gen_s:.4f}s")
        
        # Encryption (100 operations)
        msg_g = GaussianInt(12345, 12345)
        msg_s = 1234512345
        
        start = time.time()
        for _ in range(100):
            enc_gauss(msg_g, pk_g)
        t_enc_g = time.time() - start
        
        start = time.time()
        for _ in range(100):
            enc_rsa(msg_s, pk_s)
        t_enc_s = time.time() - start
        
        print(f"Encryption (100 ops):")
        print(f"  Gaussian: {t_enc_g:.4f}s")
        print(f"  Standard: {t_enc_s:.4f}s")
        if t_enc_s > 0:
            print(f"  Slowdown: {t_enc_g/t_enc_s:.2f}x")

if __name__ == "__main__":
    run()
