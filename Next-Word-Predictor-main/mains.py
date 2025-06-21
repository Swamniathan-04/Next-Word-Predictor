import json
from collections import defaultdict
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# Step 1: Load text data from the JSON file
def load_text_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['text']


# Load the text data from source.json
text = load_text_from_json('D:/Marvel_vs_DC/pythonProject1/.venv/source.json')

# Step 2: Tokenization
words = text.lower().split()

# Step 3: Create bigram frequency dictionary
bigram_freq = defaultdict(lambda: defaultdict(int))

for i in range(len(words) - 1):
    bigram_freq[words[i]][words[i + 1]] += 1


# Step 4: Function to predict the next words
def predict_next_words(current_words, num_predictions=3):
    current_words = current_words.lower().strip().split()
    if len(current_words) == 0:
        return []

    last_word = current_words[-1]

    if last_word in bigram_freq:
        next_words = bigram_freq[last_word]
        # Sort by frequency and get the most common next words
        sorted_words = sorted(next_words.items(), key=lambda item: item[1], reverse=True)
        predicted_words = [word for word, freq in sorted_words[:num_predictions]]
        return predicted_words
    else:
        return []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    predicted_words = predict_next_words(user_input)

    if predicted_words:
        response_text = f"Next possible words: {', '.join(predicted_words)}."
    else:
        response_text = "No predictions available."

    return jsonify({"response": response_text})


if __name__ == '__main__':
    app.run(debug=True)
