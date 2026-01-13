import pandas as pd

# File paths (files are in same folder as script)
file1 = input("Enter the filename for first CSV (e.g., tool-4-under-5.csv): ")
file2 = input("Enter the filename for second CSV (e.g., enrollments.csv): ")

# Read the CSV files
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

print("\n=== Columns in tool-4-under-5.csv ===")
for i, col in enumerate(df1.columns):
    print(f"{i}: {col}")

print("\n=== Columns in enrollments.csv ===")
for i, col in enumerate(df2.columns):
    print(f"{i}: {col}")

# Get column names from user
print("\n=== Enter column names ===")
village_id_col = input("Enter the name of the Village ID column (SMPS 4 : Namba Ya Utambulisho Wa Kijiji): ")
national_col = input("Enter the name of the National column: ")
regions_col = input("Enter the name of the Regions column: ")
councils_col = input("Enter the name of the Councils column: ")
wards_col = input("Enter the name of the Wards column: ")

# Which file has the data to fill FROM?
print("\nWhich file contains the complete location data (National, Regions, Councils, Wards)?")
print("1: tool-4-under-5.csv")
print("2: enrollments.csv")
source_choice = input("Enter 1 or 2: ")

if source_choice == "1":
    source_df = df1
    target_df = df2
    target_file = "enrollments.csv"
else:
    source_df = df2
    target_df = df1
    target_file = "tool-4-under-5.csv"

# Create a mapping from village ID to location data
location_mapping = source_df[[village_id_col, national_col, regions_col, councils_col, wards_col]].drop_duplicates()

# Merge the data
# First, store original columns that might get overwritten
target_df_backup = target_df.copy()

# Merge to fill missing values
merged_df = target_df.merge(
    location_mapping,
    on=village_id_col,
    how='left',
    suffixes=('', '_new')
)

# Fill empty/null values in target with values from source
for col in [national_col, regions_col, councils_col, wards_col]:
    new_col = f"{col}_new"
    if new_col in merged_df.columns:
        # Fill null or empty values
        merged_df[col] = merged_df[col].fillna(merged_df[new_col])
        merged_df[col] = merged_df.apply(
            lambda row: row[new_col] if pd.isna(row[col]) or str(row[col]).strip() == '' else row[col],
            axis=1
        )
        # Drop the temporary column
        merged_df = merged_df.drop(columns=[new_col])

# Save the result
output_file = f"updated_{target_file}"
merged_df.to_csv(output_file, index=False)

print(f"\n✓ Successfully merged data!")
print(f"✓ Output saved to: {output_file}")
print(f"\nRows processed: {len(merged_df)}")
print(f"Unique Village IDs: {merged_df[village_id_col].nunique()}")