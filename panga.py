import pandas as pd

# 1. Pakia data
missing = pd.read_csv('tool-4-under-5-missing.csv')
wanakaya = pd.read_csv('tool-4-wanakaya.csv')

# 2. Safisha IDs (kuondoa space)
id_col = 'SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa'
missing[id_col] = missing[id_col].astype(str).str.strip()
wanakaya[id_col] = wanakaya[id_col].astype(str).str.strip()

# 3. Chuja watoto pekee (< 5) na chukua mmoja kwa kila kaya (kuzuia duplicates)
watoto = wanakaya[wanakaya['SMPS 4. Je, mwanakaya ana umri gani?'] < 5].copy()
watoto_unique = watoto.drop_duplicates(subset=[id_col])

# 4. Unganisha kwa kutumia LEFT JOIN (Msingi ni zile 923)
columns_to_bring = [
    id_col, 'SMPS 4. 91. Namba ya mstari ya mwanakaya', 'SMPS 4: Jinsia',
    'SMPS 4. 92. Jina la Kwanza', 'SMPS 4. 92. Jina la Kati', 'SMPS 4. 92. Jina la Ukoo',
    'SMPS 4. Je, mwanakaya ana umri gani?', 'SMPS 4. Ingiza umri wa mwanakaya kwa miezi'
]

final_data = pd.merge(missing, watoto_unique[columns_to_bring], on=id_col, how='left')

# 5. Panga columns kulingana na mlolongo ulioomba
ordered_cols = [
    'National', 'Regions', 'Councils', 'Wards', 'Street/Villages',
    'SMPS 4 : Namba Ya Utambulisho Wa Kijiji', id_col,
    'SMPS 4. 91. Namba ya mstari ya mwanakaya', 'SMPS 4: Jinsia',
    'SMPS 4. 92. Jina la Kwanza', 'SMPS 4. 92. Jina la Kati', 'SMPS 4. 92. Jina la Ukoo',
    'SMPS 4. Je, mwanakaya ana umri gani?', 'SMPS 4. Ingiza umri wa mwanakaya kwa miezi',
    'SMPS 4 Control', 'SMPS 4 Pf', 'SMPS 4 Pan', 'SMPS 4 Tafsiri ya Kipimo cha malaria',
    'SMPS 4. Kama matokeo ya kipimo ni chanya. Je, amepatiwa dawa?',
    'SMPS 4: Aina ya Alu aliyopewa',
    'SMPS 4: Idadi ya vidonge alivyopewa kulingana na uzito na umri (Link na uzito uliochukuliwa kwenye general information) Min vidonge 6 and Max 24',
    'SMPS 4 Je, amepimwa kiwango cha wingi wa damu?'
]

# Hifadhi matokeo
final_data[ordered_cols].to_csv('final_missing_923.csv', index=False)
print("Faili la kaya 923 limekamilika!")