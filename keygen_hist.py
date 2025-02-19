import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define substrings to filter lines
KEYPAIR_CYCLES_SUBSTRING = "/constbranchindex keypair_cycles"
KEYPAIR_CYCLES_SUBSTRING2 = "/timingleaks keypair_cycles"

input_filename = 'data'  # SUPERCOP Data

# Crypto categories
crypto_signs = [""]
crypto_signs2 = ["sphincsf128harakarobust", "sphincsf192harakarobust", "sphincsf256harakarobust", "sphincsf128harakasimple", "sphincsf192harakasimple", "sphincsf256harakasimple"]


# Generate substrings for filtering
subs = [sign + KEYPAIR_CYCLES_SUBSTRING for sign in crypto_signs]
subs2 = [sign + KEYPAIR_CYCLES_SUBSTRING2 for sign in crypto_signs2]
## substrings_to_check = subs + sub2
substrings_to_check = subs2  

# Function to filter lines containing specific substrings
def filter_lines(input_file, substrings):
    df = pd.read_csv(input_file, header=None, names=["line"], dtype=str, engine='c', on_bad_lines='skip')
    mask = df["line"].str.contains('|'.join(substrings), na=False, regex=True)
    return df[mask]

# Function to extract crypto_sign and corresponding numbers
def extract_info(line):
    for crypto in crypto_signs2:  # Check both lists
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

# Rename the column
median_values.columns = ["crypto_sign", "median_value"]

# Plot histogram
plt.figure(figsize=(8, 5))
plt.bar(median_values["crypto_sign"], median_values["median_value"], color=["blue", "green", "red", "orange", "brown", "purple"])

# Labels and title
plt.xlabel("Falcon Algorithm")
plt.ylabel("Key Generation (CPU Cycles)")
plt.title("Median Key Generation Time of Sphincs (Haraka)")
plt.xticks(rotation=20)
plt.grid(axis="y", linestyle="--", alpha=0.7)

# Show the plot
plt.show()
