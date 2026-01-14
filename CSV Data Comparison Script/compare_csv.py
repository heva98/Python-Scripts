import pandas as pd

def find_missing_values(csv1_path, csv2_path, col1_name, col2_name, filter_col=None):
    """
    Compare two CSV files and find values in csv1[col1] that are missing from csv2[col2].
    Optionally filter csv1 to only include rows where filter_col has data.
    
    Args:
        csv1_path: Path to first CSV file
        csv2_path: Path to second CSV file
        col1_name: Column name in first CSV
        col2_name: Column name in second CSV
        filter_col: Column in csv1 to filter by (only include rows with data in this column)
    
    Returns:
        List of values present in csv1 but missing in csv2
    """
    try:
        # Read CSV files with proper handling
        print("Reading CSV files...")
        df1 = pd.read_csv(csv1_path, encoding='utf-8-sig', skipinitialspace=True)
        df2 = pd.read_csv(csv2_path, encoding='utf-8-sig', skipinitialspace=True)
        
        # Clean column names (remove extra spaces)
        df1.columns = df1.columns.str.strip()
        df2.columns = df2.columns.str.strip()
        
        print(f"CSV 1 has {len(df1)} rows and {len(df1.columns)} columns")
        print(f"CSV 2 has {len(df2)} rows and {len(df2.columns)} columns")
        
        # Check if columns exist
        if col1_name not in df1.columns:
            print(f"\n❌ Error: Column '{col1_name}' not found in CSV 1")
            print("Available columns:")
            for col in df1.columns:
                print(f"  - {col}")
            return None
        
        if col2_name not in df2.columns:
            print(f"\n❌ Error: Column '{col2_name}' not found in CSV 2")
            print("Available columns:")
            for col in df2.columns:
                print(f"  - {col}")
            return None
        
        if filter_col and filter_col not in df1.columns:
            print(f"\n❌ Error: Filter column '{filter_col}' not found in CSV 1")
            print("Available columns:")
            for col in df1.columns:
                print(f"  - {col}")
            return None
        
        # Apply filter if specified
        df1_filtered = df1.copy()
        if filter_col:
            before_filter = len(df1_filtered)
            # Filter to only rows where filter_col has data (not NaN and not empty string)
            mask = df1_filtered[filter_col].notna()
            mask = mask & (df1_filtered[filter_col].astype(str).str.strip() != '')
            df1_filtered = df1_filtered[mask]
            after_filter = len(df1_filtered)
            
            print(f"\n=== Filter Applied ===")
            print(f"Column to filter: '{filter_col}'")
            print(f"Rows before filter: {before_filter}")
            print(f"Rows after filter (with data in '{filter_col}'): {after_filter}")
            print(f"Rows filtered out: {before_filter - after_filter}")
        
        # Get unique values from both columns (remove NaN and empty strings)
        values_csv1_raw = df1_filtered[col1_name].dropna()
        values_csv1 = set(values_csv1_raw.astype(str).str.strip())
        values_csv1 = {v for v in values_csv1 if v and v != ''}
        
        values_csv2_raw = df2[col2_name].dropna()
        values_csv2 = set(values_csv2_raw.astype(str).str.strip())
        values_csv2 = {v for v in values_csv2 if v and v != ''}
        
        # Find missing values (in csv1 but not in csv2)
        missing_values = sorted(values_csv1 - values_csv2)
        
        # Print statistics
        print(f"\n=== Statistics ===")
        print(f"Unique values in filtered CSV 1 ('{col1_name}'): {len(values_csv1)}")
        print(f"Unique values in CSV 2 ('{col2_name}'): {len(values_csv2)}")
        print(f"Missing from CSV 2: {len(missing_values)}")
        
        return missing_values
    
    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        return None
    except pd.errors.EmptyDataError:
        print(f"❌ Error: One of the CSV files is empty")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("=" * 70)
    print("CSV Column Comparison Tool")
    print("=" * 70)
    
    # Get file paths
    csv1 = input("\nEnter path to FIRST CSV file: ").strip().strip('"').strip("'")
    csv2 = input("Enter path to SECOND CSV file: ").strip().strip('"').strip("'")
    
    print("\nReading files to display columns...")
    
    # First, read and show columns
    try:
        df1 = pd.read_csv(csv1, encoding='utf-8-sig', skipinitialspace=True)
        df2 = pd.read_csv(csv2, encoding='utf-8-sig', skipinitialspace=True)
        df1.columns = df1.columns.str.strip()
        df2.columns = df2.columns.str.strip()
        
        print("\n" + "=" * 70)
        print("COLUMNS IN CSV 1:")
        print("=" * 70)
        for i, col in enumerate(df1.columns, 1):
            print(f"{i:2d}. {col}")
        
        print("\n" + "=" * 70)
        print("COLUMNS IN CSV 2:")
        print("=" * 70)
        for i, col in enumerate(df2.columns, 1):
            print(f"{i:2d}. {col}")
    except Exception as e:
        print(f"❌ Error reading files: {e}")
        return
    
    # Get column names
    print("\n" + "=" * 70)
    print("SPECIFY COLUMNS TO COMPARE")
    print("=" * 70)
    col1 = input("\nColumn from CSV 1 to compare: ").strip()
    col2 = input("Column from CSV 2 to compare: ").strip()
    
    # Ask about filtering
    print("\n" + "=" * 70)
    print("OPTIONAL: Filter CSV 1 by a column")
    print("(This will only compare rows where the filter column has data)")
    print("=" * 70)
    use_filter = input("Do you want to apply a filter? (yes/no): ").strip().lower()
    filter_col = None
    if use_filter in ['yes', 'y', 'YES', 'Y']:
        print("\nEnter the exact column name from CSV 1 that you want to filter by.")
        print("Example: SMPS 4 Tafsiri ya Kipimo cha malaria")
        filter_col = input("\nFilter column name: ").strip()
        print(f"\n✓ Will filter CSV 1 to only rows where '{filter_col}' has data")
    
    print("\n" + "=" * 70)
    print("COMPARING FILES...")
    print("=" * 70)
    
    # Find missing values
    missing = find_missing_values(csv1, csv2, col1, col2, filter_col)
    
    if missing is not None:
        print(f"\n{'='*70}")
        print(f"RESULTS")
        print(f"{'='*70}")
        print(f"Looking for values from CSV 1 column: '{col1}'")
        print(f"That are missing in CSV 2 column: '{col2}'")
        if filter_col:
            print(f"Filtered to rows where '{filter_col}' has data")
        print(f"{'='*70}")
        
        if missing:
            print(f"\n✗ Found {len(missing)} missing value(s):\n")
            for i, val in enumerate(missing, 1):
                print(f"{i:3d}. {val}")
            
            # Ask if user wants to save to file
            print("\n" + "=" * 70)
            save = input(f"Save these {len(missing)} values to a file? (yes/no): ").strip().lower()
            if save in ['yes', 'y']:
                output_file = input("Output filename: ").strip()
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(f"Missing values from '{col1}' (CSV 1)\n")
                        f.write(f"Not found in '{col2}' (CSV 2)\n")
                        if filter_col:
                            f.write(f"Filtered by: '{filter_col}'\n")
                        f.write("=" * 70 + "\n\n")
                        for i, val in enumerate(missing, 1):
                            f.write(f"{i}. {val}\n")
                    print(f"✓ Saved to {output_file}")
                except Exception as e:
                    print(f"❌ Error saving file: {e}")
        else:
            print("\n✓ No missing values found!")
            print("All values from CSV 1 exist in CSV 2.")

if __name__ == "__main__":
    main()