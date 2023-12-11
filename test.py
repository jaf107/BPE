from bpe_tokenizer import BpeTokenizer
import os

default_corpus = ""
# default_corpus = """
# def addThreeNums(a, b, c):
#     return a + b + c
# def multiply_three_nums(a,b,c):
#     return a*b*c
# def SubtractFromTheFirst(a,b):
#     return a-b
# """
default_corpus = """
    This is the Hugging Face Course.
    This chapter is about tokenization.
    This section shows several tokenizer algorithms.
    Hopefully, you will be able to understand how they are trained and generate tokens.
"""
tokenizer = BpeTokenizer(20000)

tokenizer.train(default_corpus)

# file_path = os.path.join("dataset", "test.txt")

# with open(file_path, "r", encoding="ISO-8859-1") as file:
#     default_corpus = file.readlines()
# # print(len(default_corpus))

# tokenizer.train(default_corpus)

result = tokenizer.tokenize("""
This is not a token.
""")
# print(result)
vocab = tokenizer.get_vocab()['vocab']
vocab_size = tokenizer.get_vocab()['vocab_size']
print(vocab_size)
print(result)
