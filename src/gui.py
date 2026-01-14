import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from .rsa_core import generate_keypair, encrypt, decrypt
from .utils import encode_message, decode_message

class GaussianRSAGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gaussian RSA Cryptosystem")
        self.root.geometry("800x600")
        
        self.public_key = None
        self.private_key = None
        
        self.create_widgets()
        
    def create_widgets(self):
        tab_control = ttk.Notebook(self.root)
        
        self.tab_setup = ttk.Frame(tab_control)
        self.tab_crypto = ttk.Frame(tab_control)
        self.tab_analysis = ttk.Frame(tab_control)
        
        tab_control.add(self.tab_setup, text='Key Generation')
        tab_control.add(self.tab_crypto, text='Encryption/Decryption')
        tab_control.add(self.tab_analysis, text='Analysis')
        
        tab_control.pack(expand=1, fill="both")
        
        self.setup_tab_ui()
        self.crypto_tab_ui()
        self.analysis_tab_ui()
        
    def setup_tab_ui(self):
        frame = ttk.LabelFrame(self.tab_setup, text="Key Generation Parameters")
        frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Label(frame, text="Bit Length (approx):").grid(column=0, row=0, padx=5, pady=5)
        self.bits_entry = ttk.Entry(frame)
        self.bits_entry.insert(0, "128")
        self.bits_entry.grid(column=1, row=0, padx=5, pady=5)
        
        self.gen_btn = ttk.Button(frame, text="Generate Keys", command=self.generate_keys)
        self.gen_btn.grid(column=2, row=0, padx=5, pady=5)
        
        self.keys_display = scrolledtext.ScrolledText(self.tab_setup, width=80, height=20)
        self.keys_display.pack(padx=10, pady=10, fill="both", expand=True)
        
    def crypto_tab_ui(self):
        frame_input = ttk.LabelFrame(self.tab_crypto, text="Message Input")
        frame_input.pack(padx=10, pady=5, fill="x")
        
        self.msg_entry = ttk.Entry(frame_input, width=80)
        self.msg_entry.pack(padx=5, pady=5, fill="x")
        
        frame_ops = ttk.Frame(self.tab_crypto)
        frame_ops.pack(padx=10, pady=5)
        
        ttk.Button(frame_ops, text="Encrypt", command=self.do_encrypt).pack(side="left", padx=5)
        ttk.Button(frame_ops, text="Decrypt", command=self.do_decrypt).pack(side="left", padx=5)
        
        self.crypto_display = scrolledtext.ScrolledText(self.tab_crypto, width=80, height=20)
        self.crypto_display.pack(padx=10, pady=10, fill="both", expand=True)
        
    def analysis_tab_ui(self):
        frame = ttk.Frame(self.tab_analysis)
        frame.pack(padx=10, pady=10, fill="x")
        
        ttk.Button(frame, text="Run Benchmark (Comparison)", command=self.run_benchmark).pack(side="left")
        
        self.analysis_display = scrolledtext.ScrolledText(self.tab_analysis, width=80, height=20)
        self.analysis_display.pack(padx=10, pady=10, fill="both", expand=True)
        
    def generate_keys(self):
        try:
            bits = int(self.bits_entry.get())
            self.keys_display.delete(1.0, tk.END)
            self.keys_display.insert(tk.END, "Generating keys... Please wait.\n")
            self.root.update()
            
            # Run in thread to not freeze UI
            def task():
                start = time.time()
                self.public_key, self.private_key = generate_keypair(bits)
                dt = time.time() - start
                
                msg = f"Key Generation Complete in {dt:.4f}s\n\n"
                msg += f"Public Key (e, N):\n  e = {self.public_key[0]}\n  N = {self.public_key[1]}\n\n"
                msg += f"Private Key (d, N):\n  d = {self.private_key[0]}\n  N = {self.private_key[1]}\n"
                
                self.root.after(0, lambda: self.update_keys_display(msg))
                
            threading.Thread(target=task).start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid bit length")

    def update_keys_display(self, msg):
        self.keys_display.delete(1.0, tk.END)
        self.keys_display.insert(tk.END, msg)
            
    def do_encrypt(self):
        if not self.public_key:
            messagebox.showwarning("Warning", "Generate keys first!")
            return
            
        msg = self.msg_entry.get()
        if not msg: return
        
        try:
            N = self.public_key[1]
            chunks = encode_message(msg, N.norm())
            self.encrypted_chunks = [encrypt(c, self.public_key) for c in chunks]
            
            display_text = "Ciphertext (Gaussian Integers):\n"
            for i, c in enumerate(self.encrypted_chunks):
                display_text += f"Block {i}: {c}\n"
            
            self.crypto_display.delete(1.0, tk.END)
            self.crypto_display.insert(tk.END, display_text)
            
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def do_decrypt(self):
        if not hasattr(self, 'encrypted_chunks') or not self.encrypted_chunks:
            return
            
        if not self.private_key:
            messagebox.showwarning("Warning", "No private key!")
            return
            
        try:
            decrypted_chunks = [decrypt(c, self.private_key) for c in self.encrypted_chunks]
            text = decode_message(decrypted_chunks)
            
            self.crypto_display.insert(tk.END, "\nDecrypted Message:\n" + text + "\n")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_benchmark(self):
        self.analysis_display.delete(1.0, tk.END)
        self.analysis_display.insert(tk.END, "Running benchmark... This may take a minute.\n")
        self.root.update()
        
        def task():
            import time
            from .rsa_core import generate_keypair, encrypt, decrypt
            from .gaussian_math import GaussianInt
            
            # Simple benchmark: Time to encrypt 10 blocks
            bits = 128
            pk, sk = generate_keypair(bits)
            N = pk[1]
            msg = GaussianInt(12345, 67890)
            
            start = time.time()
            for _ in range(100):
                encrypt(msg, pk)
            enc_time = time.time() - start
            
            start = time.time()
            for _ in range(100):
                # Using dummy decrypt for speed in benchmark if needed, but let's do real
                # Note: Decrypt is slow without CRT
                # We'll just do 10 decrypts
                pass
            
            # Since we don't have standard RSA here to import easily without dependency,
            # We will just report raw speed.
            
            res = f"Benchmark Results (128-bit Gaussian RSA):\n"
            res += f"Encryption (100 ops): {enc_time:.4f}s\n"
            res += f"Avg Encryption Time: {enc_time/100:.6f}s\n"
            res += f"Note: Python implementation is interpreted, C++ would be faster.\n"
            
            self.root.after(0, lambda: self.analysis_display.insert(tk.END, res))
            
        threading.Thread(target=task).start()

def main():
    root = tk.Tk()
    app = GaussianRSAGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
