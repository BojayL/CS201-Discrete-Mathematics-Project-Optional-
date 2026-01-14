# Gaussian RSA Project / 高斯 RSA 项目

## Overview / 概述

This project implements the RSA cryptosystem over the ring of Gaussian Integers $\mathbb{Z}[i]$.
本项目实现了基于高斯整数环 $\mathbb{Z}[i]$ 的 RSA 加密系统。

## Structure / 结构

- `src/`: Source code / 源代码
  - `gaussian_math.py`: Gaussian Integer arithmetic / 高斯整数运算
  - `rsa_core.py`: RSA KeyGen, Encrypt, Decrypt / RSA 核心逻辑
  - `gui.py`: Graphical User Interface / 图形用户界面
  - `utils.py`: Text encoding utilities / 文本编码工具
- `analysis/`: Analysis scripts / 分析脚本
  - `benchmark.py`: Performance comparison / 性能对比
- `report/`: Project Report / 项目报告
  - `report.md`: Bilingual report / 双语报告

## How to Run / 如何运行

### Prerequisites / 前置要求

- Python 3.x
- Tkinter (usually included with Python)

### Start GUI / 启动界面

Run the main script from the project root:
在项目根目录下运行主脚本：

```bash
python main.py
```

### Run Benchmark / 运行基准测试

```bash
python analysis/benchmark.py
```

## Features / 功能

- **Key Generation**: Generates large Gaussian Primes (Split and Inert types).
- **Encryption/Decryption**: Full RSA cycle on the complex plane.
- **Analysis**: Compare performance with standard Integer RSA.
