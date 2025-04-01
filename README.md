# SuperCop Data Analysis
> This tool analyzes performance metrics (such as signing, verifying and key generation speed) of cryptographic algorithms submitted to the NIST PQC standardization project, as recorded in SuperCop benchmarking data. 

Post-quantum cryptography aims to develop cryptographic algorithms that remain secure against attacks from powerful quantum computers. As part of this effort, the **National Institute of Standards and Technology (NIST)** has defined five distinct security levels (1-5) to categorise the robustness of these algorithms against both classical and quantum computational threats.

The SuperCop benchmarking suite is widely used to evaluate the performance of these algorithms, providing key metrics such as speed (measured in CPU cycles), memory consumption, key sizes, ciphertext sizes, and operation times for various cryptographic tasks, including key generation, signing, and verification.

This tool ingests raw data from the SuperCop output, parses relevant information, and organize it systematically to provide users with a detailed analysis of the performance of each algorithm. It categorises algorithms based on their NIST security level, allowing users to evaluate how algorithms of similar strength perform relative to one another.

Each file in this repository corresponds to a different operation type:
- **keygen.py**: Time (CPU cycles) to generate a key pair: a secret key and a corresponding public key.
- **sign_short.py**: Time to sign a short message (1 - 453 bytes).
- **sign_long.py**: Time to sign a long message (567 - 96397 bytes).
- **verify_short.py**: Time to open a signed short message (1 - 453 bytes).
- **verify_long.py**: Time to open a signed long message (567 - 96397 bytes).

These tools are created with Python using libraries like [pandas](https://pandas.pydata.org/) for data handling and [NumPy](https://numpy.org/) for numerical analysis.

## Creating the SuperCop data file

> [!NOTE]
> A sample **data.gz** file is available [here](https://drive.google.com/file/d/1Lqis7PBvsp7TPa8GCx_R695ExA-KtHCX/view?usp=drive_link).

Generate a SuperCop data file:

```sh
wget https://bench.cr.yp.to/supercop/supercop-20250307.tar.xz
unxz < supercop-20250307.tar.xz | tar -xf -
cd supercop-20250307
nohup sh do &
```

If interrupts (an incoming network packet, for example, or for an operating-system clock tick) are frequent enough to interrupt 25% or more of the computations, there may be issues in generating this data file. The most common way for this to happen is for the same CPU core to be busy doing something else. **It is thus recommended to run SuperCop on an idle machine.** 

Unzip the resulting data.gz file:

```sh
gzip -d supercop-data/*/data.gz
```

Copy the data file to the local directory:
```sh
cp ./supercop-data/*/data ./data
```

## Setting up the virtual environment

Create a Python 3 virtual environment:

```sh
python -m venv project-venv

```

Activate the virtual environment:

```sh
source project-venv/bin/activate
```

Install the required packages:

```sh
pip install -r requirements.txt
```

## Example Usage

Compare key generation speed of all Level 3 PQC algorithms:

```sh
python3 keygen.py nistlevel3
```

Plot the key generation speed of all Level 5 PQC algorithms:

```sh
python3 keygen.py nistlevel5 plot
```

Compare signing time for short messages of all Level 1 PQC algorithms:

```sh
python3 sign_short.py nistlevel1
```

Plot the signing time for long messages of all Level 3 PQC algorithms:

```sh
python3 sign_long.py nistlevel3 plot
```

Compare verifying time for short messages of all Level 1 PQC algorithms:

```sh
python3 verify_short.py nistlevel1
```

Plot the verifying time for long messages of all Level 5 PQC algorithms:

```sh
python3 verify_long.py nistlevel5 plot
```
