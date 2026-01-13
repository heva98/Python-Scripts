import pandas as pd
import os

def fill_by_comparison():
    """Fill columns by comparing SMPS 4 village ID between two files"""
    
    # File names
    source_file = 'tool-4-under-5.csv'
    target_file = 'enrollments.csv'
    
    # Check if files exist
    if not os.path.exists(source_file):
        print(f"Error: Source file '{source_file}' not found!")
        return
    if not os.path.exists(target_file):
        print(f"Error: Target file '{target_file}' not found!")
        return
    
    # Read both CSV files
    print(f"Reading {source_file}...")
    df_source = pd.read_csv(source_file)
    print(f"Source file rows: {len(df_source)}")
    
    print(f"\nReading {target_file}...")
    df_target = pd.read_csv(target_file)
    print(f"Target file rows: {len(df_target)}")
    
    # Show columns
    print(f"\n--- Source file columns ---")
    for i, col in enumerate(df_source.columns, 1):
        print(f"{i}. {col}")
    
    print(f"\n--- Target file columns ---")
    for i, col in enumerate(df_target.columns, 1):
        print(f"{i}. {col}")
    
    # Get column names from user
    print("\n" + "="*60)
    print("Enter the exact column names (copy-paste recommended)")
    print("="*60)
    
    # ID column (the one to match on)
    print("\n--- Matching Column (SMPS 4 : Namba Ya Utambulisho Wa Kijiji) ---")
    id_col = input("Enter the ID column name: ").strip()
    
    # Verify ID column exists in both files
    if id_col not in df_source.columns:
        print(f"Error: Column '{id_col}' not found in {source_file}")
        return
    if id_col not in df_target.columns:
        print(f"Error: Column '{id_col}' not found in {target_file}")
        return
    
    # Columns to fill
    print("\n--- Columns to Fill ---")
    national_col = input("Enter National column name: ").strip()
    regions_col = input("Enter Regions column name: ").strip()
    councils_col = input("Enter Councils column name: ").strip()
    wards_col = input("Enter Wards column name: ").strip()
    
    # Verify columns exist in both files
    fill_cols = [national_col, regions_col, councils_col, wards_col]
    
    missing_in_source = [col for col in fill_cols if col not in df_source.columns]
    missing_in_target = [col for col in fill_cols if col not in df_target.columns]
    
    if missing_in_source:
        print(f"\nError: Columns not found in {source_file}: {', '.join(missing_in_source)}")
        return
    if missing_in_target:
        print(f"\nError: Columns not found in {target_file}: {', '.join(missing_in_target)}")
        return
    
    # Check which file has the data
    print("\n--- Data Check ---")
    source_has_data = df_source[fill_cols].notna().any().any()
    target_has_data = df_target[fill_cols].notna().any().any()
    
    print(f"Source file ({source_file}) has data in these columns: {source_has_data}")
    print(f"Target file ({target_file}) has data in these columns: {target_has_data}")
    
    # Determine direction
    print("\n--- Transfer Direction ---")
    print("1. Fill target file (enrollments.csv) using source file (tool-4-under-5.csv)")
    print("2. Fill source file (tool-4-under-5.csv) using target file (enrollments.csv)")
    print("3. Fill both files (merge data from both)")
    
    direction = input("\nChoose option (1/2/3): ").strip()
    
    if direction == '1':
        # Fill target using source
        df_result = fill_target_from_source(df_target, df_source, id_col, fill_cols)
        output_file = target_file.replace('.csv', '_filled.csv')
        df_result.to_csv(output_file, index=False)
        print(f"\n✓ Successfully saved to: {output_file}")
        
    elif direction == '2':
        # Fill source using target
        df_result = fill_target_from_source(df_source, df_target, id_col, fill_cols)
        output_file = source_file.replace('.csv', '_filled.csv')
        df_result.to_csv(output_file, index=False)
        print(f"\n✓ Successfully saved to: {output_file}")
        
    elif direction == '3':
        # Fill both files
        df_target_filled = fill_target_from_source(df_target, df_source, id_col, fill_cols)
        df_source_filled = fill_target_from_source(df_source, df_target, id_col, fill_cols)
        
        target_output = target_file.replace('.csv', '_filled.csv')
        source_output = source_file.replace('.csv', '_filled.csv')
        
        df_target_filled.to_csv(target_output, index=False)
        df_source_filled.to_csv(source_output, index=False)
        
        print(f"\n✓ Successfully saved to: {target_output}")
        print(f"✓ Successfully saved to: {source_output}")
    else:
        print("Invalid option selected.")
        return
    
    print("\n=== Done! ===")

def fill_target_from_source(df_target, df_source, id_col, fill_cols):
    """Fill target dataframe using source dataframe based on ID column"""
    
    # Create a mapping dictionary from source
    source_mapping = df_source.set_index(id_col)[fill_cols].to_dict('index')
    
    print(f"\nFound {len(source_mapping)} unique IDs in source file")
    
    # Track statistics
    matched = 0
    unmatched = 0
    
    # Fill the target dataframe
    df_result = df_target.copy()
    
    for idx, row in df_result.iterrows():
        village_id = row[id_col]
        
        if pd.notna(village_id) and village_id in source_mapping:
            matched += 1
            # Fill the columns
            for col in fill_cols:
                if pd.notna(source_mapping[village_id][col]):
                    df_result.at[idx, col] = source_mapping[village_id][col]
        else:
            unmatched += 1
    
    print(f"Matched records: {matched}")
    print(f"Unmatched records: {unmatched}")
    
    return df_result

def main():
    print("="*60)
    print("CSV Column Filler - Compare by Village ID")
    print("="*60)
    print("\nThis script fills National, Regions, Councils, and Wards")
    print("by matching the 'SMPS 4 : Namba Ya Utambulisho Wa Kijiji' column\n")
    
    fill_by_comparison()

if __name__ == "__main__":
    main()