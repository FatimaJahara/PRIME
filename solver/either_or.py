import re

def process_either_or_clues(clue):
    constraint = None

    cleaned_clue = re.sub(r"\s+", " ", clue).strip()

    # match = re.match(r"\(\(\( (\w+) = (\w+) \) or \( (\w+) = (\w+) \)\) and !\(\( (\w+) = (\w+) \) and \( (\w+) = (\w+) \)\)\) = \( (\w+) = (\w+) \)", cleaned_clue)


    # match = re.match(r"\(\(\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\s*\)\s*or\s*\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\s*\)\)\s*and\s*!\(\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\s*\)\s*and\s*\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\s*\)\)\)\s*=\s*\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\s*\)", cleaned_clue)
    allowed_chars = r"[\wÀ-ÖØ-öø-ÿ\s_\-–—'ʻ’\"\/\\&,:#(){}\[\]=!<>?+*/%^.\d]+"

    pattern = rf"\(\(\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\s*or\s*\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\)\s*and\s*!\(\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\s*and\s*\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\)\)\s*=\s*\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)"
    match = re.match(pattern, cleaned_clue)
    print(match)

    if match:
        # constraint = None
        var1, val1, var2, val2, var3, val3, var4, val4, target_var, target_val = match.groups()

        def is_int(value):
            try:
                int(value)
                return True
            except ValueError:
                return False

        values = [val1.strip(), val2.strip(), target_val.strip()]

        formatted_values = []
        for value in values:
            if is_int(value):
                # formatted_values.append(value)
                formatted_values.append(f'"{str(value)}"')
            else:
                formatted_values.append(f'"{value}"')

        a, b, c = var1.strip(), var2.strip(), target_var.strip()
        a = a.replace(" ", "_") if " " in a else a
        b = b.replace(" ", "_") if " " in b else b
        c = c.replace(" ", "_") if " " in c else c

        a_val, b_val, c_val = formatted_values[0], formatted_values[1], formatted_values[2]

        if a == "Name" and b == "Name":
            constraint = f'problem.addConstraint(lambda {c}: ({c} == {a_val}) or ({c} == {b_val}), ({c_val},))'

        elif a == "Name" and b != "Name":
            constraint = f'problem.addConstraint(lambda {b}, {c}: ({b} != {a_val}) and ({c} == {a_val}) or ({c} == {a_val}), ({b_val}, {c_val}))'

        elif a != "Name" and b == "Name":
            constraint = f'problem.addConstraint(lambda {a}, {c}: ({a} != {b_val}) and ({a} == {c}) or ({c} == {b_val}), ({a_val}, {c_val}))'

        elif c == "Name":
            if a == b:
                a, b = a+"_1", b+"_2"
                constraint = f'problem.addConstraint(lambda {a}, {b}: ({a} == {c_val}) or ({b} == {c_val}), ({a_val}, {b_val}))'
            else:
                constraint = f'problem.addConstraint(lambda {a}, {b}: ({a} != {b}) and ({a} == {c_val}) or ({b} == {c_val}), ({a_val}, {b_val}))'
        else:
            if a == b:
                a, b = a+"_1", b+"_2"
                constraint = f'problem.addConstraint(lambda {a}, {b}, {c}: ({a} == {c}) or ({b} == {c}), ({a_val}, {b_val}, {c_val}))'
            else:
                constraint = f'problem.addConstraint(lambda {a}, {b}, {c}: ({a} != {b}) and (({a} == {c}) or ({b} == {c})), ({a_val}, {b_val}, {c_val}))'

    return constraint