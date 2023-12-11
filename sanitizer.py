import re
from io import BytesIO
import tokenize
import keyword


class CodeSanitizer:
    def __init__(self):
        self.token_type_names = {
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

    def sanitize_code(self, code):
        sanitized_tokens = []

        if self.is_python_code(code):
            if isinstance(code, str):
                code_bytes = code.encode('utf-8')
                token_generator = tokenize.tokenize(
                    BytesIO(code_bytes).readline)
            elif isinstance(code, list):
                code_bytes = [segment.encode('utf-8') for segment in code]
                code_bytes = b'\n'.join(code_bytes)
                token_generator = tokenize.tokenize(
                    BytesIO(code_bytes).readline)
            else:
                raise ValueError(
                    "Unsupported input type. Use either string or list.")

            allowed_token_types = {tokenize.NAME,
                                   tokenize.NUMBER, tokenize.STRING, tokenize.OP}
            for token in token_generator:
                token_type = token.type
                if token_type in allowed_token_types:
                    token_value = token.string
                    sanitized_tokens.append(
                        (self.token_type_names.get(token_type, 'UNK'), token_value))
        else:
            sanitized_tokens.append(('TEXT', code))
        return sanitized_tokens

    def is_python_code(self, code):
        python_keywords = keyword.kwlist
        additional_keywords = ["def", "class", "if", "else", "for", "while"]
        code_keywords = set(python_keywords + additional_keywords)
        return any(keyword in code for keyword in code_keywords)

    # def sanitize_code(self, code):
    #     sanitized_tokens = []

    #     if isinstance(code, str):
    #         # Handle string input
    #         code_bytes = code.encode('utf-8')
    #         token_generator = tokenize.tokenize(BytesIO(code_bytes).readline)
    #     elif isinstance(code, list):
    #         # Handle list input
    #         code_bytes = [segment.encode('utf-8') for segment in code]
    #         code_bytes = b'\n'.join(code_bytes)
    #         token_generator = tokenize.tokenize(BytesIO(code_bytes).readline)
    #     else:
    #         raise ValueError(
    #             "Unsupported input type. Use either string or list.")

    #     allowed_token_types = {tokenize.NAME,
    #                            tokenize.NUMBER, tokenize.STRING, tokenize.OP}
    #     for token in token_generator:
    #         token_type = token.type
    #         if token_type in allowed_token_types:
    #             token_value = token.string
    #             sanitized_tokens.append(
    #                 (self.token_type_names.get(token_type, 'UNK'), token_value))

    #     return sanitized_tokens

    # def has_code_keywords(text):
    #     python_keywords = keyword.kwlist
    #     additional_keywords = ["def", "class", "if", "else", "for", "while"]
    #     code_keywords = set(python_keywords + additional_keywords)
    #     return any(keyword in text for keyword in code_keywords)

    def is_camel_case(self, input_string):
        return re.match(r'^[a-z]+(?:[A-Z][a-z]*)*$', input_string) is not None

    def is_pascal_case(self, input_string):
        return re.match(r'^[A-Z][a-z]*(?:[A-Z][a-z]*)*$', input_string) is not None

    def is_snake_case(self, input_string):
        return re.match(r'^[a-z]+(?:_[a-z]+)*$', input_string) is not None

    def is_all_small(self, input_string):
        return re.match(r'^[a-z]+$', input_string) is not None

    def tokenize_camel_case(self, input_string):
        tokens = re.findall(r'[a-z]+|[A-Z][a-z]*', input_string)
        tokens[0] = 'Ġ' + tokens[0]
        return tokens

    def tokenize_pascal_case(self, input_string):
        tokens = re.findall(r'[A-Z][a-z]*', input_string)
        tokens[0] = 'Ġ' + tokens[0]
        return tokens

    def tokenize_snake_case(self, input_string):
        tokens = input_string.split('_')
        tokens[0] = 'Ġ' + tokens[0]
        return tokens

    def tokenize_based_on_case(self, input_string):
        if not self.is_all_small(input_string):
            if self.is_camel_case(input_string):
                return self.tokenize_camel_case(input_string)
            elif self.is_pascal_case(input_string):
                return self.tokenize_pascal_case(input_string)
            elif self.is_snake_case(input_string):
                return self.tokenize_snake_case(input_string)

    def remove_special_token(self, token, special_character='Ġ'):
        return token.replace(special_character, '')


# # Example usage:
# code_sanitizer = CodeSanitizer()
# input_code = """
# def addThreeNums(a, b, c):
#     return a + b + c
# def multiply_three_nums(a,b,c):
#     return a*b*c
# def SubtractFromTheFirst(a,b):
#     return a-b
# """

# sanitized_tokens = code_sanitizer.sanitize_code(input_code)
# print(sanitized_tokens)

# Use other methods as needed...
