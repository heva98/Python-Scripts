"""
Fuzzy Matching Lookup Script
Matches values from sheet2 column I with sheet1 column L,
and returns corresponding values from sheet1 column O
"""

import pandas as pd
from rapidfuzz import process, fuzz

def fuzzy_lookup_with_verification(sheet1_path, sheet2_path, output_path="sheet2_matched.csv", threshold=90):
    """
    Perform fuzzy matching between two CSV files
    
    Args:
        sheet1_path: Path to the lookup reference CSV (contains columns L and O)
        sheet2_path: Path to the CSV to be matched (contains column I)
        output_path: Path for the output CSV
        threshold: Minimum similarity score (0-100) to consider a match
    """
    
    print("Loading CSV files...")
    
    # Load CSV files with error handling
    try:
        sheet1 = pd.read_csv(sheet1_path)
        sheet2 = pd.read_csv(sheet2_path)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please ensure both CSV files exist in the same directory as this script.")
        return
    except Exception as e:
        print(f"❌ Error loading files: {e}")
        return
    
    # Verify required columns exist
    if "L" not in sheet1.columns:
        print(f"❌ Error: Column 'L' not found in {sheet1_path}")
        print(f"Available columns: {', '.join(sheet1.columns)}")
        return
    
    if "O" not in sheet1.columns:
        print(f"❌ Error: Column 'O' not found in {sheet1_path}")
        print(f"Available columns: {', '.join(sheet1.columns)}")
        return
    
    if "I" not in sheet2.columns:
        print(f"❌ Error: Column 'I' not found in {sheet2_path}")
        print(f"Available columns: {', '.join(sheet2.columns)}")
        return
    
    print(f"✓ Loaded sheet1: {len(sheet1)} rows")
    print(f"✓ Loaded sheet2: {len(sheet2)} rows")
    
    # Clean and normalize text
    sheet1["L"] = sheet1["L"].astype(str).str.strip()
    sheet2["I"] = sheet2["I"].astype(str).str.strip()
    
    # Remove rows where L is NaN or empty in sheet1
    sheet1_clean = sheet1[sheet1["L"].notna() & (sheet1["L"] != "") & (sheet1["L"] != "nan")].copy()
    
    if len(sheet1_clean) == 0:
        print("❌ Error: No valid values in sheet1 column L")
        return
    
    print(f"✓ Using {len(sheet1_clean)} valid lookup values from sheet1")
    
    # Create lookup dictionary for faster access
    lookup_dict = dict(zip(sheet1_clean["Jina"], sheet1_clean["SMPS 4. Je, mwanakaya ana umri gani?"]))
    lookup_values = list(lookup_dict.keys())
    
    # Fuzzy lookup function
    def fuzzy_lookup(value):
        # Handle empty or NaN values
        if pd.isna(value) or value == "" or value == "nan":
            return None
        
        # Try exact match first (faster)
        if value in lookup_dict:
            return lookup_dict[value]
        
        # Perform fuzzy matching
        match = process.extractOne(
            value,
            lookup_values,
            scorer=fuzz.token_sort_ratio
        )
        
        # Return matched value if above threshold
        if match and match[1] >= threshold:
            matched_value = match[0]
            return lookup_dict[matched_value]
        
        return None
    
    # Apply fuzzy matching with progress indication
    print(f"\nPerforming fuzzy matching (threshold: {threshold}%)...")
    sheet2["K"] = sheet2["I"].apply(fuzzy_lookup)
    
    # Calculate statistics
    total_rows = len(sheet2)
    matched_rows = sheet2["K"].notna().sum()
    unmatched_rows = total_rows - matched_rows
    match_rate = (matched_rows / total_rows * 100) if total_rows > 0 else 0
    
    print(f"\n📊 Matching Results:")
    print(f"   Total rows: {total_rows}")
    print(f"   Matched: {matched_rows} ({match_rate:.1f}%)")
    print(f"   Unmatched: {unmatched_rows} ({100-match_rate:.1f}%)")
    
    # Show sample of unmatched values
    if unmatched_rows > 0:
        print(f"\n⚠️  Sample of unmatched values from column I:")
        unmatched_samples = sheet2[sheet2["K"].isna()]["I"].head(5)
        for idx, val in enumerate(unmatched_samples, 1):
            if val and val != "nan":
                print(f"   {idx}. '{val}'")
    
    # Save output
    try:
        sheet2.to_csv(output_path, index=False)
        print(f"\n✅ Matching complete. Output saved as: {output_path}")
    except Exception as e:
        print(f"❌ Error saving output file: {e}")
        return
    
    return sheet2


# Main execution
if __name__ == "__main__":
    # Configuration
    SHEET1_FILE = "sheet1.csv"  # Lookup reference file
    SHEET2_FILE = "sheet2.csv"  # File to be matched
    OUTPUT_FILE = "sheet2_matched.csv"
    SIMILARITY_THRESHOLD = 90  # Adjust this value (0-100) to control match strictness
    
    # Run fuzzy matching
    result = fuzzy_lookup_with_verification(
        sheet1_path=SHEET1_FILE,
        sheet2_path=SHEET2_FILE,
        output_path=OUTPUT_FILE,
        threshold=SIMILARITY_THRESHOLD
    )
    
    # Optional: Show sample results
    if result is not None:
        print("\n📋 Sample of matched results:")
        print(result[["I", "K"]].head(10).to_string(index=False))