from flask import Flask, render_template, request
from last import translate, load_translation_dict, add_phrase_to_dict

app = Flask(__name__)

# Charger le dictionnaire de traduction globalement
translation_dict = load_translation_dict('dataset.csv')

@app.route('/')
def home():
    return render_template('try.html')

@app.route("/translate", methods=["POST"])
def translate_text():
    input_text = request.form.get('english-input')
    if input_text:
        print("Input Text:", input_text)
        output = translate(input_text, translation_dict)
        return render_template('try.html', output=output, input_text=input_text)
    return render_template('try.html')

@app.route("/add_phrase", methods=["POST"])
def add_phrase():
    english_phrase = request.form.get('english-phrase')
    darija_phrase = request.form.get('darija-phrase')
    if english_phrase and darija_phrase:
        add_phrase_to_dict(english_phrase, darija_phrase, 'dataset.csv')
    return render_template('try.html')

if __name__ == '__main__':
    app.run(debug=True)
