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

# Angalia unique households
print(f"\nUnique households katika under-5: {tool_under_5['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'].nunique()}")
print(f"Unique households katika wanakaya: {tool_wanakaya['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'].nunique()}")

# Filter wanakaya - chagua watoto walio chini ya miaka 5 TU
watoto_chini_5 = tool_wanakaya[
    (tool_wanakaya['SMPS 4. Je, mwanakaya ana umri gani?'] < 5) | 
    (tool_wanakaya['SMPS 4. Ingiza umri wa mwanakaya kwa miezi'] < 60)
].copy()

print(f"\nWatoto walio chini ya miaka 5 kutoka wanakaya: {len(watoto_chini_5)}")

# Ondoa duplicates kutoka tool-4-under-5 
# Tutumia household ID na village ID kama unique identifier
tool_under_5_clean = tool_under_5.drop_duplicates(
    subset=['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'], 
    keep='first'
)

print(f"Records za under-5 baada ya kuondoa duplicates: {len(tool_under_5_clean)}")

# Unganisha datasets - left join kutoka watoto
merged_data = pd.merge(
    watoto_chini_5,
    tool_under_5_clean,
    on='SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa',
    how='left',
    suffixes=('', '_under5')
)

print(f"\nRecords baada ya kuunganisha: {len(merged_data)}")

# Tumia columns kutoka wanakaya kwa location info (National, Regions, etc)
# na columns kutoka under-5 kwa malaria test data

# Panga columns kwa mpangilio unaotakiwa
result = pd.DataFrame()

result['National'] = merged_data['National']
result['Regions'] = merged_data['Regions']
result['Councils'] = merged_data['Councils']
result['Wards'] = merged_data['Wards']
result['Street/Villages'] = merged_data['Street/Villages']
result['SMPS 4 : Namba Ya Utambulisho Wa Kijiji'] = merged_data['SMPS 4 : Namba Ya Utambulisho Wa Kijiji']
result['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'] = merged_data['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa']
result['SMPS 4. 91. Namba ya mstari ya mwanakaya'] = merged_data['SMPS 4. 91. Namba ya mstari ya mwanakaya']
result['SMPS 4: Jinsia'] = merged_data['SMPS 4: Jinsia']
result['SMPS 4. 92. Jina la Kwanza'] = merged_data['SMPS 4. 92. Jina la Kwanza']
result['SMPS 4. 92. Jina la Kati'] = merged_data['SMPS 4. 92. Jina la Kati']
result['SMPS 4. 92. Jina la Ukoo'] = merged_data['SMPS 4. 92. Jina la Ukoo']
result['SMPS 4. Je, mwanakaya ana umri gani?'] = merged_data['SMPS 4. Je, mwanakaya ana umri gani?']
result['SMPS 4. Ingiza umri wa mwanakaya kwa miezi'] = merged_data['SMPS 4. Ingiza umri wa mwanakaya kwa miezi']
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

# Hifadhi matokeo
output_file = 'merged_children_household_data.csv'
result.to_csv(output_file, index=False)

print(f"\n✓ Mafanikio! Data imehifadhiwa kwenye '{output_file}'")
print(f"✓ Jumla ya watoto: {len(result)}")
print(f"✓ Kaya tofauti: {result['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'].nunique()}")

# Angalia kuna duplicates?
duplicates = result[result.duplicated(subset=['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 'SMPS 4. 91. Namba ya mstari ya mwanakaya'], keep=False)]
print(f"✓ Duplicates (same household + line number): {len(duplicates)}")

# Muhtasari wa umri
print("\n--- Muhtasari wa Umri ---")
print(result['SMPS 4. Je, mwanakaya ana umri gani?'].value_counts().sort_index())

# Muhtasari wa malaria tests
print("\n--- Malaria Tests ---")
print(f"Waliopimwa: {result['SMPS 4 Tafsiri ya Kipimo cha malaria'].notna().sum()}")
print(f"Wasiojua (missing data): {result['SMPS 4 Tafsiri ya Kipimo cha malaria'].isna().sum()}")

print("\n--- Sampuli ya data (mistari 10 ya kwanza) ---")
print(result[['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 
              'SMPS 4. 91. Namba ya mstari ya mwanakaya',
              'SMPS 4. 92. Jina la Kwanza', 
              'SMPS 4. Je, mwanakaya ana umri gani?',
              'SMPS 4: Jinsia',
              'SMPS 4 Tafsiri ya Kipimo cha malaria']].head(10))