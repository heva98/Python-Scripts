import pandas as pd

# Get file names from user
file1 = input("Enter the name of the first CSV file (to be updated): ")
file2 = input("Enter the name of the second CSV file (source data): ")

# Read both CSV files
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Strip whitespace from column names in both dataframes
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Display available columns
print("\nAvailable columns in both files:")
print(df1.columns.tolist())

# Get matching column name
print("\nEnter the column name to use for matching (e.g., 'SMPS: School Id'):")
match_column = input().strip()

# Get columns to update
print("\nEnter the column names to update (comma-separated):")
print("Example: Regions, Councils, Wards, Street/Villages")
columns_input = input().strip()
columns_to_update = [col.strip() for col in columns_input.split(',')]

# Check for duplicates in the matching column of df2
duplicates = df2[match_column].duplicated().sum()
if duplicates > 0:
    print(f"\nWarning: Found {duplicates} duplicate values in '{match_column}' in the source file.")
    print("Keeping only the first occurrence of each duplicate.")
    df2 = df2.drop_duplicates(subset=[match_column], keep='first')

# Create a mapping dictionary from df2 using the match column as key
# Only include the columns we want to update
try:
    lookup_dict = df2.set_index(match_column)[columns_to_update].to_dict('index')
except KeyError as e:
    print(f"\nError: Column {e} not found in the source file.")
    print("Please check the column names and try again.")
    exit()

# Function to update row based on matching column
def update_row(row):
    match_value = row[match_column]
    if match_value in lookup_dict:
        for col in columns_to_update:
            row[col] = lookup_dict[match_value][col]
    return row

# Apply the update function to each row
df1_updated = df1.apply(update_row, axis=1)

# Get output file name
output_file = input("\nEnter the output file name (e.g., output.csv): ")

# Save the updated dataframe to a new CSV file
df1_updated.to_csv(output_file, index=False)

print(f"\nData merge completed successfully!")
print(f"Total rows processed: {len(df1_updated)}")
print(f"Rows updated: {len(df1[df1[match_column].isin(df2[match_column])])}")
print(f"Output saved to: {output_file}")