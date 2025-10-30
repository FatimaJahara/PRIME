from .true_false import process_true_false_clues
from .neither_nor import process_neither_nor_clues
from .either_or import process_either_or_clues
from .unaligned_pair import process_unaligned_pair_clues
from .multi_elimination import process_multi_elimination_clues

from constraint import *
import re

def solution_match(dict1, dict2):
    # Check for solution match
    return dict1 == dict2

def find_numeric_keys(data):
    # Check for numeric features
    numeric_keys = {}

    for key, values in data.items():
        if any(isinstance(value, (int, float)) for value in values):
            numeric_keys[key] = values

    return numeric_keys

def detect_clue_type(clue):
    # Detect the type of clue passed

    allowed_chars = r"[\wÀ-ÖØ-öø-ÿ\s_\-–—'ʻ’\"\/\\&,:#(){}\[\]=!<>?+*/%^.\d]+"
    patterns = {
        "True-False": rf"\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*[!=]=\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)",
        "Neither-Nor": rf"\(!\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*and\s*!\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\)\s*=\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)",
        "Either-Or": rf"\(\(\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*or\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\)\s*and\s*!\(\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*and\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\)\)\s*=\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)",
        "Unaligned-Pair": rf"!.*?\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*and\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*and\s*\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)",
        "Multi-Elimination": rf"!.*?\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*and\s*!.*?\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)\s*and\s*!.*?\(\s*{allowed_chars}\s*=\s*{allowed_chars}\s*\)"
    }

    for clue_type, pattern in patterns.items():
        if re.fullmatch(pattern, clue.replace(" ", "")):
            return clue_type

    return "Unknown"

def compare_step_solutions(step_solutions, expected_solution):
    transformed_expected = {}

    categories = [key for key in expected_solution if key != "Name"]

    for i, name in enumerate(expected_solution["Name"]):
        for category in categories:
            key = expected_solution[category][i].strip()
            transformed_expected[key] = name.strip()

    matched = False

    for step, solution in enumerate(step_solutions):
        normalized_solution = {str(k).strip(): str(v).strip() for k, v in solution.items()}
        normalized_expected = {str(k).strip(): str(v).strip() for k, v in transformed_expected.items()}

        if normalized_solution == normalized_expected:
            # print(f"Match found at step {step}")
            matched = True
            break

    return matched

def solver(solution, clues, constraints = None, prior = False):
    problem = Problem()
    column_lists = [value for key, value in solution.items() if key != "Name"]
    criteria = []
    # print(column_lists)

    for r in column_lists:
      criteria += r
      # print(r)
    # print(criteria)

    problem.addVariables(criteria, solution["Name"])

    for r in column_lists:
      problem.addConstraint(AllDifferentConstraint(), r)

    # print("Available Variables in Problem:", problem._variables.keys())

    if not prior:
        constraints = []
        for clue in clues:
            clue_type = detect_clue_type(clue)
            # print(clue_type)
            if clue_type == "True-False":
                constraints.append(process_true_false_clues(clue))
            elif clue_type == "Neither-Nor":
                constraints.append(process_neither_nor_clues(clue))
            elif clue_type == "Either-Or":
                constraints.append(process_either_or_clues(clue))
            elif clue_type == "Unaligned-Pair":
                constraints.append(process_unaligned_pair_clues(clue))
            elif clue_type == "Multi-Elimination":
                constraints.append(process_multi_elimination_clues(clue))
            else:
                print(f"Unknown clue: {clue}")

    i = 1
    required_constraints = []
    required_clues = []
    # print(f"Clues in solver: {clues}")
    for constraint, clue in zip(constraints, clues):
        # print(f"Clue: {clue}")
        # print(f"Step {i}: {constraint}")
        # print(constraint)
        if isinstance(constraint, str):
            eval(constraint)
        # else:
        #     print(f"Skipping invalid constraint: {constraint}")

        gen_solutions = problem.getSolutions()

        required_constraints.append(constraint)
        required_clues.append(clue)

        if compare_step_solutions(gen_solutions, solution):
            if len(gen_solutions) == 1:
                # required_constraints.append(constraint)
                # required_clues.append(clue)
                break
        i += 1

    generated_solutions = problem.getSolutions()

    if compare_step_solutions(generated_solutions, solution) and len(gen_solutions) == 1:
        # print(f"Clue set found of lenth {len(required_clues)}!")
        return True, required_clues, required_constraints

    return False, required_clues, required_constraints

import random



def clue_finder(solution, all_clues, n = 10):
    if n > len(all_clues):
        n = len(all_clues)

    clue_subset = random.sample(all_clues, n)
    # print(f"First {n} clues: {clue_subset}")
    solved, clues_vn, constraints_vn = solver(solution, clue_subset)
    # print(f"Solved: {solved}")
    # print(f"Subset of length {len(clues_vn)}: {clues_vn}\n")

    pos = 1
    # print(f"Subset of length {len(clues_vn)}: {clues_vn}\n")
    if solved:
        while pos <= len(clues_vn):
            # print(pos, clues_vn)
            # print(f"Before: {clues_vn}")
            removed_clue, removed_constraint = clues_vn.pop(-pos), constraints_vn.pop(-pos)
            clues_vn_2 = clues_vn
            constraints_vn_2 = constraints_vn
            # print(f"After: {clues_vn_2}")
            solved_inner, clues_vn, constraints_vn = solver(solution, clues_vn_2, constraints_vn_2, True)
            # print(f"After solver: {clues_vn}")
            # print(f"Removed {removed_clue} from position {len(clues_vn) - pos} \n")

            if not solved_inner:
                clues_vn.append(removed_clue)
                # solved = True
                constraints_vn.append(removed_constraint)
                # print(f"Added {removed_clue} back to position {pos} \n")

            pos += 1
            # print(f"Solved: {solved}")
            # print(f"Subset of length {len(clues_vn)}: {clues_vn}\n")

        # print(f"Clue set found of lenth {len(clues_vn)}!")
        return True, clues_vn, constraints_vn


    else:
        # print("Trying new batch")
        n = min(len(all_clues), n + 10)
        return clue_finder(solution, all_clues, n)

    return False, [], []