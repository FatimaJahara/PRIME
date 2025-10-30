import re

def process_multi_elimination_clues(clue):
    cleaned_clue = re.sub(r"\s+", " ", clue).strip()
    # print(cleaned_clue)
    constraint = None

    allowed_chars = r"[\wÀ-ÖØ-öø-ÿ\s_\-–—'ʻ’\"\/\\&,:#(){}\[\]=!<>?+*/%^.\d]+"

    pattern = rf"""
        !\(\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\s*=\s*\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\)\s*and\s*
        !\(\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\s*=\s*\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\)\s*and\s*
        !\(\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\s*=\s*\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\)
    """

    match = re.match(pattern, cleaned_clue, re.VERBOSE)
    # print(match)
    if match:
        groups = match.groups()

        var1, val1, var2, val2 = groups[0:4]
        var3, val3, var4, val4 = groups[4:8]
        var5, val5, var6, val6 = groups[8:12]

        def is_int(value):
            try:
                int(value)
                return True
            except ValueError:
                return False

        values = [val1.strip(), val2.strip(), val4.strip()]

        formatted_values = []
        for value in values:
            if is_int(value):
                formatted_values.append(f'"{str(value)}"')
            else:
                formatted_values.append(f'"{value}"')

        a, b, c = var1.strip(), var2.strip(), var4.strip()
        a = a.replace(" ", "_") if " " in a else a
        b = b.replace(" ", "_") if " " in b else b
        c = c.replace(" ", "_") if " " in c else c

        a_val, b_val, c_val = formatted_values[0], formatted_values[1], formatted_values[2]

        if a == "Name":
            constraint = (f'problem.addConstraint(lambda {b}, {c}: ({b} != {a_val}) and ({c} != {a_val}) and ({b} != {c}), ({b_val}, {c_val}))')

        elif b == "Name":
            constraint = (f'problem.addConstraint(lambda {a}, {c}: ({a} != {b_val}) and ({a} != {c}) and ({c} != {b_val}), ({a_val}, {c_val}))')

        elif c == "Name":
            constraint = (f'problem.addConstraint(lambda {a}, {b}: ({a} != {b}) and ({a} != {c_val}) and ({b} != {c_val}), ({a_val}, {b_val}))')

        else:
            constraint = (f'problem.addConstraint(lambda {a}, {b}, {c}: ({a} != {b}) and ({a} != {c}) and ({b} != {c}), ({a_val}, {b_val}, {c_val}))')

    return constraint