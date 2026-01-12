import pandas as pd

# Read both CSV files
print("Reading CSV files...")
df_general = pd.read_csv('tool-4-general.csv')
df_vyandarua = pd.read_csv('tool-4-vyandarua.csv')

# Strip whitespace from column names
df_general.columns = df_general.columns.str.strip()
df_vyandarua.columns = df_vyandarua.columns.str.strip()

# Define the matching column
match_column = 'SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'

# Columns to update from df_general to df_vyandarua
columns_to_update = [
    'SMPS 4: 119. Je, kaya yako ina vyandarua vya kuzuia mbu vinavyoweza kutumika wakati wa kulala?',
    'SMPS 4: 120. Je, kaya yako ina vyandarua vya kuzuia mbu vingapi?'
]

# Columns to copy when adding new rows (basic info columns)
basic_columns = ['National', 'Regions', 'Councils', 'Wards', 'Street/Villages', 'Tarehe ya kuripoti']

print(f"\nTotal households in tool-4-general: {len(df_general)}")
print(f"Total households in tool-4-vyandarua: {len(df_vyandarua)}")

# Step 1: Update existing rows in df_vyandarua
print("\nStep 1: Updating existing records...")

# Create a lookup dictionary from df_general
lookup_dict = {}
for _, row in df_general.iterrows():
    household_id = row[match_column]
    lookup_dict[household_id] = {col: row[col] for col in columns_to_update}

# Update existing rows
updated_count = 0
for idx, row in df_vyandarua.iterrows():
    household_id = row[match_column]
    if household_id in lookup_dict:
        for col in columns_to_update:
            df_vyandarua.at[idx, col] = lookup_dict[household_id][col]
        updated_count += 1

print(f"Updated {updated_count} existing records")

# Step 2: Find missing household IDs and add them
print("\nStep 2: Adding missing households...")

# Find household IDs in df_general but not in df_vyandarua
existing_ids = set(df_vyandarua[match_column].values)
general_ids = set(df_general[match_column].values)
missing_ids = general_ids - existing_ids

print(f"Found {len(missing_ids)} missing household IDs")

# Create new rows for missing households
new_rows = []
for missing_id in missing_ids:
    # Get the row from df_general
    general_row = df_general[df_general[match_column] == missing_id].iloc[0]
    
    # Create a new row with basic columns plus the two specific columns
    new_row = {}
    
    # Copy basic columns
    for col in basic_columns:
        if col in df_general.columns:
            new_row[col] = general_row[col]
    
    # Add the household ID
    new_row[match_column] = missing_id
    
    # Add the two specific columns
    for col in columns_to_update:
        new_row[col] = general_row[col]
    
    new_rows.append(new_row)

# Append new rows to df_vyandarua
if new_rows:
    new_df = pd.DataFrame(new_rows)
    df_vyandarua = pd.concat([df_vyandarua, new_df], ignore_index=True)
    print(f"Added {len(new_rows)} new household records")

# Save the updated dataframe
output_file = 'tool-4-vyandarua-updated.csv'
df_vyandarua.to_csv(output_file, index=False)

print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print(f"Total households in updated file: {len(df_vyandarua)}")
print(f"Records updated: {updated_count}")
print(f"New records added: {len(new_rows)}")
print(f"\nOutput saved to: {output_file}")
print(f"{'='*60}")