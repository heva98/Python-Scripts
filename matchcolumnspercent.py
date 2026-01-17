import pandas as pd
from rapidfuzz import process, fuzz

# Load CSV files
sheet1 = pd.read_csv("sheet1.csv")
sheet2 = pd.read_csv("sheet2.csv")

# Clean and normalize text
sheet1["L"] = sheet1["L"].astype(str).str.strip()
sheet2["I"] = sheet2["I"].astype(str).str.strip()

# Lookup list
lookup_values = sheet1["L"].tolist()

# Fuzzy lookup function
def fuzzy_lookup(value, threshold=90):
    if pd.isna(value) or value == "":
        return None

    match = process.extractOne(
        value,
        lookup_values,
        scorer=fuzz.token_sort_ratio
    )

    if match and match[1] >= threshold:
        matched_value = match[0]
        return sheet1.loc[sheet1["L"] == matched_value, "O"].values[0]

    return None

# Apply fuzzy matching
sheet2["K"] = sheet2["I"].apply(fuzzy_lookup)

# Save output
sheet2.to_csv("sheet2_matched.csv", index=False)

print("✅ Matching complete. Output saved as sheet2_matched.csv")
