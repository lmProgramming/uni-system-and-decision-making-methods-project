def add_space_before_capital_letters(s: str) -> str:
    for i in s:
        if i.isupper():
            s = s.replace(i, " " + i)
    return s


def convert_str_to_capitalized_words(s: str) -> str:
    return " ".join(
        [word.capitalize() for word in add_space_before_capital_letters(s).split(" ")]
    )
