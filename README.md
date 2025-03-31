# SuperCop Data Analysis
This is a data analysis tool designed to be used with a SuperCop data file. 

## Setup the Project

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

Activate the virtual environment:

```sh
source env/bin/activate
```

Install the required packages:

```sh
pip install -r requirements.txt
```

