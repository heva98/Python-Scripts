import pandas as pd

print("CSV Column Data Checker")
print("=" * 50)

# Get file name
filename = input("\nEnter CSV file name: ").strip()

# Get column name
column_name = input("Enter column name to check: ").strip()

try:
    # Read CSV file
    df = pd.read_csv(filename)
    
    print(f"\nFile loaded successfully!")
    print(f"Total rows: {len(df)}")
    print(f"Columns in file: {', '.join(df.columns)}")
    
    # Check if column exists
    if column_name not in df.columns:
        print(f"\n❌ Column '{column_name}' not found in the file!")
        print(f"Available columns: {', '.join(df.columns)}")
    else:
        # Check for data in the column
        non_null_count = df[column_name].notna().sum()
        null_count = df[column_name].isna().sum()
        total_count = len(df[column_name])
        
        print(f"\n{'=' * 50}")
        print(f"Column: '{column_name}'")
        print(f"{'=' * 50}")
        print(f"Total cells: {total_count}")
        print(f"Cells with data: {non_null_count}")
        print(f"Empty cells: {null_count}")
        print(f"Percentage filled: {(non_null_count/total_count)*100:.1f}%")
        
        if non_null_count > 0:
            print(f"\n✓ Column HAS data!")
            print(f"\nFirst few values:")
            print(df[column_name].dropna().head(5).to_string())
        else:
            print(f"\n✗ Column is EMPTY (no data)")
        
except FileNotFoundError:
    print(f"\n❌ Error: File '{filename}' not found!")
except Exception as e:
    print(f"\n❌ Error: {e}")