from flask import Flask, request, jsonify, render_template
from bpe_tokenizer import BpeTokenizer

app = Flask(__name__)
tokenizer = BpeTokenizer()

default_corpus = ""
with open("corpus.txt", "r") as file:
    default_corpus = file.read()


tokenizer.train(default_corpus)


@app.route('/')
def playground():
    return render_template('index.html')


@app.route('/update-corpus')
def update_corpus_page():
    return render_template('update_corpus.html')


@app.route('/update_corpus_action', methods=['POST'])
def update_corpus_action():
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
