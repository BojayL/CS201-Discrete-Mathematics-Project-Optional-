import math
from .gaussian_math import GaussianInt

def bytes_to_int(b):
    return int.from_bytes(b, 'big')

def int_to_bytes(i):
    if i == 0: return b'\x00'
    return i.to_bytes((i.bit_length() + 7) // 8, 'big')

def encode_message(message, N_norm):
    """
    Encodes a string message into a list of Gaussian Integers.
    N_norm is the norm of the modulus N.
    """
    # Max bits we can safely store in a Gaussian integer M such that M is recoverable.
    # We want M to be in the "main" residue class.
    # Conservatively, if |real| < sqrt(N_norm)/2 and |imag| < sqrt(N_norm)/2,
    # then N(M) < N_norm/2, which is safe for simple modulo reduction usually.
    
    total_bits = N_norm.bit_length()
    # We take a safety margin.
    # We want r, i to be roughly total_bits / 2 length.
    
    half_bits = (total_bits // 2) - 8 # -8 for safety padding
    if half_bits < 8:
        half_bits = 8 # Minimum
        
    chunk_size = half_bits // 8 # bytes per component
    if chunk_size < 1:
        chunk_size = 1
        
    # We will put text in both real and imag parts to double capacity?
    # Or just Text -> Real, Random -> Imag?
    # Let's do Text -> Real, Text -> Imag to be efficient.
    
    message_bytes = message.encode('utf-8')
    gaussian_chunks = []
    
    i = 0
    while i < len(message_bytes):
        # Real part
        real_chunk = message_bytes[i : i + chunk_size]
        i += chunk_size
        r_val = bytes_to_int(real_chunk)
        
        # Imag part
        if i < len(message_bytes):
            imag_chunk = message_bytes[i : i + chunk_size]
            i += chunk_size
            i_val = bytes_to_int(imag_chunk)
        else:
            i_val = 0
            
        gaussian_chunks.append(GaussianInt(r_val, i_val))
        
    return gaussian_chunks

def decode_message(gaussian_chunks):
    """
    Decodes a list of Gaussian Integers back to string.
    """
    decoded_bytes = bytearray()
    
    for g in gaussian_chunks:
        # Real part
        if g.real != 0:
            r_bytes = int_to_bytes(g.real)
            decoded_bytes.extend(r_bytes)
        
        # Imag part
        if g.imag != 0:
            i_bytes = int_to_bytes(g.imag)
            decoded_bytes.extend(i_bytes)
            
    try:
        return decoded_bytes.decode('utf-8')
    except UnicodeDecodeError:
        return decoded_bytes.decode('utf-8', errors='replace')
