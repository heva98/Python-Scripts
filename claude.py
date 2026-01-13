import pandas as pd
import numpy as np

# Soma CSV zote mbili
print("Inasoma faili za CSV...")
under5_df = pd.read_csv('tool-4-under-5.csv')
wanakaya_df = pd.read_csv('tool-4-wanakaya.csv')

# Ondoa whitespace kwenye column names
under5_df.columns = under5_df.columns.str.strip()
wanakaya_df.columns = wanakaya_df.columns.str.strip()

print(f"Idadi ya rekodi za watoto chini ya miaka 5: {len(under5_df)}")
print(f"Idadi ya rekodi za wanakaya: {len(wanakaya_df)}")

# Chagua columns zinazohitajika kutoka kila dataset
under5_cols = [
    'National', 'Regions', 'Councils', 'Wards', 'Street/Villages',
    'SMPS 4 : Namba Ya Utambulisho Wa Kijiji',
    'SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa',
    'SMPS 4 Control', 'SMPS 4 Pf', 'SMPS 4 Pan',
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

wanakaya_cols = [
    'SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa',
    'SMPS 4. 91. Namba ya mstari ya mwanakaya',
    'SMPS 4: Jinsia',
    'SMPS 4. 92. Jina la Kwanza',
    'SMPS 4. 92. Jina la Kati',
    'SMPS 4. 92. Jina la Ukoo',
    'SMPS 4. Je, mwanakaya ana umri gani?',
    'SMPS 4. Ingiza umri wa mwanakaya kwa miezi'
]

# Chagua columns zinazopo tu (ili kuepuka errors kama column haipo)
under5_selected = under5_df[[col for col in under5_cols if col in under5_df.columns]].copy()
wanakaya_selected = wanakaya_df[[col for col in wanakaya_cols if col in wanakaya_df.columns]].copy()

# Unganisha datasets kulingana na namba ya kaya
print("\nInaunganisha data...")
merged_df = pd.merge(
    under5_selected,
    wanakaya_selected,
    on='SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa',
    how='left'
)

# Chuja watoto chini ya miaka 5 tu
print("\nInachuja watoto chini ya miaka 5...")
initial_merged = len(merged_df)

# Chagua watoto wenye umri chini ya 5 (kulingana na miaka) AU wenye umri kwa miezi
umri_miaka_col = 'SMPS 4. Je, mwanakaya ana umri gani?'
umri_miezi_col = 'SMPS 4. Ingiza umri wa mwanakaya kwa miezi'

# Chuja: chukua tu wenye umri < 5 miaka AU wenye umri kwa miezi (watoto wadogo)
if umri_miaka_col in merged_df.columns and umri_miezi_col in merged_df.columns:
    merged_df = merged_df[
        (merged_df[umri_miaka_col] < 5) | 
        (merged_df[umri_miaka_col].isna() & merged_df[umri_miezi_col].notna()) |
        (merged_df[umri_miezi_col] < 60)  # chini ya 60 miezi = chini ya miaka 5
    ].copy()
    
    watoto_waliokataliwa = initial_merged - len(merged_df)
    print(f"Watoto wenye umri wa miaka 5+ walioondolewa: {watoto_waliokataliwa}")
elif umri_miaka_col in merged_df.columns:
    merged_df = merged_df[merged_df[umri_miaka_col] < 5].copy()
    watoto_waliokataliwa = initial_merged - len(merged_df)
    print(f"Watoto wenye umri wa miaka 5+ walioondolewa: {watoto_waliokataliwa}")

# Panga columns kwa mpangilio unaotakiwa
final_columns = [
    'National', 'Regions', 'Councils', 'Wards', 'Street/Villages',
    'SMPS 4 : Namba Ya Utambulisho Wa Kijiji',
    'SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa',
    'SMPS 4. 91. Namba ya mstari ya mwanakaya',
    'SMPS 4: Jinsia',
    'SMPS 4. 92. Jina la Kwanza',
    'SMPS 4. 92. Jina la Kati',
    'SMPS 4. 92. Jina la Ukoo',
    'SMPS 4. Je, mwanakaya ana umri gani?',
    'SMPS 4. Ingiza umri wa mwanakaya kwa miezi',
    'SMPS 4 Control', 'SMPS 4 Pf', 'SMPS 4 Pan',
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

# Panga columns (chagua tu zilizopo)
final_df = merged_df[[col for col in final_columns if col in merged_df.columns]].copy()

# Ondoa duplicates kulingana na kaya na namba ya mstari
print("\nInaondoa duplicates...")
initial_count = len(final_df)
final_df = final_df.drop_duplicates(
    subset=['SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa', 
            'SMPS 4. 91. Namba ya mstari ya mwanakaya'],
    keep='first'
)
duplicates_removed = initial_count - len(final_df)

# Hifadhi kwenye CSV mpya
output_file = 'watoto_chini_ya_miaka_5_combined.csv'
final_df.to_csv(output_file, index=False)

# Onyesha takwimu
print(f"\n{'='*60}")
print("TAKWIMU ZA DATA:")
print(f"{'='*60}")
print(f"Jumla ya rekodi baada ya kuunganisha: {initial_count}")
print(f"Duplicates zilizoondolewa: {duplicates_removed}")
print(f"Jumla ya rekodi final: {len(final_df)}")

# Angalia idadi ya taarifa za malaria
malaria_col = 'SMPS 4 Tafsiri ya Kipimo cha malaria'
if malaria_col in final_df.columns:
    malaria_count = final_df[malaria_col].notna().sum()
    print(f"\nIdadi ya taarifa za kipimo cha malaria: {malaria_count}")
    if malaria_count < 9109:
        print(f"⚠️ ONYO: Taarifa za malaria ni {malaria_count}, chini ya 9109 inayotarajiwa!")
    else:
        print(f"✓ Taarifa za malaria ni ya kutosha ({malaria_count} >= 9109)")

print(f"\n{'='*60}")
print(f"Faili imehifadhiwa kama: {output_file}")
print(f"{'='*60}")

# Onyesha sampuli ya data
print("\nSampuli ya rekodi 5 za kwanza:")
print(final_df.head().to_string())