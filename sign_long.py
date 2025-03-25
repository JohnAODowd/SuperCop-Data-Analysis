import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Crypto categories
# crypto_signs = ["dilithium2", "dilithium3", "dilithium5"]
# crypto_signs = ["falcon512tree", "falcon512dyn", "falcon1024tree", "falcon1024dyn"]
# crypto_signs = ["sphincsf128harakarobust", "sphincsf192harakarobust", "sphincsf256harakarobust", "sphincsf128harakasimple", "sphincsf192harakasimple", "sphincsf256harakasimple"]
# crypto_signs = ["sphincsf128shake256robust", "sphincsf128shake256simple", "sphincsf192shake256robust", "sphincsf192shake256simple", "sphincsf256shake256robust", "sphincsf256shake256simple"]

# NIST Level 1
# crypto_signs = [""]
# crypto_signs2 = ["falcon512tree", "falcon512dyn", "sphincsf128harakarobust", "sphincsf128shake256robust", "sphincsf128shake256simple",  "sphincsf128harakasimple"]

# NIST Level 2
# crypto_signs = ["dilithium2"]
# crypto_signs2 = [""]

# NIST Level 3
crypto_signs = ["dilithium3"]
crypto_signs2 = ["sphincsf192harakarobust", "sphincsf192shake256robust", "sphincsf192shake256simple",  "sphincsf192harakasimple"]

# NIST Level 5
# crypto_signs = ["dilithium5"]
# crypto_signs2 = ["falcon1024tree", "falcon1024dyn", "sphincsf256harakarobust", "sphincsf256shake256robust", "sphincsf256shake256simple",  "sphincsf256harakasimple"]

# Byte sizes list
byte_sizes = [
567,
    709, 887, 1109, 1387,
    1734, 2232, 2711, 3389,
    4237, 5297, 6622, 8278,
    10348, 12936, 16171, 20214,
    25268, 31650, 39483, 49354,
    61693, 77117, 96397
]

'''
# Byte sizes list
byte_sizes = [
    0, 1, 2, 3, 4,
    6, 8, 11, 14,
    18, 23, 29, 37,
    47, 59, 74, 93,
    117, 147, 184, 231,
    289, 362, 453, 567,
    709, 887, 1109, 1387,
    1734, 2232, 2711, 3389,
    4237, 5297, 6622, 8278,
    10348, 12936, 16171, 20214,
    25268, 31650, 39483, 49354,
    61693, 77117, 96397
]
'''

# Define substring to filter lines
SIGN_CYCLES_SUBSTRING = "/constbranchindex cycles "
SIGN_CYCLES_SUBSTRING2 = "/timingleaks cycles "

# Generate regex pattern to match {sign} + {SIGN_CYCLES_SUBSTRING} + {size}
substrings_to_check = [f"{sign}{SIGN_CYCLES_SUBSTRING}{size}" for sign in crypto_signs for size in byte_sizes]
substrings_to_check += [f"{sign}{SIGN_CYCLES_SUBSTRING2}{size}" for sign in crypto_signs2 for size in byte_sizes]


# Function to filter lines containing specific substrings
def filter_lines(input_file, substrings):
    df = pd.read_csv(input_file, header=None, names=["line"], dtype=str, engine='c', on_bad_lines='skip')

    # Build regex pattern to match any combination of {sign} + {SIGN_CYCLES_SUBSTRING} + {size}
    pattern = "|".join(substrings)  # OR operation in regex

    # Apply regex filter
    mask = df["line"].str.contains(pattern, na=False, regex=True)

    return df[mask]

def extract_info(df):
    def parse_line(line):
        parts = line.split()
        
        # Find the crypto sign in the line
        crypto_sign = next((crypto for crypto in (crypto_signs + crypto_signs2) if crypto in line), None)
        if not crypto_sign:
            return pd.Series([None, None, np.array([])])

        # Locate the byte size (first match from byte_sizes)
        byte_size = None
        numbers = []
        for i, part in enumerate(parts):
            if part.isdigit():
                num = int(part)
                if num in byte_sizes and byte_size is None:  # First occurrence is byte_size
                    byte_size = num
                elif byte_size is not None:  # Numbers start after byte_size
                    numbers.append(num)

        return pd.Series([crypto_sign, byte_size, np.array(numbers)])

    # Apply parsing to each line
    df_filtered = df.apply(parse_line)

    # Rename columns appropriately
    df_filtered.columns = ["crypto_sign", "byte_sizes", "numbers"]

    # Group by 'crypto_sign' and 'byte_sizes', then concatenate numbers
    df_grouped = df_filtered.groupby(["crypto_sign", "byte_sizes"], as_index=False).agg({
        "numbers": lambda x: np.concatenate(x.values) if len(x) > 1 else x.values[0]
    })

    return df_grouped

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

def calc_medians(df):
    # Compute the median of the "numbers" array for each row
    df["median"] = df["numbers"].apply(lambda x: np.median(x) if len(x) > 0 else np.nan)

    # Select relevant columns for the output DataFrame
    return df[["crypto_sign", "byte_sizes", "median"]]


# Read and filter lines from file
input_filename = "data"
df_filtered = filter_lines(input_filename, substrings_to_check)

# Extract information into new columns
df_filtered = extract_info(df_filtered["line"])

# Apply outlier removal to the "numbers" column
df_filtered['numbers'] = df_filtered['numbers'].apply(remove_outliers)

# Calculate the median value for all measurements
df_medians = calc_medians(df_filtered)

def summarize_medians(df):
    summary_df = df.groupby('crypto_sign')['median'].median().reset_index()
    summary_df.rename(columns={'median': 'overall_median'}, inplace=True)
    return summary_df

print(summarize_medians(df_medians))


def plot_medians(df):

    # Create a figure and axis
    plt.figure(figsize=(10, 6))

    # Plot each crypto_sign with a different color
    for crypto in df["crypto_sign"].unique():
        subset = df[df["crypto_sign"] == crypto]
        plt.plot(subset["byte_sizes"], subset["median"], marker='o', linestyle='-', label=crypto)

    # Labels and title
    plt.xlabel("n-byte", fontsize=12)
    plt.ylabel("Median Time to Sign n-byte Message (CPU Cycles)", fontsize=12)
    plt.title("Median Signing Time vs. Message Size", fontsize=14)
    
    # Add legend
    plt.legend(title="Crypto Sign", fontsize=10)

    # Show plot
    plt.show()

