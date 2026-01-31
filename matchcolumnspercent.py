"""
Fuzzy Matching Lookup Script
Matches student names from sheet21 with sheet1,
and returns corresponding age values
"""

import pandas as pd
from rapidfuzz import process, fuzz

def fuzzy_lookup_with_verification(sheet1_path, sheet21_path, output_path="sheet21_matched.csv", threshold=90):
    """
    Perform fuzzy matching between two CSV files
    
    Args:
        sheet1_path: Path to the lookup reference CSV (contains "Jina" and "SMPS 4. Je, mwanakaya ana umri gani?")
        sheet21_path: Path to the CSV to be matched (contains "SMPS 4. Jina Kamili")
        output_path: Path for the output CSV
        threshold: Minimum similarity score (0-100) to consider a match
    """
    
    print("Loading CSV files...")
    
    # Load CSV files with error handling
    try:
        sheet1 = pd.read_csv(sheet1_path)
        sheet21 = pd.read_csv(sheet21_path)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please ensure both CSV files exist in the same directory as this script.")
        return
    except Exception as e:
        print(f"❌ Error loading files: {e}")
        return
    
    # Column names
    col_name_lookup = "Jina"  # Name column in sheet1
    col_age_lookup = "SMPS 4. Je, mwanakaya ana umri gani?"  # Age column in sheet1
    col_name_match = "SMPS 4. Jina Kamili"  # Name column in sheet21
    
    # Verify required columns exist
    if col_name_lookup not in sheet1.columns:
        print(f"❌ Error: Column '{col_name_lookup}' not found in {sheet1_path}")
        print(f"Available columns: {', '.join(sheet1.columns)}")
        return
    
    if col_age_lookup not in sheet1.columns:
        print(f"❌ Error: Column '{col_age_lookup}' not found in {sheet1_path}")
        print(f"Available columns: {', '.join(sheet1.columns)}")
        return
    
    if col_name_match not in sheet21.columns:
        print(f"❌ Error: Column '{col_name_match}' not found in {sheet21_path}")
        print(f"Available columns: {', '.join(sheet21.columns)}")
        return
    
    print(f"✓ Loaded sheet1: {len(sheet1)} rows")
    print(f"✓ Loaded sheet21: {len(sheet21)} rows")
    
    # Clean and normalize text - ENHANCED
    def clean_text(text):
        """Thoroughly clean and normalize text for better matching"""
        if pd.isna(text):
            return ""
        text = str(text)
        # Convert to lowercase
        text = text.lower()
        # Remove extra whitespace (multiple spaces to single space)
        text = ' '.join(text.split())
        # Strip leading/trailing spaces
        text = text.strip()
        return text
    
    sheet1[col_name_lookup] = sheet1[col_name_lookup].apply(clean_text)
    sheet21[col_name_match] = sheet21[col_name_match].apply(clean_text)
    
    print(f"\n🔍 Sample normalized names from sheet1:")
    print(sheet1[col_name_lookup].head(3).to_list())
    print(f"\n🔍 Sample normalized names from sheet21:")
    print(sheet21[col_name_match].head(3).to_list())
    
    # Remove rows where name is NaN or empty in sheet1
    sheet1_clean = sheet1[
        sheet1[col_name_lookup].notna() & 
        (sheet1[col_name_lookup] != "") & 
        (sheet1[col_name_lookup] != "nan")
    ].copy()
    
    if len(sheet1_clean) == 0:
        print(f"❌ Error: No valid values in sheet1 column '{col_name_lookup}'")
        return
    
    print(f"✓ Using {len(sheet1_clean)} valid lookup values from sheet1")
    
    # Create lookup dictionary for faster access
    lookup_dict = dict(zip(sheet1_clean[col_name_lookup], sheet1_clean[col_age_lookup]))
    lookup_values = list(lookup_dict.keys())
    
    # Fuzzy lookup function with match score tracking
    match_scores = []
    
    def fuzzy_lookup(value):
        # Handle empty or NaN values
        if pd.isna(value) or value == "" or value == "nan":
            match_scores.append(None)
            return None
        
        # Try exact match first (faster)
        if value in lookup_dict:
            match_scores.append(100)
            return lookup_dict[value]
        
        # Perform fuzzy matching
        match = process.extractOne(
            value,
            lookup_values,
            scorer=fuzz.token_sort_ratio
        )
        
        # Store match score
        if match:
            match_scores.append(match[1])
        else:
            match_scores.append(0)
        
        # Return matched value if above threshold
        if match and match[1] >= threshold:
            matched_value = match[0]
            return lookup_dict[matched_value]
        
        return None
    
    # Apply fuzzy matching with progress indication
    print(f"\nPerforming fuzzy matching (threshold: {threshold}%)...")
    
    # Use existing column K for matched ages
    output_col_name = "SMPS 4. Je, mwanakaya ana umri gani?"
    sheet21[output_col_name] = sheet21[col_name_match].apply(fuzzy_lookup)
    
    # Add match score column for debugging
    sheet21["Match Score (%)"] = match_scores
    
    # Calculate statistics
    total_rows = len(sheet21)
    matched_rows = sheet21[output_col_name].notna().sum()
    unmatched_rows = total_rows - matched_rows
    match_rate = (matched_rows / total_rows * 100) if total_rows > 0 else 0
    
    print(f"\n📊 Matching Results:")
    print(f"   Total rows: {total_rows}")
    print(f"   Matched: {matched_rows} ({match_rate:.1f}%)")
    print(f"   Unmatched: {unmatched_rows} ({100-match_rate:.1f}%)")
    
    # Show sample of unmatched values
    if unmatched_rows > 0:
        print(f"\n⚠️  Unmatched names with their scores:")
        unmatched_data = sheet21[sheet21[output_col_name].isna()][[col_name_match, "Match Score (%)"]].head(10)
        for idx, row in unmatched_data.iterrows():
            name = row[col_name_match]
            score = row["Match Score (%)"]
            if name and name != "nan":
                print(f"   '{name}' → Score: {score}%")
    
    # Save output
    try:
        sheet21.to_csv(output_path, index=False)
        print(f"\n✅ Matching complete. Output saved as: {output_path}")
    except Exception as e:
        print(f"❌ Error saving output file: {e}")
        return
    
    return sheet21


# Main execution
if __name__ == "__main__":
    # Configuration
    SHEET1_FILE = "sheet1.csv"  # Lookup reference file (contains Jina and Umri)
    sheet21_FILE = "sheet21.csv"  # File to be matched (contains Jina Kamili)
    OUTPUT_FILE = "sheet21_matched.csv"
    SIMILARITY_THRESHOLD = 35  # Adjust this value (0-100) to control match strictness
    
    # Run fuzzy matching
    result = fuzzy_lookup_with_verification(
        sheet1_path=SHEET1_FILE,
        sheet21_path=sheet21_FILE,
        output_path=OUTPUT_FILE,
        threshold=SIMILARITY_THRESHOLD
    )
    
    # Optional: Show sample results
    if result is not None:
        print("\n📋 Sample of matched results (with scores):")
        col_name = "SMPS 4. Jina Kamili"
        col_age = "Umri (Matched)"
        col_score = "Match Score (%)"
        if col_name in result.columns and col_age in result.columns:
            print(result[[col_name, col_age, col_score]].head(10).to_string(index=False))