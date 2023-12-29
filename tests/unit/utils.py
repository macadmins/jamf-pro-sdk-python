def remove_whitespaces_newlines(string: str):
    return "".join([i.strip() for i in string.split("\n")])
