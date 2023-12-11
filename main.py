from flask import Flask, request, jsonify, render_template
from bpe_tokenizer import BpeTokenizer
import os
file_path = os.path.join("dataset", "corpus.txt")
app = Flask(__name__)
tokenizer = BpeTokenizer()

default_corpus = ""
with open(file_path, "r", encoding="utf-8") as file:
    default_corpus = file.readlines()

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


@app.route('/get_corpus', methods=['GET'])
def get_corpus_text():
    corpus_text = tokenizer.get_corpus_text()
    return jsonify({'original_text': corpus_text['original_text']}), 200


@app.route('/upload_file', methods=['POST'])
def upload_file():
    try:
        uploaded_file = request.files['file']

        # Read the content of the file
        file_content = uploaded_file.read().decode('utf-8')

        # Update the corpus based on the file content
        tokenizer.train(file_content)

        return jsonify({'message': 'Corpus updated successfully'}), 200
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return jsonify({'error': 'Failed to update corpus'}), 500


if __name__ == '__main__':
    app.run(debug=True)
