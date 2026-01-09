import pandas as pd
import os

print("CSV File Merger")
print("=" * 50)

# Get CSV file names from user
print("\nEnter the names of CSV files to merge (one per line).")
print("Press Enter on an empty line when done:")

csv_files = []
while True:
    filename = input(f"File {len(csv_files) + 1}: ").strip()
    if not filename:
        break
    csv_files.append(filename)

if not csv_files:
    print("No files entered. Exiting.")
    exit()

print(f"\nFiles to merge ({len(csv_files)}):")
for f in csv_files:
    print(f"  - {f}")

# Get output filename from user
output_file = input("\nEnter name for merged output file (default: merged_output.csv): ").strip()
if not output_file:
    output_file = "merged_output.csv"
    print(f"Using default: {output_file}")
elif not output_file.endswith('.csv'):
    output_file += '.csv'
    print(f"Added .csv extension: {output_file}")

print("\nProcessing files...")

# Read and merge all CSV files
dfs = []
for file in csv_files:
    try:
        if not os.path.exists(file):
            print(f"Warning: File not found - {file}")
            continue
        df = pd.read_csv(file)
        dfs.append(df)
        print(f"✓ Loaded {file}: {len(df)} rows, {len(df.columns)} columns")
    except Exception as e:
        print(f"✗ Error reading {file}: {e}")

if not dfs:
    print("\nNo data loaded successfully. Exiting.")
    exit()

# Merge all dataframes
merged_df = pd.concat(dfs, ignore_index=True)

# Save merged data
try:
    merged_df.to_csv(output_file, index=False)
    print(f"\n{'=' * 50}")
    print(f"SUCCESS! Merge complete!")
    print(f"Total rows: {len(merged_df)}")
    print(f"Total columns: {len(merged_df.columns)}")
    print(f"Output saved to: {output_file}")
    print(f"{'=' * 50}")
except Exception as e:
    print(f"\nError saving output file: {e}")