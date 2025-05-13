from flask import Flask, request, jsonify, render_template
from google.cloud import translate_v2 as translate
from langdetect import detect
import logging
import re

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
translate_client = translate.Client()

# List of inappropriate words to filter
INAPPROPRIATE_WORDS = ["badword1", "badword2", "badword3"]

def filter_inappropriate_words(text):
    pattern = re.compile(r"\b(" + "|".join(map(re.escape, INAPPROPRIATE_WORDS)) + r")\b", re.IGNORECASE)
    return pattern.sub("***", text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    logging.debug("Received request for translation")
    data = request.get_json()
    logging.debug(f"Request data: {data}")
    text = data.get('text', '')
    target_languages = data.get('target_languages', [])

    if not text:
        logging.error("No text provided for translation.")
        return jsonify({"error": "No text provided for translation."}), 400

    if not target_languages:
        logging.error("No target languages selected.")
        return jsonify({"error": "No target languages selected."}), 400

    # Filter inappropriate words
    filtered_text = filter_inappropriate_words(text)

    # Detect source language
    try:
        source_language = detect(filtered_text)
        logging.debug(f"Detected source language: {source_language}")
    except Exception as e:
        logging.error(f"Error detecting source language: {e}")
        return jsonify({"error": "Could not detect source language."}), 500

    translations = {}
    for lang in target_languages:
        logging.debug(f"Translating to {lang}")
        result = translate_client.translate(filtered_text, target_language=lang)
        translations[lang] = result['translatedText']

    logging.debug(f"Translations: {translations}")
    return jsonify({"source_language": source_language, **translations})

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)