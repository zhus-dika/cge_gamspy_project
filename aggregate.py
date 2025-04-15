import pandas as pd
import os
import numpy as np


# Industries mapping
aggregation_mapping_5 = {
    "Primary and Light Industry": [
        # Базовые ресурсы и потребительская лёгкая промышленность
        'Agriculture', 'Coal extraction', 'Extraction of crude oil',
        'Extraction of natural gas', 'Mining of iron ores',
        'Mining of non-ferrous metals', 'Other mining',
        'Food industry', 'Paper, pulp and print', 'Other light industry'
    ],
    "Heavy Industry and Manufacturing": [
        # Вся тяжёлая, химия, машиностроение, стройка
        'Ferrous metallurgy', 'Non-ferrous merallurgy', 'other metallurgy', 'Oil refining',
        'Chemical industry', 'Mineral products',
        'Machinery', 'Other manufacturing and construction',
        'Construction'
    ],
    "Utilities and Transport": [
        # Энергетика, вода, транспорт
        'Public electricity', 'Natural Gas production and distribution',
        'Heat and hot water supply', 'Water and waste management',
        'Land transport', 'Water transport', 'Air transport'
    ],
    "Trade and Finance": [
        # Торговля, связь, финансы, недвижимость
        'Trade', 'Information and communication',
        'Financial services', 'Real estate transactions'
    ],
    "Social and Professional Services": [
        # Соцсфера, наука, услуги
        'Professional, scientific and technical activities',
        'Education', 'Health care services', 'Other services'
    ]
}


def aggregate_sam(df, aggregation_mapping):
    # Агрегируем строки
    aggregated_rows = df.groupby(lambda x: next((agg_name for agg_name, sectors in aggregation_mapping.items() if x in sectors), x)).sum()
    # Агрегируем столбцы
    aggregated_cols = aggregated_rows.T.groupby(lambda x: next((agg_name for agg_name, sectors in aggregation_mapping.items() if x in sectors), x)).sum().T

    return aggregated_cols


def check_balance(df, tol=1e-5):
    imbalance = (df.sum(axis=1) - df.sum(axis=0)).abs()
    failed = imbalance[imbalance > tol]

    if not failed.empty:
        print('The balance is broken in the following elements:')
        print(failed)
    else:
        print('Balance is done for all elements.')


print(aggregation_mapping_5.keys())
current_path = os.path.abspath(os.path.dirname(__file__))
sam_path = os.path.join(current_path, "data", "databank_2017_type1_KZT.xlsx")
sam = pd.read_excel(sam_path, index_col=0, header=0)
new_sam = aggregate_sam(sam, aggregation_mapping_5)

check_balance(new_sam)
sam_new_path = os.path.join(current_path, "data", "aggregated_sam.xlsx")
new_sam.to_excel(sam_new_path)