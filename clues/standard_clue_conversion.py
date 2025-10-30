import re

def convert_clues_to_standard_form(clue: str) -> str:


    # Either-Or
    clue = re.sub(
        r'(\(\(\(\s*[^()]+\s*\)\s*or\s*\(\s*[^()]+\s*\)\)\s*and\s*!\(\(\s*[^()]+\s*\)\s*and\s*\(\s*[^()]+\s*\)\)\))\s*=\s*\(\s*([^()]+?)\s*\)',
        r'\1 <=> (\2)',
        clue
    )

    # Neither-Nor
    clue = re.sub(
        r'(\(!\([^()]+\)\s*and\s*!\([^()]+\)\))\s*=\s*\(\s*([^()]+?)\s*\)',
        r'\1 <=> (\2)',
        clue
    )

    # True/False ( != and == )
    clue = re.sub(
        r'\(\s*([^()]+?)\s*\)\s*!=\s*\(\s*([^()]+?)\s*\)',
        r'!((\1) <=> (\2))',
        clue
    )

    clue = re.sub(
        r'\(\s*([^()]+?)\s*\)\s*==\s*\(\s*([^()]+?)\s*\)',
        r'(\1) <=> (\2)',
        clue
    )

    # Unaligned pair
    clue = re.sub(
        r'(?<![=!<>])\(\s*([^()]+?)\s*\)\s*=\s*\(\s*([^()]+?)\s*\)',
        r'(\1) <=> (\2)',
        clue
    )

    # Multi-Elimination and Unaligned-Pair
    clue = re.sub(
        r'!\(\(\s*([^()]+?)\s*\)\s*=\s*\(\s*([^()]+?)\s*\)\)',
        r'!((\1) <=> (\2))',
        clue
    )

    return clue