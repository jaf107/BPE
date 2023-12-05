import tokenize
from io import BytesIO
import re

# Example usage:
input_code = """
def addTwoNums(a, b):
    return a + b
def multiply_three_nums(a,b,c):
    return a*b*c
def SubtractFromTheFirst(a,b):
    return a-b
"""
token_type_names = {
    tokenize.ENDMARKER: 'ENDMARKER',
    tokenize.NAME: 'NAME',
    tokenize.NUMBER: 'NUMBER',
    tokenize.STRING: 'STRING',
    tokenize.NEWLINE: 'NEWLINE',
    tokenize.INDENT: 'INDENT',
    tokenize.DEDENT: 'DEDENT',
    tokenize.OP: 'OPERATOR',
    tokenize.ERRORTOKEN: 'ERRORTOKEN',
}
def sanitize_code(code):
    sanitized_tokens = []
    code_bytes = code.encode('utf-8')
    token_generator = tokenize.tokenize(BytesIO(code_bytes).readline)
    allowed_token_types = {tokenize.NAME, tokenize.NUMBER, tokenize.STRING, tokenize.OP}
    for token in token_generator:
        token_type = token.type
        if token_type in allowed_token_types:
            token_value = token.string
            sanitized_tokens.append((token_type_names.get(token_type, 'UNK'), token_value))
    return sanitized_tokens

sanitized_tokens = sanitize_code(input_code)
# for token_type, token_value in sanitized_tokens:
#     # print(f"{token_type}: {token_value}")
#     print(f"{token_value}")



def is_camel_case(input_string):
    # Check if the string matches the camelCase pattern
    return re.match(r'^[a-z]+(?:[A-Z][a-z]*)*$', input_string) is not None

def is_pascal_case(input_string):
    # Check if the string matches the PascalCase pattern
    return re.match(r'^[A-Z][a-z]*(?:[A-Z][a-z]*)*$', input_string) is not None

def is_snake_case(input_string):
    # Check if the string matches the snake_case pattern
    return re.match(r'^[a-z]+(?:_[a-z]+)*$', input_string) is not None

def is_all_small(input_string):
    # Use a regular expression to match only lowercase letters
    return re.match(r'^[a-z]+$', input_string) is not None

def tokenize_camel_case(input_string):
    # Use regular expression to split camelCase string
    tokens = re.findall(r'[a-z]+|[A-Z][a-z]*', input_string)
    tokens[0] = 'Ġ' + tokens[0]
    return tokens

def tokenize_pascal_case(input_string):
    # Use regular expression to split PascalCase string
    tokens = re.findall(r'[A-Z][a-z]*', input_string)
    tokens[0] = 'Ġ' + tokens[0]
    return tokens

def tokenize_snake_case(input_string):
    # Split snake_case string using underscores
    tokens = input_string.split('_')
    tokens[0] = 'Ġ' + tokens[0]
    return tokens

def tokenize_based_on_case(input_string):
    if not is_all_small(input_string):
        if is_camel_case(input_string) :
            # print("camelCase",input_string )
            return tokenize_camel_case(input_string)
        elif is_pascal_case(input_string):
            # print("PascalCase",input_string )
            return tokenize_pascal_case(input_string)
        elif is_snake_case(input_string):
            # print("snake_case",input_string )
            return tokenize_snake_case(input_string)
        

corpus = []
for token_type, token_value in sanitized_tokens:
    modified_token = 'Ġ' + token_value
    corpus.append(modified_token)
    tokens = tokenize_based_on_case(token_value)
    if tokens:
        corpus.extend(tokens)

from collections import defaultdict
code_word_freqs = defaultdict(int)

# print(corpus)
for word in corpus:
  code_word_freqs[word] += 1
# print(tokenize_camel_case('addTwoNums'))
print(code_word_freqs)