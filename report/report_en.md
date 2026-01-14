# Project Report: Extending RSA Cryptography to the Ring of Gaussian Integers

**Student Name**: *******
**Course**: Discrete Mathematics  
**Date**: December 23, 2025

---

## Abstract
This project explores the intersection of Algebraic Number Theory and Cryptography by extending the classic RSA public-key cryptosystem from the ring of integers $\mathbb{Z}$ to the ring of Gaussian Integers $\mathbb{Z}[i]$. The primary goal was to investigate how cryptographic primitives behave in a quadratic extension field. We successfully designed and implemented a functional RSA-like scheme that operates entirely on the complex plane. The project includes a custom mathematical library for Gaussian arithmetic, a novel key generation algorithm utilizing Cornacchia’s algorithm for prime decomposition, and a graphical user interface. Our analysis confirms that while the mathematical hardness reduces to the standard integer factorization problem, the Gaussian variant offers a rich theoretical landscape and unique implementation challenges, specifically regarding prime generation and data encoding.

---

## 1. Introduction

### 1.1 Project Background
The RSA algorithm is arguably the most famous public-key cryptosystem in the world. Its security is founded on the difficulty of factoring large composite integers. In a standard Discrete Mathematics curriculum, we learn that RSA operates in the ring $\mathbb{Z}_N$. However, abstract algebra teaches us that $\mathbb{Z}$ is just one example of a Euclidean Domain.

This project was born out of a simple question: **"What happens if we replace the integers in RSA with complex numbers?"**

### 1.2 Problem Statement
The standard RSA algorithm is defined over real integers. Implementing it over complex numbers (specifically Gaussian Integers $a+bi$) presents several challenges:
1.  **Ordering**: Unlike integers, complex numbers do not have a natural ordering, which complicates concepts like "division with remainder".
2.  **Primes**: "Prime numbers" behave differently in $\mathbb{Z}[i]$. Some ordinary primes like 5 are no longer prime in $\mathbb{Z}[i]$ (since $5 = (1+2i)(1-2i)$).
3.  **Arithmetic**: Basic operations like GCD and modular exponentiation need to be redefined and implemented for complex numbers.

### 1.3 Project Objectives
The main objectives of this project are:
1.  To deeply understand the algebraic structure of $\mathbb{Z}[i]$ and its relation to $\mathbb{Z}$.
2.  To design a complete cryptosystem (KeyGen, Encrypt, Decrypt) that works natively with Gaussian Integers.
3.  To implement this system in Python, creating a usable tool with a GUI.
4.  To analyze the performance and security implications of this extension compared to the standard RSA.

---

## 2. Mathematical Theoretical Framework

To implement RSA in a new domain, we first had to establish the mathematical ground rules.

### 2.1 The Gaussian Integer Ring $\mathbb{Z}[i]$
The set of Gaussian integers is defined as $\mathbb{Z}[i] = \{a + bi \mid a, b \in \mathbb{Z}\}$.
It forms a **Euclidean Domain**, which is crucial because it means the **Euclidean Algorithm** (for finding GCD) still works. This is the fundamental requirement for RSA key generation.

**The Norm**:
To measure the "size" of a Gaussian integer, we use the Norm function:
$$ N(a+bi) = a^2 + b^2 $$
The norm has a vital property: it is **multiplicative**. $N(\alpha \beta) = N(\alpha)N(\beta)$. This allows us to map complex divisibility problems back to ordinary integer arithmetic.

### 2.2 Prime Classification (In-Depth)
Understanding "what makes a Gaussian integer prime" is central to this project. Unlike in $\mathbb{Z}$, where primes are simply "numbers divisible only by 1 and themselves," in $\mathbb{Z}[i]$, the concept is tied to the sum of two squares.

A Gaussian integer $\pi$ is prime if and only if it satisfies one of the following conditions:

1.  **Inert Primes ($p \equiv 3 \pmod 4$)**:
    *   **Definition**: These are rational primes that remain prime in the Gaussian ring.
    *   **Example**: $3$ is a prime in $\mathbb{Z}$. In $\mathbb{Z}[i]$, there are no integers $a, b$ such that $a^2+b^2=3$. Thus, 3 cannot be factored.
    *   **Properties**: Their norm is $p^2$. For example, $N(3) = 9$.

2.  **Split Primes ($p \equiv 1 \pmod 4$)**:
    *   **Definition**: These rational primes are **composite** in the Gaussian ring. They factor into two conjugate Gaussian primes: $p = \pi \bar{\pi}$.
    *   **Example**: Take $5$. Since $5 \equiv 1 \pmod 4$, Fermat's Theorem on Sums of Two Squares guarantees $5 = 1^2 + 2^2$. Thus, $5 = (1+2i)(1-2i)$. Here, $1+2i$ is the Gaussian prime.
    *   **Properties**: Their norm is $p$. For example, $N(1+2i) = 1^2+2^2 = 5$.

3.  **Ramified Prime (2)**:
    *   The number 2 is unique because it factors as $2 = (1+i)(1-i)$. Since $1-i = -i(1+i)$, these factors are associates. Effectively, 2 is the square of a prime unit.

**Visualization**: If we plot Gaussian primes on the complex plane, they do not form a random scatter. They exhibit symmetry (multiplication by $i$ rotates by 90 degrees). The "Gaussian Moat" problem asks if one can walk to infinity stepping only on primes with bounded steps; this illustrates the non-trivial distribution of these numbers.

### 2.3 The Generalized Euler Totient Function
Standard RSA relies on $\phi(N) = (p-1)(q-1)$. For Gaussian RSA, we needed a corresponding formula.
If $M = \pi \rho$ is the product of two Gaussian primes, the size of the multiplicative group modulo $M$ is given by:
$$ \Phi(M) = (N(\pi) - 1)(N(\rho) - 1) $$
This formula was derived by applying the Chinese Remainder Theorem to rings. It represents the number of invertible elements modulo $M$.

---

## 3. Algorithm Design

### 3.1 Key Generation Strategy
This was the most complex part of the design. We need two large Gaussian primes $\pi$ and $\rho$.
I implemented a hybrid strategy:
*   **Method A (Inert)**: Pick a random large integer prime $p$. If $p \equiv 3 \pmod 4$, then $\pi = p$ is a Gaussian prime.
*   **Method B (Split)**: Pick a random large integer prime $p \equiv 1 \pmod 4$. To find $\pi$, we need to write $p = a^2 + b^2$. I implemented the **Cornacchia-Smith algorithm** (a variant of the Euclidean algorithm) to efficiently solve for $a$ and $b$. Then $\pi = a+bi$.

**Algorithm Steps**:
1.  Generate $\pi$ and $\rho$ (approx 512 bits each).
2.  Compute Modulus $M = \pi \rho$. Note that $M$ is a complex number!
3.  Compute $\Phi(M) = (N(\pi)-1)(N(\rho)-1)$.
4.  Pick public exponent $e = 65537$.
5.  Calculate private key $d$ such that $ed \equiv 1 \pmod{\Phi(M)}$.

### 3.2 Encryption and Decryption
The core operations are identical to standard RSA, but performed in $\mathbb{Z}[i]$:
*   **Encrypt**: $C = P^e \pmod M$
*   **Decrypt**: $P = C^d \pmod M$

### 3.3 Data Encoding (The "Embedding" Problem)
A unique challenge in Gaussian RSA is: "How do we represent a text message as a complex number?"
In standard RSA, we just turn text into a big integer. In Gaussian RSA, we have a 2D plane.
**My Solution**: I designed a scheme that splits the message binary into two parts. One part becomes the real component, and the other becomes the imaginary component. This allows us to carry twice as much data per encryption operation compared to just using the real line, effectively utilizing the algebraic structure of the ring.

---

## 4. Implementation Details

The project was implemented in **Python 3**. I avoided using "black-box" crypto libraries for the core logic to ensure I implemented the mathematical algorithms myself.

*   **`gaussian_math.py`**: This is the engine room. I implemented a `GaussianInt` class that handles:
    *   Overloaded `+`, `-`, `*` operators.
    *   `divmod`: A custom division algorithm that rounds complex division to the nearest Gaussian integer to find the remainder.
    *   `xgcd`: The Extended Euclidean Algorithm adapted for complex numbers to find modular inverses.
*   **`rsa_core.py`**: Handles the prime generation and the encryption lifecycle.
*   **GUI**: A Tkinter-based interface was created to make the project interactive and demonstrable.

---

## 5. Analysis and Results

### 5.1 Complexity Analysis
Is Gaussian RSA efficient?
Theoretically, multiplying two complex numbers $(a+bi)(c+di)$ requires 4 integer multiplications (or 3 with optimization) and additions.
Therefore, we expect Gaussian RSA to be slower than standard RSA for the same modulus size.

### 5.2 Benchmark Results
I wrote a benchmark script to compare my implementation against a standard integer RSA implementation (also written in Python for fairness).
*   **Key Generation**: Slower, due to the need to decompose primes ($p=a^2+b^2$).
*   **Encryption**: Approx **5x slower**. This aligns with theory (complex arithmetic overhead + object creation overhead in Python).

### 5.3 Security Discussion
Does using Gaussian Integers make RSA more secure?
The security relies on the **Gaussian Integer Factorization Problem**.
$$ \text{Given } M, \text{ find } \pi, \rho \text{ such that } M = \pi \rho $$
However, since $N(M) = N(\pi)N(\rho)$, factoring $M$ in $\mathbb{Z}[i]$ is mathematically equivalent to factoring the integer $N(M)$ in $\mathbb{Z}$.
**Conclusion**: The "hardness" is the same as standard RSA. However, the system adds a layer of **obscurity**. An attacker seeing a complex modulus $M$ might be confused if they are only equipped with standard integer factorization tools. They would first need to understand the algebraic mapping to reduce it to a standard problem.

---

## 6. Project Usage Manual

To ensure the reproducibility of this project, I have included a detailed guide on how to install and run the software.

### 6.1 Prerequisites
The project relies on standard Python libraries.
*   **Python Version**: Python 3.8 or higher is recommended.
*   **Dependencies**: The project primarily uses the standard library (`math`, `random`, `tkinter`). No external `pip install` is required for the core functionality.

### 6.2 Running the Application
1.  **Launch the GUI**:
    Navigate to the project root directory in your terminal and run:
    ```bash
    python main.py
    ```
    This will open the "Gaussian RSA Cryptosystem" window.

2.  **Using the System**:
    * **Step 1: Key Generation**: Go to the "Key Generation" tab. Enter a bit length (e.g., 128 or 256) and click "Generate Keys". The system will display the generated complex Public Key $(e, N)$ and Private Key $(d, N)$.
    
      ![image-20251223233331479](/Users/bojay.l/Library/Application Support/typora-user-images/image-20251223233331479.png)

    * **Step 2: Encryption**: Switch to the "Encryption/Decryption" tab. Enter a text message (e.g., "Hello World") and click "Encrypt". The ciphertext will be shown as a list of Gaussian Integers.
    
    *   **Step 3: Decryption**: Click "Decrypt" to recover the original message from the ciphertext using the private key.
    
3.  **Running Benchmarks**:
    To see the performance comparison between Gaussian RSA and Standard RSA, run:
    ```bash
    python analysis/benchmark.py
    ```
    This script will execute encryption operations for various bit lengths and output the timing results to the console.
    
    <img src="/Users/bojay.l/Library/Application Support/typora-user-images/image-20251223233403206.png" alt="image-20251223233403206" style="zoom:50%;" />

---

## 7. Conclusion

This project successfully demonstrated that RSA is not limited to integers. By porting the algorithm to the Gaussian Integers, I gained a profound understanding of:
1.  **Abstract Algebra**: How concepts like "Prime", "GCD", and "Modulo" generalize.
2.  **Algorithmic Number Theory**: How to implement complex algorithms like Cornacchia’s method.
3.  **Cryptography Design**: The importance of precise mathematical definitions in security.

While Gaussian RSA is computationally more expensive and offers no theoretical security advantage over standard RSA, it serves as an excellent educational bridge to more advanced cryptographic systems (like Lattice-based cryptography) that rely on similar algebraic structures.

---
*End of Report*

