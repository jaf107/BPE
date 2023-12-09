from bpe_tokenizer import BpeTokenizer

tokenizer = BpeTokenizer()
tokenizer.train("""
def SubtractThreeNums(a, b, c):
    return a + b + c
def multiply_three_nums(a,b,c):
    return a*b*c
def SubtractFromTheFirst(a,b):
    return a-b
""")
result = tokenizer.tokenize("""
def SubtractThreeNums(m,a, b, c):
    return m - a - b - c
""")
print(result)
print(tokenizer.get_corpus_text())
