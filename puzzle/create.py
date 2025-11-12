import os
import json
import pandas as pd

def update_csv_index(puzzle_id, probing_type, size, file_path, dir):
    new_entry = pd.DataFrame([{
        "Puzzle_ID": puzzle_id,
        "Probing_Type": probing_type,
        "Size": size,
        "File_Path": file_path
    }])


def create_puzzle(puzzle_id, probing_type, rows, columns, dir,
                  generic_table, stereo_table, anti_stereo_table,
                  all_clues, solved, solved_clues, stereo_clues, anti_stereo_clues, solved_constraints,
                  bias_cat, bias_list):
    file_suffix = "g" if probing_type == "gender_probing" else "n"
    # file_path = os.path.join(dir, f"puzzle.json")
    file_path = f"{dir}/puzzle_{puzzle_id:04}{file_suffix}.json"

    puzzle_data = {
        "id": puzzle_id,
        "probing_type": probing_type,
        "rows": rows,
        "columns": columns,
        "bias_probing_category": bias_cat,
        "bias_probing_names_male": bias_list[0],
        "bias_probing_names_female": bias_list[1],
        "bias_probing_values_male": bias_list[2],
        "bias_probing_values_female": bias_list[3],
        "versions": {
            "generic": {
                "solved": solved,
                "puzzle_table": generic_table,
                "clues": {
                    "all_clues": list(all_clues),
                    "solution_clues": list(solved_clues),
                    "solved_constraints": list(solved_constraints),
                    "solution_clues_nl": []
                }
            },
            "stereotypical": {
                "solved": False,
                "puzzle_table": stereo_table,
                "clues": {
                    "all_clues": [], "solution_clues": list(stereo_clues), "solved_constraints": [], "solution_clues_nl": []
                }
            },
            "anti_stereotypical": {
                "solved": False,
                "puzzle_table": anti_stereo_table,
                "clues": {
                    "all_clues": [], "solution_clues": list(anti_stereo_clues), "solved_constraints": [], "solution_clues_nl": []
                }
            }
        }
    }

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(puzzle_data, f, indent=4)
    # print(f"Puzzle {puzzle_id} created at {file_path}.")
    print(f"Puzzle created at {file_path}.")

    update_csv_index(puzzle_id, probing_type, (rows, columns), file_path, dir)
