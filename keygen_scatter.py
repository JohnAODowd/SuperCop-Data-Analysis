import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define substrings to filter lines
KEYPAIR_CYCLES_SUBSTRING = "/constbranchindex keypair_cycles"
KEYPAIR_CYCLES_SUBSTRING2 = "/timingleaks keypair_cycles"

input_filename = 'data'  # SUPERCOP Data

# Crypto categories
crypto_signs = ["dilithium2", "dilithium3", "dilithium5", "ed25519"]
crypto_signs2 = ["sphincs256", "falcon512dyn", "ronald512"]

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

# Plot the data
plt.figure(figsize=(10, 6))

# Iterate over unique crypto_sign values
for crypto in df["crypto_sign"].unique():
    subset = df[df["crypto_sign"] == crypto]["numbers"].explode()
    
    if subset.dropna().empty:  # Avoid errors if subset is empty
        continue
    
    subset = subset.dropna().astype(int).reset_index(drop=True)
    plt.plot(subset.index, subset.values, marker='o', linestyle='-', label=crypto)

# Labels and title
plt.xlabel("Measurement")
plt.ylabel("Key Generation (CPU Cycles)")
plt.title("Key Generation Performance (Outliers Removed)")
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
