import pandas as pd

# Soma data
under5 = pd.read_csv("tool-4-under-5-missing.csv")
wanakaya = pd.read_csv("tool-4-wanakaya-use1.csv")

# Chuja wanakaya chini ya miaka 5
wanakaya_under5 = wanakaya[
    (wanakaya['SMPS 4. Je, mwanakaya ana umri gani?'] < 5) |
    (wanakaya['SMPS 4. Ingiza umri wa mwanakaya kwa miezi'].notna())
]

# Merge (chukua location kutoka under5)
merged_df = pd.merge(
    under5,
    wanakaya_under5,
    on=[
        'SMPS 4 : Namba Ya Utambulisho Wa Kijiji',
        'SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'
    ],
    how='left',
    suffixes=('', '_wk')
)

# Angalia columns (debug – unaweza ku-comment baadae)
print(merged_df.columns.tolist())

# Chagua columns kwa usalama
final_df = merged_df[
    [
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
]

# Save file
final_df.to_csv("tool4_under5_final.csv", index=False)

print("✅ Imefanikiwa: tool4_under5_final.csv")
