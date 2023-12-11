import keyword


def has_code_keywords(text):
    python_keywords = keyword.kwlist
    additional_keywords = ["def", "class", "if", "else", "for", "while"]
    code_keywords = set(python_keywords + additional_keywords)
    return any(keyword in text for keyword in code_keywords)


corpus = """
def addThreeNums(a, b, c):
    return a + b + c
def multiply_three_nums(a,b,c):
    return a*b*c
def SubtractFromTheFirst(a,b):
    return a-b
"""

print(has_code_keywords(corpus))
