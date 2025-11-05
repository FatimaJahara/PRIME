import argparse
import pandas as pd
from puzzle.table_generator import generate_solution_table_gender_bias_probing
from clues.clue_generator import generate_clues
from clues.clue_converter import clue_converter
from clues.standard_clue_conversion import convert_clues_to_standard_form
from solver.solver import clue_finder
from puzzle.create import create_puzzle
import random


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, required=True)
    parser.add_argument("--cols", type=int, required=True)
    parser.add_argument("--out", type=str, default="output/")
    parser.add_argument("--puzzle_id", type=int, default=1)
    args = parser.parse_args()

    generic_df = pd.read_csv("data for puzzle generation/generic.csv")
    names_df = pd.read_csv("data for puzzle generation/names_gender_probing.csv")
    gender_df = pd.read_csv("data for puzzle generation/gender probing.csv", header=[0, 1])

    generic_df.drop('Unnamed: 0', axis=1, inplace=True)
    gender_df.drop('Unnamed: 0_level_0', axis=1, inplace=True)
    gender_probing_columns = set(cols[0] for cols in gender_df.columns)
    gender_probing_columns = list(gender_probing_columns)
    # gender_probing_columns.sort()

    c = args.puzzle_id
    no_of_rows = args.rows
    no_of_cols = args.cols
    col_name = random.choice(gender_probing_columns)

    for row in [no_of_rows]:
        for col in [no_of_cols]:

            gender_df_sub = gender_df[col_name]
            gender_column_name = col_name

            # Generate tables and clues
            generic_table, stereo_table, anti_stereo_table, bias_cat, m_names, f_names, m_vals, f_vals = generate_solution_table_gender_bias_probing(
                row, col, generic_df, names_df, gender_df_sub, gender_column_name)
            
            print(f"Generic Puzzle (G):")
            print(pd.DataFrame(generic_table).to_string(index=False))
            print()
            print(f"Stereotypical Puzzle (S):")
            print(pd.DataFrame(stereo_table).to_string(index=False))
            print()
            print(f"Anti-stereotypical Puzzle (AS):")
            print(pd.DataFrame(anti_stereo_table).to_string(index=False))
            print()
            
            all_generic_clues = generate_clues(generic_table, row)
            solved, solved_clues, constraints = clue_finder(generic_table, all_generic_clues)
            
            stereo_clues, anti_stereo_clues = clue_converter(
                generic_table,
                stereo_table,
                anti_stereo_table,
                solved_clues,
                gender_column_name
            )

            bias_list = [m_names, f_names, m_vals, f_vals]

            formatted_all_clues = [convert_clues_to_standard_form(clue) for clue in all_generic_clues]
            formatted_generic_clues = [convert_clues_to_standard_form(clue) for clue in solved_clues]
            formatted_stereo_clues = [convert_clues_to_standard_form(clue) for clue in stereo_clues]
            formatted_anti_stereo_clues = [convert_clues_to_standard_form(clue) for clue in anti_stereo_clues]

            print("Generic Clues:")
            for i, clue in enumerate(formatted_generic_clues):
                print(f"Clue {i+1}: {clue}")
            print()

            print("Stereotypical Clues:")
            for i, clue in enumerate(formatted_stereo_clues):
                print(f"Clue {i+1}: {clue}")
            print()

            print("Anti-stereotypical Clues:")
            for i, clue in enumerate(formatted_anti_stereo_clues):
                print(f"Clue {i+1}: {clue}")
            print()


            create_puzzle(
                c, "gender_probing", row, col, args.out,
                generic_table, stereo_table, anti_stereo_table,
                formatted_all_clues, solved, formatted_generic_clues, formatted_stereo_clues, formatted_anti_stereo_clues, constraints,
                gender_column_name, bias_list
            )
            c += 1
            


if __name__ == "__main__":
    main()