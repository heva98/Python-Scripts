import pandas as pd

# Read both CSV files
sheet1 = pd.read_csv('tool-1.csv')
sheet2 = pd.read_csv('events.csv')

# Strip whitespace from column names to avoid issues
sheet1.columns = sheet1.columns.str.strip()
sheet2.columns = sheet2.columns.str.strip()

# Create a lookup dictionary from sheet1 using Level 6 as key
# The value will be a dict containing the hierarchical data
lookup = {}
for _, row in sheet1.iterrows():
    level6_value = row['Level 6']
    lookup[level6_value] = {
        'National': row['National'],
        'Regions': row['Regions'],
        'Councils': row['Councils'],
        'Wards': row['Wards'],
        'Street/Villages': row['Street/Villages']
    }

# Fill sheet2 columns based on Level 6 match
for idx, row in sheet2.iterrows():
    level6_value = row['Level 6']
    
    # Check if this Level 6 value exists in sheet1
    if level6_value in lookup:
        sheet2.at[idx, 'National'] = lookup[level6_value]['National']
        sheet2.at[idx, 'Regions'] = lookup[level6_value]['Regions']
        sheet2.at[idx, 'Councils'] = lookup[level6_value]['Councils']
        sheet2.at[idx, 'Wards'] = lookup[level6_value]['Wards']
        sheet2.at[idx, 'Street/Villages'] = lookup[level6_value]['Street/Villages']
    else:
        print(f"Warning: Level 6 value '{level6_value}' not found in sheet1")

# Save the updated sheet2
sheet2.to_csv('events_updated.csv', index=False)
print("Events.csv has been updated and saved as 'events_updated.csv'")
print(f"Total rows processed: {len(sheet2)}")
print(f"Unique Level 6 values in tool-1.csv: {len(lookup)}")