import argparse
import pandas as pd
from puzzle.table_generator import generate_solution_table_gender_bias_probing
from clues.clue_generator import generate_clues
from clues.clue_converter import clue_converter
from clues.standard_clue_conversion import convert_clues_to_standard_form
from solver.solver import clue_finder
from puzzle.create import create_puzzle
import random
import sys

def generate_single_puzzle(c, row, col, gender_df, gender_probing_columns, generic_df, names_df, out_dir):
    col_name = random.choice(gender_probing_columns)

    for row in [row]:
        for col in [col]:

            gender_df_sub = gender_df[col_name]
            gender_column_name = col_name

            print(f"\n--- Puzzle {c} ---")
            print(f"Bias Probing Category: {gender_column_name}")

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
                c, "gender_probing", row, col, out_dir,
                generic_table, stereo_table, anti_stereo_table,
                formatted_all_clues, solved, formatted_generic_clues, formatted_stereo_clues, formatted_anti_stereo_clues, constraints,
                gender_column_name, bias_list
            )
            c += 1
    

def main():
    parser = argparse.ArgumentParser(description="Generate PRIME logic puzzles.")
    parser.add_argument("--rows", type=int, required=True, help="Number of rows in the puzzle grid.")
    parser.add_argument("--cols", type=int, required=True, help="Number of columns in the puzzle grid.")
    parser.add_argument("--out", type=str, default="output/", help="Output directory to save puzzles.")
    parser.add_argument("--start_id", type=int, default=1, help="Starting puzzle ID.")
    parser.add_argument("--batch", type=int, default=1, help="Number of puzzles to generate (default: 1).")
    args = parser.parse_args()

    if args.rows % 2 != 0:
        print(f"Error: Number of rows must be even. You entered {args.rows}.")
        sys.exit(1)

    generic_df = pd.read_csv("data/categories and items/generic.csv")
    names_df = pd.read_csv("data/categories and items/names_gender_probing.csv")
    gender_df = pd.read_csv("data/categories and items/gender probing.csv", header=[0, 1])

    generic_df.drop('Unnamed: 0', axis=1, inplace=True)
    gender_df.drop('Unnamed: 0_level_0', axis=1, inplace=True)
    gender_probing_columns = set(cols[0] for cols in gender_df.columns)
    gender_probing_columns = list(gender_probing_columns)
    # gender_probing_columns.sort()


    # Single or batch mode
    if args.batch == 1:
        generate_single_puzzle(args.start_id, args.rows, args.cols, gender_df, gender_probing_columns, generic_df, names_df, args.out)
    else:
        for i in range(args.batch):
            print(f"\nGenerating puzzle {args.start_id + i}/{args.start_id + args.batch - 1}")
            generate_single_puzzle(args.start_id + i, args.rows, args.cols, gender_df, gender_probing_columns, generic_df, names_df, args.out)
            


if __name__ == "__main__":
    main()
