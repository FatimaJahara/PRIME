import re

def process_neither_nor_clues(clue):
    # print(clue)
    cleaned_clue = re.sub(r"\s+", " ", clue).strip()
    allowed_chars = r"[\wÀ-ÖØ-öø-ÿ\s_\-–—'ʻ’\"\/\\&,:#(){}\[\]=!<>?+*/%^.\d]+"

    pattern = rf"\(\!\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\s+and\s+\!\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\)\s*(=|!=)\s*\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)"

    match = re.search(pattern, cleaned_clue)
    match = re.match(pattern, clue)
    # print(match)
    if match:
        var1, val1, var2, val2, operator, var3, val3 = match.groups()

        def is_int(value):
            try:
                int(value)
                return True
            except ValueError:
                return False

        values = [val1.strip(), val2.strip(), val3.strip()]

        formatted_values = []
        for value in values:
            if is_int(value):
                formatted_values.append(f'"{str(value)}"')
            else:
                formatted_values.append(f'"{value}"')

        a, b, c = var1.strip(), var2.strip(), var3.strip()
        a = a.replace(" ", "_") if " " in a else a
        b = b.replace(" ", "_") if " " in b else b
        c = c.replace(" ", "_") if " " in c else c

        a_val, b_val, c_val = formatted_values[0], formatted_values[1], formatted_values[2]

        if a == "Name" and b == "Name":
            constraint = f'problem.addConstraint(lambda {c}: ({c} != {a_val}) and ({c} != {a_val}), ({c_val},))'

        elif a == "Name" and b != "Name":
            constraint = f'problem.addConstraint(lambda {b}, {c}: ({b} != {a_val}) and ({b} != {c}) and ({c} != {a_val}), ({b_val}, {c_val}))'

        elif a != "Name" and b == "Name":
            constraint = f'problem.addConstraint(lambda {a}, {c}: ({a} != {b_val}) and ({c} != {b_val}) and ({a} != {c}), ({a_val}, {c_val}))'

        elif c == "Name":
            if a == b:
                a, b = a+"_1", b+"_2"
            constraint = f'problem.addConstraint(lambda {a}, {b}: ({a} != {b}) and ({b} != {c_val}) and ({a} != {c_val}), ({a_val}, {b_val}))'

        else:
            if a == b:
                a, b = a+"_1", b+"_2"
            constraint = f'problem.addConstraint(lambda {a}, {b}, {c}: ({a} != {b}) and ({b} != {c}) and ({a} != {c}), ({a_val}, {b_val}, {c_val}))'


    return constraint