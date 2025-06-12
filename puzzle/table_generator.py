import random
import numpy as np
import pandas as pd
from utils.normalization import normalize_text, normalize_list, convert_numeric_to_str

def generate_solution_table_gender_bias_probing(row, cols, generic_df, names_df, gender_df, gender_column_name):
    random_cols = np.random.choice(generic_df.columns, cols-1, replace=False)
    generic_bias_probing = []
    available_values = {col: list(generic_df[col].dropna().apply(normalize_text)) for col in random_cols[:-1]}

    for _ in range(row):
        row_values = []
        for col in random_cols[:-1]:
            value = random.choice(available_values[col])
            available_values[col].remove(value)
            row_values.append(value)
        generic_bias_probing.append(row_values)

    selected_names_Male = normalize_list(random.sample(list(names_df['Male'].dropna()), row//2))
    selected_names_Female = normalize_list(random.sample(list(names_df['Female'].dropna()), row//2))
    generic_names = [f"Person {chr(65 + i)}" for i in range(row)]

    selected_gender_Male = normalize_list(random.sample(list(gender_df['Man'].dropna()), row//2))
    selected_gender_Female = normalize_list(random.sample(list(gender_df['Woman'].dropna()), row//2))

    df = pd.DataFrame(columns=['Name', gender_column_name] + list(random_cols[:-1]))
    df['Name'] = selected_names_Male + selected_names_Female
    df[gender_column_name] = selected_gender_Male + selected_gender_Female
    generic_df_subset = pd.DataFrame(generic_bias_probing, columns=random_cols[:-1])
    for col in random_cols[:-1]:
        df[col] = generic_df_subset[col].apply(normalize_text)

    anti_df = pd.DataFrame(columns=['Name', gender_column_name] + list(random_cols[:-1]))
    anti_df['Name'] = selected_names_Male + selected_names_Female
    anti_df[gender_column_name] = selected_gender_Female + selected_gender_Male
    for col in random_cols[:-1]:
        anti_df[col] = generic_df_subset[col].apply(normalize_text)

    gen_df = pd.DataFrame(columns=['Name', gender_column_name] + list(random_cols[:-1]))
    gen_df['Name'] = generic_names
    bias_probing_category = selected_gender_Female + selected_gender_Male
    random.shuffle(bias_probing_category)
    gen_df[gender_column_name] = bias_probing_category
    for col in random_cols[:-1]:
        gen_df[col] = generic_df_subset[col].apply(normalize_text)

    return (convert_numeric_to_str(gen_df.to_dict('list')),
            convert_numeric_to_str(df.to_dict('list')),
            convert_numeric_to_str(anti_df.to_dict('list')),
            gender_column_name,
            selected_names_Male, selected_names_Female,
            selected_gender_Male, selected_gender_Female)