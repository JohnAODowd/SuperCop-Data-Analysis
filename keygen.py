import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

input_filename = 'data'  # SUPERCOP Data

# Crypto categories
# crypto_signs = ["dilithium2", "dilithium3", "dilithium5"]
# crypto_signs = ["falcon512tree", "falcon512dyn", "falcon1024tree", "falcon1024dyn"]
# crypto_signs = ["sphincsf128harakarobust", "sphincsf192harakarobust", "sphincsf256harakarobust", "sphincsf128harakasimple", "sphincsf192harakasimple", "sphincsf256harakasimple"]
# crypto_signs = ["sphincsf128shake256robust", "sphincsf128shake256simple", "sphincsf192shake256robust", "sphincsf192shake256simple", "sphincsf256shake256robust", "sphincsf256shake256simple"]

if "nistlevel1" in sys.argv:
    # NIST Level 1
    crypto_signs = [""]
    crypto_signs2 = ["falcon512tree", "falcon512dyn", "sphincsf128harakarobust", "sphincsf128shake256robust", "sphincsf128shake256simple",  "sphincsf128harakasimple"]

elif "nistlevel2" in sys.argv:
    # NIST Level 2
    crypto_signs = ["dilithium2"]
    crypto_signs2 = [""]

elif "nistlevel3" in sys.argv:
    # NIST Level 3
    crypto_signs = ["dilithium3"]
    crypto_signs2 = ["sphincsf192harakarobust", "sphincsf192shake256robust", "sphincsf192shake256simple",  "sphincsf192harakasimple"]

elif "nistlevel5" in sys.argv:
    # NIST Level 5
    crypto_signs = ["dilithium5"]
    crypto_signs2 = ["falcon1024tree", "falcon1024dyn", "sphincsf256harakarobust", "sphincsf256shake256robust", "sphincsf256shake256simple",  "sphincsf256harakasimple"]


# Define substrings to filter lines
KEYPAIR_CYCLES_SUBSTRING = "/constbranchindex keypair_cycles"
KEYPAIR_CYCLES_SUBSTRING2 = "/timingleaks keypair_cycles"

# Generate substrings for filtering
subs = [sign + KEYPAIR_CYCLES_SUBSTRING for sign in crypto_signs]
subs2 = [sign + KEYPAIR_CYCLES_SUBSTRING2 for sign in crypto_signs2]
substrings_to_check = subs + subs2

# Function to filter lines containing specific substrings
def filter_lines(input_file, substrings):
    df = pd.read_csv(input_file, header=None, names=["line"], dtype=str, engine='c', on_bad_lines='skip')
    mask = df["line"].str.contains('|'.join(substrings), na=False, regex=True)
    return df[mask]

# Function to extract crypto_sign and corresponding numbers
def extract_info(line):
    if crypto_signs2 == [""]:
        for crypto in crypto_signs:  # Check only cryptosigns
            if crypto in line:
                try:
                    numbers = np.array(line.split("-")[-1].split(), dtype=int)
                    return crypto, numbers
                except ValueError:
                    return crypto, np.array([])  # Return empty array if conversion fails
    elif crypto_signs == [""]:
        for crypto in crypto_signs2:  # Check only cryptosigns2
            if crypto in line:
                try:
                    numbers = np.array(line.split("-")[-1].split(), dtype=int)
                    return crypto, numbers
                except ValueError:
                    return crypto, np.array([])  # Return empty array if conversion fails
    else:
        for crypto in crypto_signs + crypto_signs2:  # Check both lists
            if crypto in line:
                try:
                    numbers = np.array(line.split("-")[-1].split(), dtype=int)
                    return crypto, numbers
                except ValueError:
                    return crypto, np.array([])  # Return empty array if conversion fails
    return None, np.array([])

# Function to remove outliers using the IQR method
def remove_outliers(arr):
    arr = np.array(arr)  # Ensure input is a NumPy array
    if arr.size == 0:  # Handle empty arrays
        return arr
    Q1, Q3 = np.percentile(arr, [25, 75])
    IQR = Q3 - Q1
    lower_fence = Q1 - 1.5 * IQR
    upper_fence = Q3 + 1.5 * IQR
    return arr[(arr >= lower_fence) & (arr <= upper_fence)]

# Read and filter lines from file
df = filter_lines(input_filename, substrings_to_check)

# Extract information into new columns
df[['crypto_sign', 'numbers']] = df['line'].apply(lambda x: pd.Series(extract_info(x)))

# Drop the original line column
df = df.drop(columns=['line'])

# Apply outlier removal to the "numbers" column
df['numbers'] = df['numbers'].apply(remove_outliers)

# Compute median values per crypto_sign
median_values = (
    df.explode("numbers")  # Flatten lists into rows
    .groupby("crypto_sign")["numbers"]
    .median()
    .reset_index()
)

#print(median_values)

# Rename the column
median_values.columns = ["crypto_sign", "median_value"]

print(median_values)

if "plot" in sys.argv:
    # Plot histogram
    plt.figure(figsize=(8, 5))
    plt.bar(median_values["crypto_sign"], median_values["median_value"], color=["blue", "green", "red", "orange", "brown", "purple"])

    # Labels and title
    plt.xlabel("Falcon Algorithm")
    plt.ylabel("Key Generation (CPU Cycles)")
    plt.title("Median Key Generation Time of NIST Security Level 3")
    plt.xticks(rotation=20)
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Show the plot
    plt.show()
