def generate_true_false_clues(solution_table):
    clues = set()
    attributes = list(solution_table[0].keys())
    tuples_in_set = []

    for row1 in solution_table:
        for row2 in solution_table:
            for attr1 in attributes:
                for attr2 in attributes:
                    if attr1 != attr2 and row1 != row2:
                        clue_eq = f"({attr1} = {row1[attr1]}) == ({attr2} = {row1[attr2]})"
                        clue_tuple = tuple(sorted([attr1, str(row1[attr1]), str(row1[attr2]), attr2]))
                        if clue_tuple not in tuples_in_set:
                            clues.add(clue_eq)
                            tuples_in_set.append(clue_tuple)

                        clue_neq = f"( {attr1} = {row1[attr1]} ) != ( {attr2} = {row2[attr2]} )"
                        clue_tuple = tuple(sorted([attr1, str(row1[attr1]), attr2, str(row2[attr2])]))

                        if clue_tuple not in tuples_in_set:
                            clues.add(clue_neq)
                            tuples_in_set.append(clue_tuple)

    return clues

def generate_neither_nor_clues(solution_table):
    clues = set()
    attributes = list(solution_table[0].keys())

    for attr1 in attributes:
        values = {row[attr1] for row in solution_table}

        for row in solution_table:
            for value1 in values:
                for value2 in values:
                    if value1 != value2:
                        value1, value2 = sorted([value1, value2])
                        for attr2 in attributes:
                            if attr1 != attr2:
                                valid_clue = False
                                if row[attr2] not in {row2[attr2] for row2 in solution_table if row2[attr1] == value1 or row2[attr1] == value2}:
                                    valid_clue = True
                                if valid_clue:
                                    clue = (f"(!( {attr1} = {value1} ) and !( {attr1} = {value2} )) = "
                                            f"( {attr2} = {row[attr2]} )")
                                    clues.add(clue)
    return clues

def generate_either_or_clues(solution_table): # Test
    clues = set()
    attributes = list(solution_table[0].keys())
    tuples_in_set = []

    for row1 in solution_table:
      for row2 in solution_table:
            for attr1 in attributes:
                for attr2 in attributes:
                    for attr3 in attributes:
                        if row1 != row2 and attr1 != attr3 and attr2 != attr3:

                            clue = (
                                f"((( {attr1} = {row1[attr1]} ) or ( {attr2} = {row2[attr2]} )) and "
                                f"!(( {attr1} = {row1[attr1]} ) and ( {attr2} = {row2[attr2]} ))) = "
                                f"( {attr3} = {row1[attr3]} )"
                            )
                            clue_tuple = tuple(sorted([attr1, str(row1[attr1]), attr2, str(row2[attr2]), attr3, str(row1[attr3])]))
                            if clue_tuple not in tuples_in_set:
                                clues.add(clue)
                                tuples_in_set.append(clue_tuple)

                            clue = (
                                f"((( {attr1} = {row1[attr1]} ) or ( {attr2} = {row2[attr2]} )) and "
                                f"!(( {attr1} = {row1[attr1]} ) and ( {attr2} = {row2[attr2]} ))) = "
                                f"( {attr3} = {row2[attr3]} )"
                            )

                            clue_tuple = tuple(sorted([attr1, str(row1[attr1]), attr2, str(row2[attr2]), attr3, str(row2[attr3])]))
                            if clue_tuple not in tuples_in_set:
                                clues.add(clue)
                                tuples_in_set.append(clue_tuple)

    return clues


def generate_unaligned_pair_clues(solution_table):
    clues = set()  # Use a set to avoid duplicate clues
    attributes = list(solution_table[0].keys())  # Get the attribute names from the first row
    tuples_in_set = []

    # Loop through each pair of rows
    for row1 in solution_table:
        for row2 in solution_table:
                for attr1 in attributes:
                    for attr2 in attributes:
                        for attr3 in attributes:
                            if attr1 != attr2 and attr1 != attr3 and attr2 != attr3 and row1 != row2:

                                condition1 = f"!(( {attr1} = {row1[attr1]} ) = ( {attr2} = {row2[attr2]} ))"

                                aligned_condition1 = f"(( {attr1} = {row1[attr1]} ) = ( {attr3} = {row1[attr3]} )) or (( {attr1} = {row1[attr1]} ) = ( {attr3} = {row2[attr3]} ))"
                                aligned_condition2 = f"(( {attr2} = {row2[attr2]} ) = ( {attr3} = {row1[attr3]} )) or (( {attr2} = {row2[attr2]} ) = ( {attr3} = {row2[attr3]} ))"

                                clue = f"{condition1} and ({aligned_condition1}) and ({aligned_condition2}) "


                                clue_tuple = tuple(sorted([attr1, str(row1[attr1]), attr2, str(row2[attr2]), attr3, str(row1[attr3]), str(row2[attr3])]))
                                if clue_tuple not in tuples_in_set:
                                    clues.add(clue)
                                    tuples_in_set.append(clue_tuple)

    return clues


def generate_multi_elimination_clues(solution_table):

    clues = set()
    attributes = list(solution_table[0].keys())
    tuples_in_set = []

    for row1 in solution_table:
        for row2 in solution_table:
            for row3 in solution_table:
                for attr1 in attributes:
                    for attr2 in attributes:
                        for attr3 in attributes:
                            if attr1 != attr2 and attr1 != attr3 and attr2 != attr3 and row1 != row2 and row1 != row3 and row2 != row3:

                                condition1 = f"!(( {attr1} = {row1[attr1]} ) = ( {attr2} = {row2[attr2]} ))"

                                aligned_condition1 = f"!(( {attr1} = {row1[attr1]} ) = ( {attr3} = {row3[attr3]} ))"
                                aligned_condition2 = f"!(( {attr2} = {row2[attr2]} ) = ( {attr3} = {row3[attr3]} ))"

                                clue = f"{condition1} and {aligned_condition1}  and {aligned_condition2} "


                                clue_tuple = tuple(sorted([attr1, str(row1[attr1]), attr2, str(row2[attr2]), attr3, str(row3[attr3])]))
                                if clue_tuple not in tuples_in_set:
                                    clues.add(clue)
                                    tuples_in_set.append(clue_tuple)

    return clues