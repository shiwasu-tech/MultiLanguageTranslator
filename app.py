from flask import Flask, request, jsonify, render_template
from google.cloud import translate_v2 as translate
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
translate_client = translate.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate_text():
    logging.debug("Received request for translation")
    data = request.get_json()
    logging.debug(f"Request data: {data}")
    text = data.get('text')
    target_languages = data.get('target_languages', [])

    if not text or not target_languages:
        logging.error("Missing text or target languages")
        return jsonify({'error': 'テキストと翻訳先言語を指定してください．'}), 400

    translations = {}
    for lang in target_languages:
        logging.debug(f"Translating to {lang}")
        result = translate_client.translate(text, target_language=lang)
        translations[lang] = result['translatedText']

    logging.debug(f"Translations: {translations}")
    return jsonify(translations)

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(debug=True)