from flask import Flask, request, jsonify
from bpe_tokenizer import BpeTokenizer

app = Flask(__name__)
tokenizer = BpeTokenizer()
default_corpus = """
def addThreeNums(a, b, c):
    return a + b + c
def multiply_three_nums(a,b,c):
    return a*b*c
def SubtractFromTheFirst(a,b):
    return a-b
"""
tokenizer.train(default_corpus)
@app.route('/update_corpus', methods=['POST'])
def update_corpus():
    data = request.get_json()
    if 'corpus' in data:
        corpus = data['corpus']
        tokenizer.train(corpus)
        return jsonify({'message': 'Corpus updated successfully'}), 200
    else:
        return jsonify({'error': 'Missing corpus parameter'}), 400

@app.route('/tokenize', methods=['POST'])
def tokenize():
    data = request.get_json()
    if 'text' in data:
        text = data['text']
        result = tokenizer.tokenize(text)
        return jsonify({'tokenized_output': result}), 200
    else:
        return jsonify({'error': 'Missing text parameter'}), 400

if __name__ == '__main__':
    app.run(debug=True)
