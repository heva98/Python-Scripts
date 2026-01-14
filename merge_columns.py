import pandas as pd
import numpy as np

# Soma CSV files
print("Inasoma files...")
tool_under_5 = pd.read_csv('tool-4-under-5.csv')
tool_wanakaya = pd.read_csv('tool-4-wanakaya.csv')

# Strip whitespace from column names
tool_under_5.columns = tool_under_5.columns.str.strip()
tool_wanakaya.columns = tool_wanakaya.columns.str.strip()

print(f"Records katika tool4under5: {len(tool_under_5)}")
print(f"Records katika tool4wanakaya: {len(tool_wanakaya)}")

# CHECK 1: Angalia duplicates katika tool4under5
print("\n--- STEP 1: Checking tool4under5 ---")
if 'SMPS 4. 91. Namba ya mstari ya mwanakaya' in tool_under_5.columns:
    print("✗ tool4under5 HAINA column ya line number!")
    print("Available columns:")
    for col in tool_under_5.columns:
        if 'mstari' in col.lower() or 'line' in col.lower() or '91' in col:
            print(f"  - {col}")
else:
    dup_under5 = tool_under_5[tool_under_5.duplicated(
        subset=['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'], 
        keep=False
    )]
    print(f"Duplicates households katika under5: {len(dup_under5)}")
    if len(dup_under5) > 0:
        print("Sample:")
        print(dup_under5[['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa']].head())

# CHECK 2: Filter na clean wanakaya
print("\n--- STEP 2: Cleaning wanakaya ---")
watoto_chini_5 = tool_wanakaya[
    (tool_wanakaya['SMPS 4. Je, mwanakaya ana umri gani?'] < 5) | 
    (tool_wanakaya['SMPS 4. Ingiza umri wa mwanakaya kwa miezi'] < 60)
].copy()

print(f"Watoto walio chini ya miaka 5: {len(watoto_chini_5)}")

# Ondoa duplicates kutoka wanakaya (household + line number)
before_dup = len(watoto_chini_5)
watoto_chini_5 = watoto_chini_5.drop_duplicates(
    subset=['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 
            'SMPS 4. 91. Namba ya mstari ya mwanakaya'],
    keep='first'
)
after_dup = len(watoto_chini_5)
print(f"Baada ya kuondoa duplicates: {after_dup} (removed {before_dup - after_dup})")

# CHECK 3: Unganisha data
print("\n--- STEP 3: Merging data ---")

# Kwanza ondoa duplicates kutoka tool_under_5
tool_under_5_clean = tool_under_5.drop_duplicates(
    subset=['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'],
    keep='first'
)
print(f"tool4under5 baada ya kuondoa duplicates: {len(tool_under_5_clean)}")

# Unganisha kwa household ID
merged_data = pd.merge(
    watoto_chini_5,
    tool_under_5_clean,
    on='SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa',
    how='left',
    suffixes=('', '_under5')
)

print(f"Records baada ya kuunganisha: {len(merged_data)}")

# CHECK 4: Verify hakuna duplicates
dup_check = merged_data[merged_data.duplicated(
    subset=['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 
            'SMPS 4. 91. Namba ya mstari ya mwanakaya'],
    keep=False
)]

if len(dup_check) > 0:
    print(f"\n⚠️ ONYO: Kuna {len(dup_check)} duplicates!")
    print("Tunaondoa duplicates...")
    merged_data = merged_data.drop_duplicates(
        subset=['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 
                'SMPS 4. 91. Namba ya mstari ya mwanakaya'],
        keep='first'
    )
    print(f"Baada ya kuondoa: {len(merged_data)}")
else:
    print("✓ Hakuna duplicates!")

# Panga columns kwa mpangilio unaotakiwa
result = pd.DataFrame()

# Location info
result['National'] = merged_data['National']
result['Regions'] = merged_data['Regions']
result['Councils'] = merged_data['Councils']
result['Wards'] = merged_data['Wards']
result['Street/Villages'] = merged_data['Street/Villages']

# IDs
result['SMPS 4 : Namba Ya Utambulisho Wa Kijiji'] = merged_data['SMPS 4 : Namba Ya Utambulisho Wa Kijiji']
result['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'] = merged_data['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa']
result['SMPS 4. 91. Namba ya mstari ya mwanakaya'] = merged_data['SMPS 4. 91. Namba ya mstari ya mwanakaya']

# Child info
result['SMPS 4: Jinsia'] = merged_data['SMPS 4: Jinsia']
result['SMPS 4. 92. Jina la Kwanza'] = merged_data['SMPS 4. 92. Jina la Kwanza']
result['SMPS 4. 92. Jina la Kati'] = merged_data['SMPS 4. 92. Jina la Kati']
result['SMPS 4. 92. Jina la Ukoo'] = merged_data['SMPS 4. 92. Jina la Ukoo']
result['SMPS 4. Je, mwanakaya ana umri gani?'] = merged_data['SMPS 4. Je, mwanakaya ana umri gani?']
result['SMPS 4. Ingiza umri wa mwanakaya kwa miezi'] = merged_data['SMPS 4. Ingiza umri wa mwanakaya kwa miezi']

# Malaria test data
result['SMPS 4 Control'] = merged_data['SMPS 4 Control']
result['SMPS 4 Pf'] = merged_data['SMPS 4 Pf']
result['SMPS 4 Pan'] = merged_data['SMPS 4 Pan']
result['SMPS 4 Tafsiri ya Kipimo cha malaria'] = merged_data['SMPS 4 Tafsiri ya Kipimo cha malaria']
result['SMPS 4. Kama matokeo ya kipimo ni chanya. Je, amepatiwa dawa?'] = merged_data['SMPS 4. Kama matokeo ya kipimo ni chanya. Je, amepatiwa dawa?']
result['SMPS 4: Aina ya Alu aliyopewa'] = merged_data['SMPS 4: Aina ya Alu aliyopewa']
result['SMPS 4: Idadi ya vidonge alivyopewa kulingana na uzito na umri (Link na uzito uliochukuliwa kwenye general information) Min vidonge 6 and Max 24'] = merged_data['SMPS 4: Idadi ya vidonge alivyopewa kulingana na uzito na umri (Link na uzito uliochukuliwa kwenye general information) Min vidonge 6 and Max 24']
result['SMPS 4 Je, amepimwa kiwango cha wingi wa damu?'] = merged_data['SMPS 4 Je, amepimwa kiwango cha wingi wa damu?']
result['SMPS 4. Kama hapana toa sababu'] = merged_data['SMPS 4. Kama hapana toa sababu']
result['SMPS 4 Kiwango/wingi wa damu (Hb-g/dl)'] = merged_data['SMPS 4 Kiwango/wingi wa damu (Hb-g/dl)']
result['SMPS 4: MUAC (5cm-20cm)'] = merged_data['SMPS 4: MUAC (5cm-20cm)']
result['SMPS 4: Kuna watoto chini ya miaka 5'] = merged_data['SMPS 4: Kuna watoto chini ya miaka 5']

# FINAL CHECK: Verify hakuna duplicates
final_dup = result[result.duplicated(
    subset=['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 
            'SMPS 4. 91. Namba ya mstari ya mwanakaya'],
    keep=False
)]

print(f"\n--- FINAL VALIDATION ---")
print(f"✓ Total records: {len(result)}")
print(f"✓ Unique (household + line): {result[['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 'SMPS 4. 91. Namba ya mstari ya mwanakaya']].drop_duplicates().shape[0]}")
print(f"✓ Duplicates: {len(final_dup)}")

if len(final_dup) == 0:
    print("✓✓✓ PERFECT! Hakuna duplicates kabisa!")
else:
    print(f"✗✗✗ ERROR! Bado kuna {len(final_dup)} duplicates")

# Hifadhi matokeo
output_file = 'merged_children_household_data.csv'
result.to_csv(output_file, index=False)

print(f"\n✓ Data imehifadhiwa kwenye '{output_file}'")
print(f"✓ Kaya tofauti: {result['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'].nunique()}")
print(f"✓ Records zenye malaria test data: {result['SMPS 4 Tafsiri ya Kipimo cha malaria'].notna().sum()}")
print(f"✓ Records bila jina: {result['SMPS 4. 92. Jina la Kwanza'].isna().sum()}")

print("\n--- Sample ya data ---")
print(result[['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 
              'SMPS 4. 91. Namba ya mstari ya mwanakaya',
              'SMPS 4. 92. Jina la Kwanza', 
              'SMPS 4. Je, mwanakaya ana umri gani?',
              'SMPS 4 Tafsiri ya Kipimo cha malaria']].head(15))