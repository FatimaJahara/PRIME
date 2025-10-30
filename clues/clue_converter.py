import re
import os
import json
import random

import re

def extract_bias_mappings_inline(generic, stereo, anti, bias_category, stable_category):
    bias_mappings = {}
    name_mappings = {}

    g_lookup = {stable: bias for stable, bias in zip(generic[stable_category], generic[bias_category])}
    s_lookup = {stable: bias for stable, bias in zip(stereo[stable_category], stereo[bias_category])}
    a_lookup = {stable: bias for stable, bias in zip(anti[stable_category], anti[bias_category])}
    g_names = {stable: name for stable, name in zip(generic[stable_category], generic["Name"])}
    s_names = {stable: name for stable, name in zip(stereo[stable_category], stereo["Name"])}
    a_names = {stable: name for stable, name in zip(anti[stable_category], anti["Name"])}

    for val in generic[stable_category]:
        if val in s_lookup and val in a_lookup:
            bias_mappings[g_lookup[val]] = (g_lookup[val], s_lookup[val], a_lookup[val])
            name_mappings[g_names[val]] = (s_names[val], a_names[val])

    return bias_mappings, name_mappings

def apply_bias_value_substitution_inline(clue, mapping_dict, category):
    placeholder_map = {}
    placeholder_clue = clue

    for i, generic_val in enumerate(mapping_dict.keys()):
        placeholder = f"__GENERIC_PLACEHOLDER_{i}__"
        placeholder_map[placeholder] = mapping_dict[generic_val]
        pattern = rf"\(\s*{re.escape(category)}\s*=\s*{re.escape(generic_val)}\s*\)"
        replacement = f"({category} = {placeholder})"
        placeholder_clue = re.sub(pattern, replacement, placeholder_clue)

    for placeholder, final_val in placeholder_map.items():
        placeholder_clue = placeholder_clue.replace(placeholder, final_val)

    return placeholder_clue

def clue_converter(generic_table, stereo_table, anti_table, generic_clues, bias_category):
    # Automatically determine the stable category
    stable_columns = set(generic_table.keys()) & set(stereo_table.keys()) & set(anti_table.keys())
    stable_columns -= {"Name", bias_category}
    stable_category = next(iter(stable_columns))

    bias_mappings, name_mappings = extract_bias_mappings_inline(
        generic_table, stereo_table, anti_table, bias_category, stable_category
    )

    stereo_clues = []
    anti_stereo_clues = []

    for clue in generic_clues:
        s_clue, a_clue = clue, clue

        for g_name, (s_name, a_name) in name_mappings.items():
            s_clue = re.sub(rf"\b{re.escape(g_name)}\b", s_name, s_clue)
            a_clue = re.sub(rf"\b{re.escape(g_name)}\b", a_name, a_clue)

        if bias_category in clue:
            gen_to_s = {gen: s for gen, s, _ in bias_mappings.values()}
            gen_to_a = {gen: a for gen, _, a in bias_mappings.values()}
            s_clue = apply_bias_value_substitution_inline(s_clue, gen_to_s, bias_category)
            a_clue = apply_bias_value_substitution_inline(a_clue, gen_to_a, bias_category)

        stereo_clues.append(s_clue)
        anti_stereo_clues.append(a_clue)

    return stereo_clues, anti_stereo_clues
