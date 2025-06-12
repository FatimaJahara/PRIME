import re

def process_unaligned_pair_clues(clue):
    # cleaned_clue = re.sub(r"\s+", " ", clue).strip()
    # print(cleaned_clue)
    # pattern = r"""
    # !\(\(\s*([\w\s]+)\s*=\s*([\w\s]+)\s*\)\s*=\s*\(\s*([\w\s]+)\s*=\s*([\w\s]+)\s*\)\)\s*and\s*
    # \(\(\(\s*([\w\s]+)\s*=\s*([\w\s]+)\s*\)\s*=\s*\(\s*([\w\s]+)\s*=\s*([\w\s]+)\s*\)\)\s*or\s*
    # \(\(\s*([\w\s]+)\s*=\s*([\w\s]+)\)\s*=\s*\(\s*([\w\s]+)\s*=\s*([\w\s]+)\)\)\)\s*and\s*
    # \(\(\(\s*([\w\s]+)\s*=\s*([\w\s]+)\)\s*=\s*\(\s*([\w\s]+)\s*=\s*([\w\s]+)\)\)\s*or\s*
    # \(\(\s*([\w\s]+)\s*=\s*([\w\s]+)\)\s*=\s*\(\s*([\w\s]+)\s*=\s*([\w\s]+)\)\)\)\s*
    # """
    cleaned_clue = re.sub(r"\s+", " ", clue).strip()
    print(f"Cleaned clue: {cleaned_clue}")
    # pattern = r"""
    # !\(\(\s*([\w\s]+)\s*=\s*([\w\s]+)\s*\)\s*=\s*\(\s*([\w\s]+)\s*=\s*([\w\s]+)\s*\)\)\s*and\s*
    # \(\(\(\s*([\w\s]+)\s*=\s*([\w\s]+)\s*\)\s*=\s*\(\s*([\w\s]+)\s*=\s*([\w\s]+)\s*\)\)\s*or\s*
    # \(\(\s*([\w\s]+)\s*=\s*([\w\s]+)\)\s*=\s*\(\s*([\w\s]+)\s*=\s*([\w\s]+)\)\)\)\s*and\s*
    # \(\(\(\s*([\w\s]+)\s*=\s*([\w\s]+)\)\s*=\s*\(\s*([\w\s]+)\s*=\s*([\w\s]+)\)\)\s*or\s*
    # \(\(\s*([\w\s]+)\s*=\s*([\w\s]+)\)\s*=\s*\(\s*([\w\s]+)\s*=\s*([\w\s]+)\)\)\)\s*
    # """

    # pattern = r"""
    # !\(\(\s*([\w\s-]+)\s*=\s*([\w\s-]+)\s*\)\s*=\s*\(\s*([\w\s-]+)\s*=\s*([\w\s-]+)\s*\)\)\s*and\s*
    # \(\(\(\s*([\w\s-]+)\s*=\s*([\w\s-]+)\s*\)\s*=\s*\(\s*([\w\s-]+)\s*=\s*([\w\s-]+)\s*\)\)\s*or\s*
    # \(\(\s*([\w\s-]+)\s*=\s*([\w\s-]+)\)\s*=\s*\(\s*([\w\s-]+)\s*=\s*([\w\s-]+)\)\)\)\s*and\s*
    # \(\(\(\s*([\w\s-]+)\s*=\s*([\w\s-]+)\)\s*=\s*\(\s*([\w\s-]+)\s*=\s*([\w\s-]+)\)\)\s*or\s*
    # \(\(\s*([\w\s-]+)\s*=\s*([\w\s-]+)\)\s*=\s*\(\s*([\w\s-]+)\s*=\s*([\w\s-]+)\)\)\)\s*
    # """
    # pattern = r"""
    #     !\(\(\s*([\w\s_\-'.]+)\s*=\s*([\w\s_\-'.]+)\s*\)\s*=\s*\(\s*([\w\s_\-'.]+)\s*=\s*([\w\s_\-'.]+)\s*\)\)\s*and\s*
    #     \(\(\(\s*([\w\s_\-'.]+)\s*=\s*([\w\s_\-'.]+)\s*\)\s*=\s*\(\s*([\w\s_\-'.]+)\s*=\s*([\w\s_\-'.]+)\)\)\s*or\s*
    #     \(\(\s*([\w\s_\-'.]+)\s*=\s*([\w\s_\-'.]+)\)\s*=\s*\(\s*([\w\s_\-'.]+)\s*=\s*([\w\s_\-'.]+)\)\)\)\s*and\s*
    #     \(\(\(\s*([\w\s_\-'.]+)\s*=\s*([\w\s_\-'.]+)\)\s*=\s*\(\s*([\w\s_\-'.]+)\s*=\s*([\w\s_\-'.]+)\)\)\s*or\s*
    #     \(\(\s*([\w\s_\-'.]+)\s*=\s*([\w\s_\-'.]+)\)\s*=\s*\(\s*([\w\s_\-'.]+)\s*=\s*([\w\s_\-'.]+)\)\)\)
    # """

    # pattern = r"""
    #       !\(\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\s*\)\s*=\s*\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\s*\)\)\s*and\s*
    #       \(\(\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\s*\)\s*=\s*\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\)\)\s*or\s*
    #       \(\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\)\s*=\s*\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\)\)\)\s*and\s*
    #       \(\(\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\)\s*=\s*\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\)\)\s*or\s*
    #       \(\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\)\s*=\s*\(\s*([\w\s_\-'.’\/&,:]+)\s*=\s*([\w\s_\-'.’\/&,:]+)\)\)\)
    #   """

    allowed_chars = r"[\wÀ-ÖØ-öø-ÿ\s_\-–—'ʻ’\"\/\\&,:#(){}\[\]=!<>?+*/%^.\d]+"

    pattern = rf"""
    !\(\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\s*=\s*\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\)\s*and\s*
    \(\(\(\s*({allowed_chars})\s*=\s*({allowed_chars})\s*\)\s*=\s*\(\s*({allowed_chars})\s*=\s*({allowed_chars})\)\)\s*or\s*
    \(\(\s*({allowed_chars})\s*=\s*({allowed_chars})\)\s*=\s*\(\s*({allowed_chars})\s*=\s*({allowed_chars})\)\)\)\s*and\s*
    \(\(\(\s*({allowed_chars})\s*=\s*({allowed_chars})\)\s*=\s*\(\s*({allowed_chars})\s*=\s*({allowed_chars})\)\)\s*or\s*
    \(\(\s*({allowed_chars})\s*=\s*({allowed_chars})\)\s*=\s*\(\s*({allowed_chars})\s*=\s*({allowed_chars})\)\)\)
"""





    match = re.match(pattern, cleaned_clue, re.VERBOSE)
    print(match)
    if match:
        constraint = None
        groups = match.groups()

        var1, val1, var2, val2 = groups[0:4]
        var3, val3, var4, val4 = groups[4:8]
        var5, val5, var6, val6 = groups[8:12]
        var7, val7, var8, val8 = groups[12:16]
        var9, val9, var10, val10 = groups[16:]

        def is_int(value):
            try:
                int(value)
                return True
            except ValueError:
                return False

        values = [val1.strip(), val2.strip(), val4.strip(), val6.strip()]

        formatted_values = []
        for value in values:
            if is_int(value):
                # formatted_values.append(value)
                formatted_values.append(f'"{str(value)}"')
            else:
                formatted_values.append(f'"{value}"')

        a, b, c, d = var1.strip(), var2.strip(), var4.strip(), var6.strip()
        a = a.replace(" ", "_") if " " in a else a
        b = b.replace(" ", "_") if " " in b else b
        c = c.replace(" ", "_") if " " in c else c
        d = d.replace(" ", "_") if " " in d else d

        a_val, b_val, c_val, d_val = formatted_values[0], formatted_values[1], formatted_values[2], formatted_values[3]

        c, d = c+"_1", d+"_2"

        if a == "Name":
            constraint = f'problem.addConstraint(lambda {b}, {c}, {d}: ({b} != {a_val}) and (({c} == {a_val}) or ({d} == {a_val})) and (({b} == {c}) or ({b} == {d})), ({b_val}, {c_val}, {d_val}))'

        elif b == "Name":
            constraint = f'problem.addConstraint(lambda {a}, {c}, {d}: ({a} != {b_val}) and (({a} == {c}) or ({a} == {d})) and (({c} == {b_val}) or ({d} == {b_val})), ({a_val}, {c_val}, {d_val}))'

        elif c == "Name_1" and d == "Name_2":
            constraint = f'problem.addConstraint(lambda {a}, {b}: ({a} != {b}) and (({a} == {c_val}) or ({a} == {d_val})) and (({b} == {c_val}) or ({b} == {d_val})), ({a_val}, {b_val}))'

        else:
            constraint = f'problem.addConstraint(lambda {a}, {b}, {c}, {d}: ({a} != {b}) and (({a} == {c}) or ({a} == {d})) and (({b} == {c}) or ({b} == {d})), ({a_val}, {b_val}, {c_val}, {d_val}))'

    return constraint