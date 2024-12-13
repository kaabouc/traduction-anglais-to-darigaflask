from flask import Flask, render_template, request
from last import app, translate, load_translation_dict, add_phrase_to_dict  # Importez app depuis last.py
from chatgemini import model
import os

app = Flask(__name__)

# Import functions from last.py after defining app
from last import translate, load_translation_dict  

@app.route('/')
def translator():
    return render_template('try.html')  # Change this line

@app.route('/try.html')
def home():
    return render_template('try.html')

@app.route('/ask_gemini', methods=['POST'])
def ask_gemini():
    question = request.form['question']
    try:
        refinement_prompt = f"Refine this translation to English: {question}"
        gemini_response = model.generate_content(refinement_prompt)
        refined_output_data = gemini_response.text.strip()        
        print("Traduction raffinée par Gemini:", refined_output_data)
        response = model.generate_content(f"Provide a concise response in Darija using Latin letters (a to z): {refined_output_data}")
        gemini_response = response.text.strip()
    except Exception as e:
        gemini_response = f"Error: {str(e)}"

    return render_template('try.html', gemini_response=gemini_response, question=question)


@app.route("/translate", methods=["POST"])
def translate_text():
    if request.method == "POST":
        try:
            # Step 1: Get input text and direction
            input_text = request.form['input-text']
            direction = request.form['direction']  # Direction: 'darija_to_eng' or 'eng_to_darija'

            # Step 2: Perform initial translation using the dictionary
            initial_output = translate(input_text, translation_dict, reverse_translation_dict, direction)
            print("Traduction initiale:", initial_output)  # Log the initial output

            # Step 3: Refine the translation using Gemini (if direction is Darija to English)
            if direction == 'darija_to_eng':
                refinement_prompt = f"Refine this translation to English: {initial_output}"
                gemini_response = model.generate_content(refinement_prompt)
                refined_output = gemini_response.text.strip()
                print("Traduction raffinée par Gemini:", refined_output)  # Log the refined output
            else:
                # refinement_prompt = f"Refine this translation to Darija language ( morocco ) latine lettre : {initial_output}"
                # gemini_response = model.generate_content(refinement_prompt)
                # refined_output = gemini_response.text.strip()
                # For English to Darija, no Gemini refinement needed
                refined_output = initial_output

            # Step 4: Send results to the template
            return render_template(
                'try.html',
                input_text=input_text,
                initial_output=initial_output,
                refined_output=refined_output
            )

        except Exception as e:
            print("Erreur pendant la traduction:", str(e))
            return render_template('try.html', error=str(e))


@app.route("/add_phrase", methods=["GET", "POST"])
def add_phrase():
    if request.method == "POST":
        english_phrase = request.form['english-phrase']
        darija_phrase = request.form['darija-phrase']
        add_phrase_to_dict(english_phrase, darija_phrase, 'dataset.csv')  # Ajoutez la phrase à votre dictionnaire de traduction
        return render_template('try.html')

if __name__ == '__main__':
    # Charger les deux dictionnaires (Anglais → Darija et Darija → Anglais)
    translation_dict, reverse_translation_dict = load_translation_dict('dataset.csv')
    # Obtenez le port depuis l'environnement ou utilisez 5000 par défaut
    port = int(os.environ.get("PORT", 5000))

    # Démarrez le serveur Flask
    app.run(host="0.0.0.0", port=port, debug=True)