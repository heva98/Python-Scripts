import pandas as pd

# Read both CSV files
events19 = pd.read_csv('events19.csv')
tool_wanakaya = pd.read_csv('tool-4-wanakaya-v4.csv')

# Column names
id_column = 'SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'
data_column = 'SMPS 4 Idadi ya Wanakaya'

# Create a dictionary mapping ID to the data value from events19
id_to_data = dict(zip(events19[id_column], events19[data_column]))

# Update the tool_wanakaya dataframe by mapping IDs to data values
tool_wanakaya[data_column] = tool_wanakaya[id_column].map(id_to_data)

# Save the updated dataframe to a new CSV file
tool_wanakaya.to_csv('tool-4-wanakaya-v4-updated.csv', index=False)

print("Data copy completed successfully!")
print(f"Total rows in events19: {len(events19)}")
print(f"Total rows in tool-4-wanakaya-v4: {len(tool_wanakaya)}")
print(f"Rows matched and updated: {tool_wanakaya[data_column].notna().sum()}")
print(f"Rows with no match: {tool_wanakaya[data_column].isna().sum()}")