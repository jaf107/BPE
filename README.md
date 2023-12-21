This project is done for Software-Project-Lab 3 course.

## PyPI Package

Install the BPE tokenizer package using the following command:

```bash
pip install python-bpe-tokenizer
```

## Usage

```python
from bpe_tokenizer import BPETokenizer

# Instantiate the BPE tokenizer
tokenizer = BPETokenizer()

# Train the tokenizer on your data
tokenizer.train(corpus)

# Tokenize text using the trained tokenizer
tokenized_text = tokenizer.tokenize("Hello, world!")

# Detokenize text using the trained tokenizer
detokenized_text = tokenizer.detokenize(tokenized_text)
```

For more detailed examples and usage, refer to the [documentation](https://drive.google.com/file/d/1ISfmKGE8dyLZLSashgL2AsHo4LKNK-Yd/view?usp=drive_link).

## Documentation

Detailed documentation is available at [link](https://drive.google.com/file/d/1ISfmKGE8dyLZLSashgL2AsHo4LKNK-Yd/view?usp=drive_link).

## BPE Playground

Explore and test the BPE tokenizer in the [BPE Playground](http://jaf107.pythonanywhere.com/).

## Contact

For any inquiries or feedback, feel free to contact the maintainers:

- Abu Jafar Saifullah
  - Email: jafarmahin107@gmail.com

