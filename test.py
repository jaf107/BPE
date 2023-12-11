from bpe_tokenizer import BpeTokenizer
import os

tokenizer = BpeTokenizer(20000)
# tokenizer.train("""
# def SubtractThreeNums(a, b, c):
#     return a + b + c
# def multiply_three_nums(a,b,c):
#     return a*b*c
# def SubtractFromTheFirst(a,b):
#     return a-b
# """)
file_path = os.path.join("dataset", "test.txt")

default_corpus = ""
with open(file_path, "r", encoding="ISO-8859-1") as file:
    default_corpus = file.readlines()
# print(len(default_corpus))

tokenizer.train(default_corpus)

result = tokenizer.tokenize("""
def addThreeNums(a, b, c):
    return a + b + c
""")
# print(result)
vocab = tokenizer.get_vocab()['vocab']
vocab_size = tokenizer.get_vocab()['vocab_size']
print(vocab_size)
print(result)
