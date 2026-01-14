import pandas as pd
import sys

def find_missing_values(csv1_path, csv2_path, col1_name, col2_name):
    """
    Compare two CSV files and find values in csv1[col1] that are missing from csv2[col2].
    
    Args:
        csv1_path: Path to first CSV file
        csv2_path: Path to second CSV file
        col1_name: Column name in first CSV
        col2_name: Column name in second CSV
    
    Returns:
        List of values present in csv1 but missing in csv2
    """
    try:
        # Read CSV files
        df1 = pd.read_csv(csv1_path)
        df2 = pd.read_csv(csv2_path)
        
        # Check if columns exist
        if col1_name not in df1.columns:
            print(f"Error: Column '{col1_name}' not found in {csv1_path}")
            print(f"Available columns: {', '.join(df1.columns)}")
            return None
        
        if col2_name not in df2.columns:
            print(f"Error: Column '{col2_name}' not found in {csv2_path}")
            print(f"Available columns: {', '.join(df2.columns)}")
            return None
        
        # Get unique values from both columns
        values_csv1 = set(df1[col1_name].dropna())
        values_csv2 = set(df2[col2_name].dropna())
        
        # Find missing values (in csv1 but not in csv2)
        missing_values = sorted(values_csv1 - values_csv2)
        
        return missing_values
    
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    print("CSV Column Comparison Tool")
    print("-" * 40)
    
    # Get file paths
    csv1 = input("Enter path to first CSV file: ").strip()
    csv2 = input("Enter path to second CSV file: ").strip()
    
    # Get column names
    col1 = input("Enter column name from first CSV: ").strip()
    col2 = input("Enter column name from second CSV: ").strip()
    
    print("\nComparing files...")
    
    # Find missing values
    missing = find_missing_values(csv1, csv2, col1, col2)
    
    if missing is not None:
        print(f"\n{'='*40}")
        print(f"Values in '{csv1}' but missing from '{csv2}':")
        print(f"{'='*40}")
        
        if missing:
            for i, val in enumerate(missing, 1):
                print(f"{i}. {val}")
            print(f"\nTotal missing values: {len(missing)}")
        else:
            print("No missing values found! All values from CSV1 exist in CSV2.")

if __name__ == "__main__":
    main()