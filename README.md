# cge_gamspy
## Running guide

- `cd .\Documents\zhus_dika\CGE_projects\cge_gamspy_project\`
- `.\cge_gamspy\Scripts\activate`
- `pip install -r requirements.txt`

## Scripts' description

### *convert_sam_types.py* 

convert full format of SAM table 

<img src="https://github.com/zhus-dika/cge_gamspy_project/blob/main/data/sam_type_2.jpeg" alt="drawing" width="650"/>

to short format:

<img src="https://github.com/zhus-dika/cge_gamspy_project/blob/main/data/sam_type_1.PNG" alt="drawing" width="650"/>

### *aggregate.py* 

compress of industries to overcome the limitation of the gams license

### *main.py* 

example gamspy code

### *main_custom.py* 

main gamspy code for custom data

## Industries
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
    34: "Other services"

## Tax Structure in the SAM

This project uses the following tax structure based on the Social Accounting Matrix (SAM).

| Tax Code | Tax Name                                      | Type of Tax    | Paid By                | SAM Position                |
|----------|-----------------------------------------------|----------------|------------------------|-----------------------------|
| TC       | Taxes on Consumption of Domestic Products     | Indirect Tax   | Households (HOH)       | Row: "TC"                  |
| TE       | Taxes on Exports Paid by Rest of the World   | Indirect Tax   | Rest of the World (ROW)| Row: "TE"                  |
| TK       | Direct Taxes on Production                   | Indirect Tax   | Industries (i)         | Row: "TK"                  |
| TY       | Taxes on Income                              | Direct Tax     | Households (HOH)       | Row: "GOV", Column: "HOH" |

### Notes
- Indirect Taxes (TC, TE, TK) are included in product prices or production costs.
- Direct Taxes (TY) are collected from household income.
- In the SAM table:
  - Rows indicate *who paid* the tax.
  - Columns indicate *to whom* the tax was paid (usually the Government "GOV").

---

### Example in the SAM Table:

| From / To | Industries | HOH   | ROW   | GOV   |
|-----------|------------|-------|-------|-------|
| TC        | -          | -     | -     | +     |
| TE        | -          | -     | -     | +     |
| TK        | -          | -     | -     | +     |
| TY        | -          | -     | -     | +     |

---

### Usage in the Model

When building the CGE model:

- TC → Affects consumption demand equations.
- TE → Affects export price equations.
- TK → Affects production cost equations.
- TY → Enters directly into the household budget constraint.
