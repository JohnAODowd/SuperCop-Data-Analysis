# SuperCop Data Analysis
> A data analysis tool designed to be used with a SuperCop data file. 

## Creating the SuperCop data file

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

## If you are unable to generate a SuperCop data file...

A sample data.gz file is available [here](https://drive.google.com/file/d/1Lqis7PBvsp7TPa8GCx_R695ExA-KtHCX/view?usp=drive_link).

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

## Usage

```sh
python3 keygen.py nistlevel1
python3 keygen.py nistlevel2
python3 keygen.py nistlevel3
python3 keygen.py nistlevel5
```

```sh
python3 keygen.py nistlevel1 plot
python3 keygen.py nistlevel2 plot
python3 keygen.py nistlevel3 plot
python3 keygen.py nistlevel5 plot
```

```sh
python3 sign_short.py nistlevel1 
python3 sign_short.py nistlevel2 
python3 sign_short.py nistlevel3 
python3 sign_short.py nistlevel5
```

```sh
python3 sign_short.py nistlevel1 plot
python3 sign_short.py nistlevel2 plot
python3 sign_short.py nistlevel3 plot
python3 sign_short.py nistlevel5 plot
```


```sh
python3 sign_long.py nistlevel1 
python3 sign_long.py nistlevel2 
python3 sign_long.py nistlevel3 
python3 sign_long.py nistlevel5
```

```sh
python3 sign_long.py nistlevel1 plot
python3 sign_long.py nistlevel2 plot
python3 sign_long.py nistlevel3 plot
python3 sign_long.py nistlevel5 plot
```

```sh
python3 verify_short.py nistlevel1 
python3 verify_short.py nistlevel2 
python3 verify_short.py nistlevel3 
python3 verify_short.py nistlevel5 
```

```sh
python3 verify_short.py nistlevel1 plot
python3 verify_short.py nistlevel2 plot
python3 verify_short.py nistlevel3 plot
python3 verify_short.py nistlevel5 plot
```

```sh
python3 verify_long.py nistlevel1 
python3 verify_long.py nistlevel2 
python3 verify_long.py nistlevel3 
python3 verify_long.py nistlevel5 
```

```sh
python3 verify_long.py nistlevel1 plot
python3 verify_long.py nistlevel2 plot
python3 verify_long.py nistlevel3 plot
python3 verify_long.py nistlevel5 plot
```
