import re

def process_true_false_clues(clue):

    cleaned_clue = re.sub(r"\s+", " ", clue).strip()
    # print("Cleaned Clue:", cleaned_clue)
    allowed_chars = r"[\wÀ-ÖØ-öø-ÿ\s_\-–—'ʻ’\"\/\\&,:#(){}\[\]=!<>?+*/%^.\d]+"

    pattern = rf"\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\s*(==|!=)\s*\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)"
    match = re.search(pattern, cleaned_clue)


    if match:
        constraint = None
        var1, val1, operator, var2, val2 = match.groups()

        def is_int(value):
                try:
                    int(value)
                    return True
                except ValueError:
                    return False

        values = [val1.strip(), val2.strip()]

        formatted_values = []
        for value in values:
            if is_int(value):
                # formatted_values.append(value)
                formatted_values.append(f'"{str(value)}"')
            else:
                formatted_values.append(f'"{value}"')

        a, b = var1.strip(), var2.strip()
        a = a.replace(" ", "_") if " " in a else a
        b = b.replace(" ", "_") if " " in b else b
        a_val, b_val = formatted_values[0], formatted_values[1]

        if a == "Name":
            if operator == "==":
                constraint = f'problem.addConstraint(InSetConstraint([{a_val}]), [{b_val}])'
            elif operator == "!=":
                constraint = f'problem.addConstraint(NotInSetConstraint([{a_val}]), [{b_val}])'
        elif b == "Name":
            if operator == "==":
                constraint = f'problem.addConstraint(InSetConstraint([{b_val}]), [{a_val}])'
            elif operator == "!=":
                constraint = f'problem.addConstraint(NotInSetConstraint([{b_val}]), [{a_val}])'
        else:
            if operator == "==":
                constraint = f'problem.addConstraint(lambda {a}, {b}: {a} == {b}, ({a_val}, {b_val}))'
            elif operator == "!=":
                constraint = f'problem.addConstraint(lambda {a}, {b}: {a} != {b}, ({a_val}, {b_val}))'

    return constraint