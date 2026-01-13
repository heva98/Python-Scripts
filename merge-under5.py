import pandas as pd
import numpy as np

# Read the CSV files
print("Reading CSV files...")
events_df = pd.read_csv('events.csv')
tested_children_df = pd.read_csv('tool-4-under-5.csv')

# Strip whitespace from headers
events_df.columns = events_df.columns.str.strip()
tested_children_df.columns = tested_children_df.columns.str.strip()

print(f"\nEvents.csv has {len(events_df)} rows and {len(events_df.columns)} columns")
print(f"Tool-4-under-5.csv has {len(tested_children_df)} rows and {len(tested_children_df.columns)} columns")

# Display columns
print("\n" + "="*80)
print("COLUMNS IN EVENTS.CSV:")
print("="*80)
for i, col in enumerate(events_df.columns, 1):
    print(f"{i}. {col}")

print("\n" + "="*80)
print("STEP 1: SPECIFY COLUMN NAMES")
print("="*80)

# Get column names
print("\n1. Village ID column name (should be same in both files):")
village_col = input("   ").strip()

print("\n2. Household ID column name (should be same in both files):")
household_col = input("   ").strip()

print("\n3. Member Line Number column name (from events.csv):")
line_number_col = input("   ").strip()

print("\n4. Age in months column name (from events.csv):")
age_months_col = input("   ").strip()

print("\n5. First Name column name (from events.csv) [Optional - press Enter to skip]:")
first_name_col = input("   ").strip()
if first_name_col == "":
    first_name_col = None

print("\n6. Gender column name (from events.csv) [Optional - press Enter to skip]:")
gender_col = input("   ").strip()
if gender_col == "":
    gender_col = None

# Verify columns
print("\n" + "="*80)
print("VERIFYING COLUMNS...")
print("="*80)

errors = []
if village_col not in events_df.columns:
    errors.append(f"Missing in events.csv: {village_col}")
if household_col not in events_df.columns:
    errors.append(f"Missing in events.csv: {household_col}")
if line_number_col not in events_df.columns:
    errors.append(f"Missing in events.csv: {line_number_col}")
if age_months_col not in events_df.columns:
    errors.append(f"Missing in events.csv: {age_months_col}")
if first_name_col and first_name_col not in events_df.columns:
    errors.append(f"Missing in events.csv: {first_name_col}")
if gender_col and gender_col not in events_df.columns:
    errors.append(f"Missing in events.csv: {gender_col}")

if village_col not in tested_children_df.columns:
    errors.append(f"Missing in tool-4-under-5.csv: {village_col}")
if household_col not in tested_children_df.columns:
    errors.append(f"Missing in tool-4-under-5.csv: {household_col}")

if errors:
    print("ERRORS FOUND:")
    for error in errors:
        print(f"  ✗ {error}")
    exit()

print("✓ All columns verified!")

# Filter for children under 5 in events.csv
print("\n" + "="*80)
print("STEP 2: FINDING CHILDREN UNDER 5 IN EVENTS.CSV...")
print("="*80)

events_df[age_months_col] = pd.to_numeric(events_df[age_months_col], errors='coerce')
under5_df = events_df[events_df[age_months_col] < 60].copy()

print(f"Found {len(under5_df)} children under 5 years in events.csv")

# Count children under 5 per household
household_child_counts = under5_df.groupby([village_col, household_col]).size().reset_index(name='children_count')

print("\n" + "="*80)
print("HOUSEHOLD ANALYSIS:")
print("="*80)
print(f"Total households with children under 5: {len(household_child_counts)}")
print(f"Households with 1 child under 5: {len(household_child_counts[household_child_counts['children_count'] == 1])}")
print(f"Households with 2+ children under 5: {len(household_child_counts[household_child_counts['children_count'] > 1])}")

# Match tested children to households
print("\n" + "="*80)
print("STEP 3: MATCHING TESTED CHILDREN TO HOUSEHOLDS...")
print("="*80)

# Create a list to store results
results = []

for idx, test_row in tested_children_df.iterrows():
    village = test_row[village_col]
    household = test_row[household_col]
    
    # Find all children under 5 in this household
    matching_children = under5_df[
        (under5_df[village_col] == village) & 
        (under5_df[household_col] == household)
    ]
    
    if len(matching_children) == 0:
        # No match found
        result = test_row.to_dict()
        result['match_status'] = 'NO_MATCH'
        result['match_count'] = 0
        result[line_number_col] = None
        result[age_months_col] = None
        if first_name_col:
            result[first_name_col] = None
        if gender_col:
            result[gender_col] = None
        results.append(result)
        
    elif len(matching_children) == 1:
        # Exact match - one child under 5 in household
        result = test_row.to_dict()
        result['match_status'] = 'EXACT_MATCH'
        result['match_count'] = 1
        child = matching_children.iloc[0]
        result[line_number_col] = child[line_number_col]
        result[age_months_col] = child[age_months_col]
        if first_name_col:
            result[first_name_col] = child[first_name_col]
        if gender_col:
            result[gender_col] = child[gender_col]
        results.append(result)
        
    else:
        # Multiple children - create rows for each possibility
        for i, (_, child) in enumerate(matching_children.iterrows(), 1):
            result = test_row.to_dict()
            result['match_status'] = f'MULTIPLE_MATCH_{i}'
            result['match_count'] = len(matching_children)
            result[line_number_col] = child[line_number_col]
            result[age_months_col] = child[age_months_col]
            if first_name_col:
                result[first_name_col] = child[first_name_col]
            if gender_col:
                result[gender_col] = child[gender_col]
            results.append(result)

merged_df = pd.DataFrame(results)

# Summary statistics
exact_matches = len(merged_df[merged_df['match_status'] == 'EXACT_MATCH'])
no_matches = len(merged_df[merged_df['match_status'] == 'NO_MATCH'])
multiple_matches = len(merged_df[merged_df['match_status'].str.contains('MULTIPLE_MATCH', na=False)])

print(f"✓ Exact matches (1 child per household): {exact_matches}")
print(f"⚠ Multiple possibilities (2+ children per household): {multiple_matches} rows created")
print(f"✗ No matches found: {no_matches}")

# Save results
output_filename = 'merged_tested_children_with_household_details.csv'
merged_df.to_csv(output_filename, index=False)
print(f"\n✓ Merged data saved to: {output_filename}")

# Save households with multiple children for manual review
if multiple_matches > 0:
    multiple_df = merged_df[merged_df['match_status'].str.contains('MULTIPLE_MATCH', na=False)]
    multiple_filename = 'households_with_multiple_children_REVIEW_NEEDED.csv'
    multiple_df.to_csv(multiple_filename, index=False)
    print(f"✓ Households with multiple children saved to: {multiple_filename}")
    print("  → These need manual review to identify which specific child was tested")

# Save no matches for review
if no_matches > 0:
    no_match_df = merged_df[merged_df['match_status'] == 'NO_MATCH']
    no_match_filename = 'no_matches_found.csv'
    no_match_df.to_csv(no_match_filename, index=False)
    print(f"✓ Unmatched records saved to: {no_match_filename}")

# Show preview
print("\n" + "="*80)
print("PREVIEW - EXACT MATCHES:")
print("="*80)
exact_preview = merged_df[merged_df['match_status'] == 'EXACT_MATCH'].head(3)
if len(exact_preview) > 0:
    cols_to_show = [village_col, household_col, line_number_col, age_months_col]
    if first_name_col:
        cols_to_show.append(first_name_col)
    cols_to_show.append('match_status')
    print(exact_preview[cols_to_show].to_string())
else:
    print("No exact matches found")

print("\n" + "="*80)
print("MERGE COMPLETE!")
print("="*80)
print(f"\nTotal tested children: {len(tested_children_df)}")
print(f"Total rows in output: {len(merged_df)}")
print(f"\nMatch rate: {(exact_matches/len(tested_children_df)*100):.1f}% exact matches")
if multiple_matches > 0:
    print(f"\nNOTE: {len(merged_df[merged_df['match_count'] > 1][household_col].unique())} households have multiple children under 5.")
    print("These require manual review to determine which child was actually tested.")
    