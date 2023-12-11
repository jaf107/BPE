from collections import defaultdict
from transformers import AutoTokenizer
from sanitizer import CodeSanitizer
from tqdm import tqdm


class BpeTokenizer:
    def __init__(self, vocab_size=10000):
        self.vocab_size = vocab_size
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.sanitizer = CodeSanitizer()
        self.merges = None
        self.corpusText = ""
        self.vocab = []
        self.sanitized_tokens = []
        self.word_freqs = defaultdict(int)

    def _pre_tokenize(self, input):
        corpus = []

        if isinstance(input, str):
            sanitized_tokens = self.sanitizer.sanitize_code(input)
            for token_type, token_value in sanitized_tokens:
                modified_token = 'Ġ' + token_value
                corpus.append(modified_token)
                tokens = self.sanitizer.tokenize_based_on_case(token_value)
                if tokens:
                    corpus.extend(tokens)
        elif isinstance(input, list):
            for code_segment in input:
                sanitized_tokens = self.sanitizer.sanitize_code(code_segment)
                for token_type, token_value in sanitized_tokens:
                    modified_token = 'Ġ' + token_value
                    corpus.append(modified_token)
                    tokens = self.sanitizer.tokenize_based_on_case(token_value)
                    if tokens:
                        corpus.extend(tokens)
        else:
            raise ValueError(
                "Unsupported input type. Use either string or list.")

        sanitized_tokens = self.sanitizer.sanitize_code(input)
        self.sanitized_tokens = sanitized_tokens
        word_freqs = defaultdict(int)

        for token_type, token_value in sanitized_tokens:
            modified_token = 'Ġ' + token_value
            corpus.append(modified_token)
            tokens = self.sanitizer.tokenize_based_on_case(token_value)
            if tokens:
                corpus.extend(tokens)
        for word in corpus:
            word_freqs[word] += 1

        self.word_freqs = word_freqs
        return word_freqs

    def _compute_pair_freqs(self, splits, word_freqs):
        pair_freqs = defaultdict(int)
        for word, freq in word_freqs.items():
            split = splits[word]
            if len(split) == 1:
                continue
            for i in range(len(split) - 1):
                pair = (split[i], split[i + 1])
                pair_freqs[pair] += freq
        return pair_freqs

    def _merge_most_frequent_pairs_with_progress(self, alphabet, word_freqs, tqdm_bar):
        def merge_pair(a, b, splits):
            for word in word_freqs:
                split = splits[word]
                if len(split) == 1:
                    continue

                i = 0
                while i < len(split) - 1:
                    if split[i] == a and split[i + 1] == b:
                        split = split[:i] + [a + b] + split[i + 2:]
                    else:
                        i += 1
                splits[word] = split
            return splits

        vocab = [""] + alphabet.copy()
        splits = {word: [c for c in word] for word in word_freqs.keys()}
        merges = {}

        while len(vocab) < self.vocab_size:
            pair_freqs = self._compute_pair_freqs(splits, word_freqs)
            if not pair_freqs:
                break
            best_pair = max(pair_freqs, key=pair_freqs.get)
            splits = merge_pair(*best_pair, splits)
            merges[best_pair] = best_pair[0] + best_pair[1]
            vocab.append(best_pair[0] + best_pair[1])
            tqdm_bar.update(1)

        return vocab, merges

    def _tokenize(self, text):
        text = text.strip()
        text = " " + text

        pre_tokenize_result = self.tokenizer._tokenizer.pre_tokenizer.pre_tokenize_str(
            text)
        pre_tokenized_text = [word for word, offset in pre_tokenize_result]
        splits = [[l for l in word] for word in pre_tokenized_text]
        for pair, merge in self.merges.items():
            for idx, split in enumerate(splits):
                i = 0
                while i < len(split) - 1:
                    if split[i] == pair[0] and split[i + 1] == pair[1]:
                        split = split[:i] + [merge] + split[i + 2:]
                    else:
                        i += 1
                splits[idx] = split
        tokens = sum(splits, [])
        tokens = [self.sanitizer.remove_special_token(
            token) for token in tokens]
        return tokens

    def train(self, input):
        self.corpusText = input
        sanitized_tokens = self.sanitizer.sanitize_code(input)
        word_freqs = self._pre_tokenize(input)

        alphabet = []
        for word in word_freqs.keys():
            for letter in word:
                if letter not in alphabet:
                    alphabet.append(letter)
        alphabet.sort()

        # self.vocab, self.merges = self._merge_most_frequent_pairs(
        #     alphabet, word_freqs)
        tqdm_bar = tqdm(total=self.vocab_size,
                        desc="Training BPE", unit="merge")
        self.vocab, self.merges = self._merge_most_frequent_pairs_with_progress(
            alphabet, word_freqs, tqdm_bar)
        tqdm_bar.close()

    def tokenize(self, text):
        if self.merges is None:
            raise ValueError(
                "Tokenizer has not been trained. Call 'train' method first.")
        return self._tokenize(text)

    def get_corpus_text(self):
        return {
            "original_text": self.corpusText
        }

    def get_vocab(self):
        return {
            "vocab": self.vocab,
            "vocab_size": len(self.vocab)
        }

    def get_merges_list(self):
        return {
            "merge": self.merges
        }


# Example usage:
# tokenizer = BpeTokenizer()
# tokenizer.train("""
# def addThreeNums(a, b, c):
#     return a + b + c
# def multiply_three_nums(a,b,c):
#     return a*b*c
# def SubtractFromTheFirst(a,b):
#     return a-b
# """)
# result = tokenizer.tokenize("""
# def SubtractThreeNums(m,a, b, c):
#     return m - a - b - c
# """)
# print(result)
