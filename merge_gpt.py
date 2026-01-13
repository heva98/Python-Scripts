import pandas as pd

# Soma data
under5 = pd.read_csv("tool-4-under-5.csv", low_memory=False)
wanakaya = pd.read_csv("tool-4-wanakaya.csv", low_memory=False)

# Chuja wanakaya: watoto waliokubalika
wanakaya_children = wanakaya[
    (wanakaya["SMPS 4. Je, mwanakaya ana umri gani?"] <= 5) &
    (wanakaya["SMPS 4. Ingiza umri wa mwanakaya kwa miezi"].notna())
]

# Merge kwa KEY MOJA TU: Namba ya kaya
final = pd.merge(
    under5,
    wanakaya_children,
    how="left",
    on="SMPS 4. Namba ya utambulisho wa kaya iliyochaguliwa",
    suffixes=("_under5", "")
)

# Save
final.to_csv("tool-4-under5-linked-SIMPLE.csv", index=False)

print("DONE ✅")
print("Rows:", len(final))
