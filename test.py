from bpe_tokenizer import BpeTokenizer
import os

tokenizer = BpeTokenizer()
# tokenizer.train("""
# def SubtractThreeNums(a, b, c):
#     return a + b + c
# def multiply_three_nums(a,b,c):
#     return a*b*c
# def SubtractFromTheFirst(a,b):
#     return a-b
# """)
file_path = os.path.join("dataset", "test_run.txt")

default_corpus = ""
with open(file_path, "r", encoding="utf-8") as file:
    default_corpus = file.read()

tokenizer.train(default_corpus)

result = tokenizer.tokenize("""
def SubtractThreeNums(m,a, b, c):
    return m - a - b - c
""")
# print(result)
vocab = tokenizer.get_vocab()['vocab']
vocab_size = tokenizer.get_vocab()['vocab_size']

print(result)
