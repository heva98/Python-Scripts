import pandas as pd
import numpy as np

# Soma CSV files
print("Inasoma files...")
tool_under_5 = pd.read_csv('tool-4-under-5.csv')
tool_wanakaya = pd.read_csv('tool-4-wanakaya.csv')

# Strip whitespace from column names
tool_under_5.columns = tool_under_5.columns.str.strip()
tool_wanakaya.columns = tool_wanakaya.columns.str.strip()

print(f"Records katika tool-4-under-5: {len(tool_under_5)}")
print(f"Records katika tool-4-wanakaya: {len(tool_wanakaya)}")

# Onyesha samples za data kwa debugging
print("\n--- Sample ya tool-4-under-5 ---")
print(tool_under_5[['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa']].head())
print("\n--- Sample ya tool-4-wanakaya ---")
print(tool_wanakaya[['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 'SMPS 4. 91. Namba ya mstari ya mwanakaya']].head())

# Chagua columns kutoka tool-4-under-5 (malaria test data)
under5_cols = [
    'SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa',
    'SMPS 4 : Namba Ya Utambulisho Wa Kijiji',
    'SMPS 4 Control',
    'SMPS 4 Pf',
    'SMPS 4 Pan',
    'SMPS 4 Tafsiri ya Kipimo cha malaria',
    'SMPS 4. Kama matokeo ya kipimo ni chanya. Je, amepatiwa dawa?',
    'SMPS 4: Aina ya Alu aliyopewa',
    'SMPS 4: Idadi ya vidonge alivyopewa kulingana na uzito na umri (Link na uzito uliochukuliwa kwenye general information) Min vidonge 6 and Max 24',
    'SMPS 4 Je, amepimwa kiwango cha wingi wa damu?',
    'SMPS 4. Kama hapana toa sababu',
    'SMPS 4 Kiwango/wingi wa damu (Hb-g/dl)',
    'SMPS 4: MUAC (5cm-20cm)',
    'SMPS 4: Kuna watoto chini ya miaka 5'
]

# Chagua columns kutoka tool-4-wanakaya (household member data)
wanakaya_cols = [
    'National',
    'Regions',
    'Councils',
    'Wards',
    'Street/Villages',
    'SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa',
    'SMPS 4. 91. Namba ya mstari ya mwanakaya',
    'SMPS 4: Jinsia',
    'SMPS 4. 92. Jina la Kwanza',
    'SMPS 4. 92. Jina la Kati',
    'SMPS 4. 92. Jina la Ukoo',
    'SMPS 4. Je, mwanakaya ana umri gani?',
    'SMPS 4. Ingiza umri wa mwanakaya kwa miezi'
]

# Chagua columns zilizopo tu
under5_cols_available = [col for col in under5_cols if col in tool_under_5.columns]
wanakaya_cols_available = [col for col in wanakaya_cols if col in tool_wanakaya.columns]

# Chagua data
under5_selected = tool_under_5[under5_cols_available].copy()
wanakaya_selected = tool_wanakaya[wanakaya_cols_available].copy()

print(f"\n--- Kabla ya kuunganisha ---")
print(f"Unique households katika under-5: {under5_selected['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'].nunique()}")
print(f"Unique households katika wanakaya: {wanakaya_selected['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'].nunique()}")

# Ondoa duplicates kutoka tool-4-under-5 kwa household ID
# Kwa sababu tool-4-under-5 inafaa kuwa na record moja tu kwa kila household
under5_selected = under5_selected.drop_duplicates(subset=['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'], keep='first')

print(f"\nBaada ya kuondoa duplicates kutoka under-5: {len(under5_selected)} records")

# Unganisha datasets - LEFT JOIN kutoka wanakaya ili kupata watoto wote walio chini ya miaka 5
merged_data = pd.merge(
    wanakaya_selected,
    under5_selected,
    on='SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa',
    how='left'
)

print(f"\nRecords baada ya kuunganisha: {len(merged_data)}")

# Filter watoto walio chini ya miaka 5 (umri <= 4 miaka AU umri kwa miezi <= 59)
# Hesabu umri kwa miaka kutoka umri kwa miezi
merged_data['umri_miaka'] = merged_data['SMPS 4. Ingiza umri wa mwanakaya kwa miezi'] / 12

# Chagua watoto walio chini ya miaka 5
children_under_5 = merged_data[
    (merged_data['SMPS 4. Je, mwanakaya ana umri gani?'] < 5) | 
    (merged_data['SMPS 4. Ingiza umri wa mwanakaya kwa miezi'] < 60)
].copy()

# Ondoa temporary column
children_under_5 = children_under_5.drop('umri_miaka', axis=1)

print(f"\nWatoto walio chini ya miaka 5: {len(children_under_5)}")

# Panga columns kwa mpangilio unaotakiwa
final_column_order = [
    'National',
    'Regions',
    'Councils',
    'Wards',
    'Street/Villages',
    'SMPS 4 : Namba Ya Utambulisho Wa Kijiji',
    'SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa',
    'SMPS 4. 91. Namba ya mstari ya mwanakaya',
    'SMPS 4: Jinsia',
    'SMPS 4. 92. Jina la Kwanza',
    'SMPS 4. 92. Jina la Kati',
    'SMPS 4. 92. Jina la Ukoo',
    'SMPS 4. Je, mwanakaya ana umri gani?',
    'SMPS 4. Ingiza umri wa mwanakaya kwa miezi',
    'SMPS 4 Control',
    'SMPS 4 Pf',
    'SMPS 4 Pan',
    'SMPS 4 Tafsiri ya Kipimo cha malaria',
    'SMPS 4. Kama matokeo ya kipimo ni chanya. Je, amepatiwa dawa?',
    'SMPS 4: Aina ya Alu aliyopewa',
    'SMPS 4: Idadi ya vidonge alivyopewa kulingana na uzito na umri (Link na uzito uliochukuliwa kwenye general information) Min vidonge 6 and Max 24',
    'SMPS 4 Je, amepimwa kiwango cha wingi wa damu?',
    'SMPS 4. Kama hapana toa sababu',
    'SMPS 4 Kiwango/wingi wa damu (Hb-g/dl)',
    'SMPS 4: MUAC (5cm-20cm)',
    'SMPS 4: Kuna watoto chini ya miaka 5'
]

# Chagua columns zilizopo tu
available_final_cols = [col for col in final_column_order if col in children_under_5.columns]
result = children_under_5[available_final_cols].copy()

# Hifadhi matokeo
output_file = 'merged_children_household_data.csv'
result.to_csv(output_file, index=False)

print(f"\n✓ Mafanikio! Data imehifadhiwa kwenye '{output_file}'")
print(f"✓ Jumla ya watoto walio chini ya miaka 5: {len(result)}")
print(f"✓ Kaya tofauti: {result['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'].nunique()}")

# Onyesha muhtasari
print("\n--- Muhtasari wa Umri ---")
print(result['SMPS 4. Je, mwanakaya ana umri gani?'].value_counts().sort_index())

print("\n--- Sampuli ya data (mistari 5 ya kwanza) ---")
print(result[['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 
              'SMPS 4. 92. Jina la Kwanza', 
              'SMPS 4. Je, mwanakaya ana umri gani?',
              'SMPS 4: Jinsia']].head(10))