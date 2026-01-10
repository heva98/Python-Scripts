import pandas as pd
import sys

def update_csv_data():
    """
    Script to update blank values in one CSV file with values from another CSV file
    based on matching ID columns.
    """
    
    print("=" * 60)
    print("CSV Data Update Tool")
    print("=" * 60)
    
    # Get file paths
    print("\nEnter the file paths for your CSV files:")
    file1_path = input("Path to CSV file 1 (to be updated): ").strip()
    file2_path = input("Path to CSV file 2 (source of data): ").strip()
    
    # Load CSV files
    try:
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)
        print(f"\n✓ Successfully loaded both CSV files")
    except FileNotFoundError as e:
        print(f"\n✗ Error: File not found - {e}")
        return
    except Exception as e:
        print(f"\n✗ Error loading files: {e}")
        return
    
    # Display columns
    print(f"\nColumns in CSV file 1: {', '.join(df1.columns.tolist())}")
    print(f"Columns in CSV file 2: {', '.join(df2.columns.tolist())}")
    
    # Get column names for matching (ID column)
    print("\n" + "-" * 60)
    print("Specify the ID column for matching records:")
    id_col1 = input("ID column name in CSV file 1: ").strip()
    id_col2 = input("ID column name in CSV file 2: ").strip()
    
    # Validate ID columns exist
    if id_col1 not in df1.columns:
        print(f"\n✗ Error: Column '{id_col1}' not found in CSV file 1")
        return
    if id_col2 not in df2.columns:
        print(f"\n✗ Error: Column '{id_col2}' not found in CSV file 2")
        return
    
    # Get column names for data to be updated
    print("\n" + "-" * 60)
    print("Specify the data column to update:")
    data_col1 = input("Column name in CSV file 1 (to be updated): ").strip()
    data_col2 = input("Column name in CSV file 2 (source): ").strip()
    
    # Validate data columns exist
    if data_col1 not in df1.columns:
        print(f"\n✗ Error: Column '{data_col1}' not found in CSV file 1")
        return
    if data_col2 not in df2.columns:
        print(f"\n✗ Error: Column '{data_col2}' not found in CSV file 2")
        return
    
    # Count blank values before update
    blank_count = df1[data_col1].isna().sum() + (df1[data_col1] == '').sum()
    print(f"\n📊 Found {blank_count} blank values in '{data_col1}' column")
    
    # Create a mapping dictionary from df2
    mapping_dict = df2.set_index(id_col2)[data_col2].to_dict()
    
    # Update blank values in df1
    updates_made = 0
    for idx, row in df1.iterrows():
        # Check if the value is blank (NaN or empty string)
        if pd.isna(row[data_col1]) or row[data_col1] == '':
            id_value = row[id_col1]
            # Look for matching ID in df2
            if id_value in mapping_dict and pd.notna(mapping_dict[id_value]):
                df1.at[idx, data_col1] = mapping_dict[id_value]
                updates_made += 1
    
    print(f"✓ Updated {updates_made} records")
    
    # Save updated file
    print("\n" + "-" * 60)
    output_path = input("Enter output file path (press Enter for 'updated_output.csv'): ").strip()
    if not output_path:
        output_path = "updated_output.csv"
    
    try:
        df1.to_csv(output_path, index=False)
        print(f"\n✓ Successfully saved updated file to: {output_path}")
    except Exception as e:
        print(f"\n✗ Error saving file: {e}")
        return
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total records in CSV file 1: {len(df1)}")
    print(f"Blank values before update: {blank_count}")
    print(f"Records updated: {updates_made}")
    print(f"Output file: {output_path}")
    print("=" * 60)

if __name__ == "__main__":
    try:
        update_csv_data()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)