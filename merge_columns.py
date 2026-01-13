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

# Angalia columns
print("\nColumns katika tool4under5:")
print(tool_under_5.columns.tolist())

# Angalia kama kuna line number column katika tool4under5
if 'SMPS 4. 91. Namba ya mstari ya mwanakaya' in tool_under_5.columns:
    print("\n✓ Namba ya mstari ipo katika tool4under5")
    print(f"Sample ya line numbers: {tool_under_5['SMPS 4. 91. Namba ya mstari ya mwanakaya'].head(10).tolist()}")
else:
    print("\n✗ Namba ya mstari HAIPO katika tool4under5")
    print("Tunahitaji kuongeza hii column kwanza!")

# Filter wanakaya - chagua watoto walio chini ya miaka 5 TU
watoto_chini_5 = tool_wanakaya[
    (tool_wanakaya['SMPS 4. Je, mwanakaya ana umri gani?'] < 5) | 
    (tool_wanakaya['SMPS 4. Ingiza umri wa mwanakaya kwa miezi'] < 60)
].copy()

print(f"\nWatoto walio chini ya miaka 5 kutoka wanakaya: {len(watoto_chini_5)}")

# Check kama line number ipo katika tool4under5
if 'SMPS 4. 91. Namba ya mstari ya mwanakaya' in tool_under_5.columns:
    # UNGANISHA KWA HOUSEHOLD ID **NA** LINE NUMBER
    merge_keys = [
        'SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa',
        'SMPS 4. 91. Namba ya mstari ya mwanakaya'
    ]
    
    print(f"\nKuunganisha kwa: {merge_keys}")
    
    merged_data = pd.merge(
        tool_under_5,
        watoto_chini_5,
        on=merge_keys,
        how='left',
        suffixes=('_under5', '_wanakaya')
    )
else:
    # Kama hakuna line number, unganisha kwa household ID tu
    print("\nKuunganisha kwa household ID peke yake (TATIZO!)")
    
    merged_data = pd.merge(
        tool_under_5,
        watoto_chini_5,
        on='SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa',
        how='left',
        suffixes=('_under5', '_wanakaya')
    )

print(f"\nRecords baada ya kuunganisha: {len(merged_data)}")

# Panga columns kwa mpangilio unaotakiwa
result = pd.DataFrame()

# Location info - tumia kutoka wanakaya (zaidi ya specific)
result['National'] = merged_data['National_wanakaya'].fillna(merged_data['National_under5'])
result['Regions'] = merged_data['Regions_wanakaya'].fillna(merged_data['Regions_under5'])
result['Councils'] = merged_data['Councils_wanakaya'].fillna(merged_data['Councils_under5'])
result['Wards'] = merged_data['Wards_wanakaya'].fillna(merged_data['Wards_under5'])
result['Street/Villages'] = merged_data['Street/Villages_wanakaya'].fillna(merged_data['Street/Villages_under5'])

# IDs
result['SMPS 4 : Namba Ya Utambulisho Wa Kijiji'] = merged_data['SMPS 4 : Namba Ya Utambulisho Wa Kijiji']
result['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'] = merged_data['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa']

# Line number - chagua kutoka under5 kama ipo, vinginevyo kutoka wanakaya
if 'SMPS 4. 91. Namba ya mstari ya mwanakaya' in tool_under_5.columns:
    result['SMPS 4. 91. Namba ya mstari ya mwanakaya'] = merged_data['SMPS 4. 91. Namba ya mstari ya mwanakaya']
else:
    result['SMPS 4. 91. Namba ya mstari ya mwanakaya'] = merged_data['SMPS 4. 91. Namba ya mstari ya mwanakaya']

# Child info kutoka wanakaya
result['SMPS 4: Jinsia'] = merged_data['SMPS 4: Jinsia']
result['SMPS 4. 92. Jina la Kwanza'] = merged_data['SMPS 4. 92. Jina la Kwanza']
result['SMPS 4. 92. Jina la Kati'] = merged_data['SMPS 4. 92. Jina la Kati']
result['SMPS 4. 92. Jina la Ukoo'] = merged_data['SMPS 4. 92. Jina la Ukoo']
result['SMPS 4. Je, mwanakaya ana umri gani?'] = merged_data['SMPS 4. Je, mwanakaya ana umri gani?']
result['SMPS 4. Ingiza umri wa mwanakaya kwa miezi'] = merged_data['SMPS 4. Ingiza umri wa mwanakaya kwa miezi']

# Malaria test data kutoka under-5
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

print(f"\n✓ MAFANIKIO! Data imehifadhiwa kwenye '{output_file}'")
print(f"✓ Jumla ya records: {len(result)} (expected: 15952)")
print(f"✓ Kaya tofauti: {result['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'].nunique()}")

# Angalia duplicates - lazima hakuna!
duplicates = result[result.duplicated(subset=['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 'SMPS 4. 91. Namba ya mstari ya mwanakaya'], keep=False)]
print(f"✓ Duplicates (same household + line): {len(duplicates)}")

if len(duplicates) > 0:
    print("\n⚠️ ONYO: Kuna duplicates! Hebu tuangalie:")
    print(duplicates[['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 
                      'SMPS 4. 91. Namba ya mstari ya mwanakaya',
                      'SMPS 4. 92. Jina la Kwanza']].head(20))

# Angalia records zisizo na taarifa za mtoto
missing_child_info = result['SMPS 4. 92. Jina la Kwanza'].isna().sum()
print(f"✓ Records bila jina la mtoto: {missing_child_info}")

if missing_child_info > 0:
    print(f"   ({missing_child_info / len(result) * 100:.1f}% ya records)")

print("\n--- Sampuli ya data (mistari 10 ya kwanza) ---")
print(result[['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 
              'SMPS 4. 91. Namba ya mstari ya mwanakaya',
              'SMPS 4. 92. Jina la Kwanza', 
              'SMPS 4. Je, mwanakaya ana umri gani?',
              'SMPS 4 Tafsiri ya Kipimo cha malaria']].head(10))