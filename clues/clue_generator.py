from .clue_types import (
    generate_true_false_clues, generate_neither_nor_clues, generate_either_or_clues,
    generate_unaligned_pair_clues, generate_multi_elimination_clues
)

def convert_column_dict_to_row_list(column_dict):
    keys = list(column_dict.keys())
    num_rows = len(column_dict[keys[0]])

    row_list = []
    for i in range(num_rows):
        row = {key: column_dict[key][i] for key in keys}
        row_list.append(row)

    return row_list


def generate_clues(solution_table, row):
    solution = convert_column_dict_to_row_list(solution_table)
    if row <= 2:
        true_false_clues = generate_true_false_clues(solution)
        either_or_clues = generate_either_or_clues(solution)
        unaligned_pair_clues = generate_unaligned_pair_clues(solution)
        all_clues = (
            list(true_false_clues) + list(either_or_clues) + list(unaligned_pair_clues)
        )

    else:
        true_false_clues = generate_true_false_clues(solution)
        neither_nor_clues = generate_neither_nor_clues(solution)
        either_or_clues = generate_either_or_clues(solution)
        unaligned_pair_clues = generate_unaligned_pair_clues(solution)
        multi_elimination_clues = generate_multi_elimination_clues(solution)

        all_clues = (
            list(true_false_clues) + list(neither_nor_clues) + list(either_or_clues) + list(unaligned_pair_clues) + list(multi_elimination_clues)
        )

    return all_clues