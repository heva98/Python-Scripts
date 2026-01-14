import pandas as pd

# Read both CSV files
tool4_df = pd.read_csv('tool-4-wanakaya.csv')
enrollments_df = pd.read_csv('enrollments.csv')

# Strip whitespace from column names
tool4_df.columns = tool4_df.columns.str.strip()
enrollments_df.columns = enrollments_df.columns.str.strip()

# Define the household ID column name
household_id_col = 'kijiji'

# Define columns to copy
columns_to_copy = ['National', 'Regions', 'Councils', 'Wards']

# Create a mapping dictionary from tool-4-RCH
# Key: household ID, Value: dict with the location columns
mapping = {}
for idx, row in tool4_df.iterrows():
    hh_id = row.get(household_id_col)
    if pd.notna(hh_id):  # Only process non-null household IDs
        mapping[hh_id] = {
            col: row.get(col) for col in columns_to_copy
        }

# Update enrollments dataframe
matches = 0
no_matches = 0

for idx, row in enrollments_df.iterrows():
    hh_id = row.get(household_id_col)
    
    if pd.notna(hh_id) and hh_id in mapping:
        # Copy values from tool4 to enrollments
        for col in columns_to_copy:
            enrollments_df.at[idx, col] = mapping[hh_id][col]
        matches += 1
    else:
        no_matches += 1

# Save the updated enrollments file
enrollments_df.to_csv('enrollments_updated.csv', index=False)

print(f"Processing complete!")
print(f"Matches found and updated: {matches}")
print(f"Rows with no match: {no_matches}")
print(f"Updated file saved as: enrollments_updated.csv")