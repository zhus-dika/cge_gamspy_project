import numpy as np
import copy
import pandas as pd
import os

# load social accounting matrix
current_path = os.path.abspath(os.path.dirname(__file__))
sam_path = os.path.join(current_path, "data", "Databank_CGE_2017.xlsx")
df_sam2 = pd.read_excel(sam_path, sheet_name="read_format_KZT", index_col=0, header=0)
df_sam2 = df_sam2.fillna(0.)

num_commodities = 34

# create new dataframe with sam in format of type 1
factors = [69, 70]#["K", "L"]
agents = [71, 72, 73, 74, 75]#["HH_bottom40R", "HH_top60R", "HH_bottom40U", "HH_top60U", "Govt"]
taxes = [76, 77, 78, 79, 80]#["TC", "TE", "TK", "TY"]
inv = [81] #["Investment"]
row = [82]#["ROW"]
ind_full = list(range(1, 2 * num_commodities + 1))
ind = list(range(1, num_commodities + 1))

points_full = ind_full + factors + agents + taxes + inv + row
points = ind + factors + agents + taxes + inv + row
points_without_ind = factors + agents + taxes + inv + row

num_rows = len(points_full)

idx2points = {el: points_full[i] for i, el in enumerate(df_sam2.index[:num_rows])}
col2points = {el: points_full[i] for i, el in enumerate(df_sam2.columns[:num_rows])}

# drop other rows & columns
df_sam2.drop(df_sam2.index[num_rows + 1:], inplace=True)
df_sam2.drop(columns=df_sam2.columns[num_rows:], inplace=True)

# rename rows & columns
df_sam2.rename(index=idx2points, inplace=True)
df_sam2.rename(columns=col2points, inplace=True)

# create sam in format type1
df_sam1 = copy.deepcopy(df_sam2)
df_sam1.drop(df_sam2.index[num_commodities:2 * num_commodities], inplace=True)
df_sam1.drop(columns=df_sam2.columns[num_commodities:2 * num_commodities], inplace=True)
#************* read data from sam2 *************#
for j in ind:
    for i in ind:
        df_sam1.loc[i, j] = df_sam2.loc[i + num_commodities, j]
    df_sam1.loc[j, points_without_ind[0]:] = df_sam2.loc[j, points_without_ind[0]:] + df_sam2.loc[j + num_commodities, points_without_ind[0]:]

for point in points_without_ind:
    for i in ind:
        df_sam1.loc[point, i] = df_sam2.loc[point, i] + df_sam2.loc[point, i + num_commodities]
for i in ind:
    df_sam1.loc[i, i] = df_sam2.loc[i, i + num_commodities] - df_sam1.loc[i, i]

df_sam1.loc[21, 19] -= 288790.8387262111

# check
for i in ind:
    if abs(df_sam1.loc[i].sum() - df_sam1[i].sum()) >= 1e-07:
        print(i)
        print("df_sam1.loc[i].sum()", df_sam1.loc[i].sum())
        print("df_sam1[i].sum()", df_sam1[i].sum())
        print(df_sam1.loc[i].sum() - df_sam1[i].sum())

# unite "HH_bottom40R", "HH_top60R", "HH_bottom40U", "HH_top60U" factors to single "HOH" factor
# by rows
df_sam1.loc[71] = df_sam1.loc[71:74].sum()
# by columns
df_sam1[71] = df_sam1[71] + df_sam1[72] + df_sam1[73] + df_sam1[74]
# drop other columns
df_sam1.drop(columns=[72, 73, 74], inplace=True)
# rename columns
df_sam1.rename(columns={
    1: "Agriculture",
    2: "Coal extraction",
    3: "Extraction of crude oil",
    4: "Extraction of natural gas",
    5: "Mining of iron ores",
    6: "Mining of non-ferrous metals",
    7: "Other mining",
    8: "Food industry",
    9: "Paper, pulp and print",
    10: "Other light industry",
    11: "Ferrous metallurgy",
    12: "Non-ferrous merallurgy",
    13: "other metallurgy",
    14: "Oil refining",
    15: "Chemical industry",
    16: "Mineral products",
    17: "Machinery",
    18: "Other manufacturing and construction",
    19: "Public electricity",
    20: "Natural Gas production and distribution",
    21: "Heat and hot water supply",
    22: "Water and waste management",
    23: "Land transport",
    24: "Water transport",
    25: "Air transport",
    26: "Construction",
    27: "Trade",
    28: "Information and communication",
    29: "Financial services",
    30: "Real estate transactions",
    31: "Professional, scientific and technical activities",
    32: "Education",
    33: "Health care services",
    34: "Other services",
    69: "CAP", 70: "LAB", 71: "HOH", 75: "GOV", 76: "TC", 77: "TE", 78: "TK", 79: "TI", 80: "TY", 81: "INV", 82: "EXT"}, inplace=True)
    # 69: "CAP", 70: "LAB", 71: "HOH", 75: "GOV", 76: "IDT", 77: "TE", 78: "TK", 79: "TRF", 80: "TRF", 81: "INV", 82: "EXT"}, inplace=True)
# drop other rows
df_sam1.drop(index=[72, 73, 74], inplace=True)
# rename rows
df_sam1.rename(index={
    1: "Agriculture",
    2: "Coal extraction",
    3: "Extraction of crude oil",
    4: "Extraction of natural gas",
    5: "Mining of iron ores",
    6: "Mining of non-ferrous metals",
    7: "Other mining",
    8: "Food industry",
    9: "Paper, pulp and print",
    10: "Other light industry",
    11: "Ferrous metallurgy",
    12: "Non-ferrous merallurgy",
    13: "other metallurgy",
    14: "Oil refining",
    15: "Chemical industry",
    16: "Mineral products",
    17: "Machinery",
    18: "Other manufacturing and construction",
    19: "Public electricity",
    20: "Natural Gas production and distribution",
    21: "Heat and hot water supply",
    22: "Water and waste management",
    23: "Land transport",
    24: "Water transport",
    25: "Air transport",
    26: "Construction",
    27: "Trade",
    28: "Information and communication",
    29: "Financial services",
    30: "Real estate transactions",
    31: "Professional, scientific and technical activities",
    32: "Education",
    33: "Health care services",
    34: "Other services",
    69: "CAP", 70: "LAB", 71: "HOH", 75: "GOV", 76: "TC", 77: "TE", 78: "TK", 79: "TI", 80: "TY", 81: "INV", 82: "EXT"},
    inplace=True)
    # 69: "CAP", 70: "LAB", 71: "HOH", 75: "GOV", 76: "IDT", 77: "TE", 78: "TK", 79: "TRF", 80: "TY", 81: "INV", 82: "EXT"}, inplace=True)
# save data to file
df_sam1.to_excel(os.path.join(current_path, "data", "databank_2017_type1_KZT.xlsx"))