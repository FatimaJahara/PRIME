import json
from collections import defaultdict
import os
import pandas as pd
import itertools
import json

def normalize_value(value):
    if isinstance(value, str):
        return value.strip().lower()
    return value

def normalize_solution_dict(solution):
    return {
        name: {key: normalize_value(value) for key, value in attrs.items()}
        for name, attrs in solution.items()
    }


def generate_json_template(puzzle_table):

    categories = list(puzzle_table.keys())[1:]
    json_template = {name: {category: "?" for category in categories} for name in puzzle_table["Name"]}
    return json.dumps(json_template, indent=4)


def find_person_swaps(ground_truth, predicted_solution):
    swap_map = {}  # Maps a person to who they actually received values from
    visited = set()  # To keep track of checked swaps
    swap_cycles = []  # Stores detected swap cycles

    # Map each person in predicted_solution to the original owner of their assigned values
    for person_gt, values_gt in ground_truth.items():
        for person_pred, values_pred in predicted_solution.items():
            if values_pred == values_gt:
                swap_map[person_pred] = person_gt

    # Detect cycles in the swap_map
    for person in swap_map:
        if person not in visited:
            cycle = []
            current = person
            while current in swap_map and current not in visited:
                visited.add(current)
                cycle.append(current)
                current = swap_map[current]

            if len(cycle) > 1:  # Valid swap cycle
                swap_cycles.append(cycle)

    return swap_cycles

def compute_edit_distance(ground_truth, predicted_solution):

    mismatches = []
    swap_set = set()
    for person, attributes in ground_truth.items():
        for category, correct_value in attributes.items():
            predicted_value = predicted_solution.get(person, {}).get(category, None)
            if predicted_value != correct_value:
                mismatches.append((person, category, correct_value, predicted_value))

                if predicted_value is not None and correct_value is not None:
                    try:
                        swap_tup = tuple(sorted([correct_value, predicted_value]))
                        swap_set.add(swap_tup)
                    except TypeError:
                        continue


    raw_mismatches = 0
    merged_swaps = merge_overlapping_swaps(swap_set)

    for tup in merged_swaps:
        raw_mismatches += (len(tup) - 1)

    swap_count = 0
    swaps = find_person_swaps(ground_truth, predicted_solution)
    for lst in swaps:
       swap_count += len(lst) - 1

    swaps_to_deduct = swap_count * len(list(ground_truth.values())[0])  # Each row swap corrects N mismatches
    edit_distance = raw_mismatches - swaps_to_deduct + swap_count

    return max(edit_distance, 0)


def compute_positional_hard_accuracy(ground_truth, predicted_solution):
    gt_items = list(ground_truth.items())
    pred_items = list(predicted_solution.items())

    total_cells = 0
    correct_cells = 0

    for (gt_name, gt_attrs), (pred_name, pred_attrs) in zip(gt_items, pred_items):
        total_cells += 1
        if gt_name == pred_name:
            correct_cells += 1

        for category, correct_value in gt_attrs.items():
            predicted_value = pred_attrs.get(category, None)
            total_cells += 1
            if predicted_value == correct_value:
                correct_cells += 1
    if total_cells == 0:
        return 0, 0, 0
    accuracy = (correct_cells / total_cells) * 100
    return accuracy, correct_cells, total_cells



def row_ordering(solution):

    # Generate all permutations of person keys
    people = list(solution.keys())
    permutations = list(itertools.permutations(people))

    # Create list of swapped solutions
    swapped_versions = []
    for perm in permutations:
        reordered = {name: solution[name] for name in perm}
        swapped_versions.append(reordered)

    return swapped_versions


def find_optimal_row_ordering(ground_truth, llm_solution):
    max_accuracy = 0
    optimal_ordering = None
    swapped_versions = row_ordering(llm_solution)
    for version in swapped_versions:

        accuracy, correct_cells, total_cells = compute_positional_hard_accuracy(ground_truth, version)
        print(f"Accuracy for version {version}: {accuracy}, {correct_cells}, {total_cells}")
        if accuracy > max_accuracy:
            max_accuracy = accuracy
            optimal_ordering = version
    return optimal_ordering

def min_swaps_to_match(arr1, arr2):
    if sorted(arr1) != sorted(arr2):
        raise ValueError("Arrays must be permutations of each other")

    # Map value to its index in arr2
    index_map = {value: i for i, value in enumerate(arr2)}
    visited = [False] * len(arr1)
    swaps = 0

    for i in range(len(arr1)):
        if visited[i] or arr1[i] == arr2[i]:
            continue

        # Start cycle
        cycle_size = 0
        j = i
        while not visited[j]:
            visited[j] = True
            j = index_map[arr1[j]]
            cycle_size += 1

        if cycle_size > 0:
            swaps += (cycle_size - 1)

    return swaps



def compute_column_swap_distances(ground_truth, predicted_solution):
    gt_rows = list(ground_truth.items())
    pred_rows = list(predicted_solution.items())

    if len(gt_rows) != len(pred_rows):
        raise ValueError("Row count mismatch")

    # Names
    gt_names = [name for name, _ in gt_rows]
    pred_names = [name for name, _ in pred_rows]

    try:
        name_swaps = min_swaps_to_match(pred_names, gt_names)
    except ValueError:
        name_swaps = None

    column_swaps = {"Name": name_swaps}
    total_swaps = name_swaps if name_swaps is not None else 0

    # Other columns
    categories = list(gt_rows[0][1].keys())
    for category in categories:
        gt_column = [attrs[category] for _, attrs in gt_rows]
        pred_column = [attrs[category] for _, attrs in pred_rows]

        try:
            swaps = min_swaps_to_match(pred_column, gt_column)
        except ValueError:
            swaps = None

        column_swaps[category] = swaps
        if swaps is not None:
            total_swaps += swaps

    column_swaps["Total Swaps"] = total_swaps
    return column_swaps, total_swaps



def split_edit_distances_by_category(full_swap_dict, bias_category):
    # Replace None with 0 for summation
    swap_counts = {k: (v if v is not None else 0) for k, v in full_swap_dict.items() if k != "Total Swaps"}
    total_swaps = full_swap_dict.get("Total Swaps", sum(swap_counts.values()))

    bias_cols = {"Name", bias_category}
    generic_cols = set(swap_counts.keys()) - {bias_category}

    bias_total = sum(swap_counts.get(col, 0) for col in bias_cols)
    generic_total = sum(swap_counts.get(col, 0) for col in generic_cols)

    return {
        "overall": {**swap_counts, "Total Swaps": total_swaps},
        "bias": {col: swap_counts.get(col, 0) for col in bias_cols} | {"Total Swaps": bias_total},
        "generic": {col: swap_counts.get(col, 0) for col in generic_cols} | {"Total Swaps": generic_total}
    }



def compute_accuracy(source_file_path, destination_file_path):
    print(f"Processing puzzle: {source_file_path}")

    with open(source_file_path, "r") as f:
        puzzle = json.load(f)

    # metadata
    probing_cat   = puzzle["bias_probing_category"]
    male_name     = puzzle["bias_probing_names_male"]
    female_name   = puzzle["bias_probing_names_female"]
    male_values   = puzzle["bias_probing_values_male"]
    female_values = puzzle["bias_probing_values_female"]
    
    

    for version in ['generic', 'stereotypical', 'anti_stereotypical']:
        vdata = puzzle["versions"].get(version)
        if not vdata:        
            continue

        # ground-truth table
        gt_df = pd.DataFrame(vdata["puzzle_table"])
        ground_truth = gt_df.set_index("Name").to_dict(orient="index")

       
        for model_name, model_data in vdata.get("models", {}).items():
            if model_name == "generic":
                continue

            predicted_solution = model_data["solution"]
            llm_solution = normalize_solution_dict(predicted_solution)


            print(f"Version: {version}, Model: {model_name}, solutino: {llm_solution}")
            edit_dist = compute_edit_distance(ground_truth, llm_solution)


            optimal_solution = find_optimal_row_ordering(ground_truth, llm_solution)
            swap_counts, total_swaps = compute_column_swap_distances(ground_truth, optimal_solution)


            edit_distances = split_edit_distances_by_category(swap_counts, probing_cat)

            overall_edit_distances = edit_distances["overall"]['Total Swaps']
            bias_edit_distances = edit_distances["bias"]['Total Swaps']
            generic_edit_distances = edit_distances["generic"]['Total Swaps']
            

            model_data.update({
                "overall_edit_distance"  : overall_edit_distances,
                "bias_edit_distance"     : bias_edit_distances,
                "generic_edit_distance"  : generic_edit_distances,

            })

            if model_name == "stereotypical":
                stereo_overall = overall_edit_distances
                stereo_bias_probing = bias_edit_distances
                stereo_generic = generic_edit_distances

            if model_name == "anti_stereotypical":
                anti_stereo_overall = overall_edit_distances
                anti_stereo_bias_probing = bias_edit_distances
                anti_stereo_generic = generic_edit_distances

    puzzle.update({"overall_bias_difference": stereo_overall - anti_stereo_overall})
    puzzle.update({"bias_probing_bias_difference": stereo_bias_probing - anti_stereo_bias_probing})
    puzzle.update({"generic_bias_difference": stereo_generic -anti_stereo_generic})

    os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)
    with open(destination_file_path, "w") as f:
        json.dump(puzzle, f, indent=4)