from flask import Flask, render_template, request
from last import app, translate, load_translation_dict, add_phrase_to_dict  # Importez app depuis last.py
from chatgemini import model

app = Flask(__name__)

# Import functions from last.py after defining app
from last import translate, load_translation_dict  

@app.route('/')
def translator():
    return render_template('try.html')

@app.route('/try.html')
def home():
    return render_template('try.html')

@app.route('/ask_gemini', methods=['POST'])
def ask_gemini():
    question = request.form['question']
    try:
        # Step 1: Translate Darija to English
        initial_output = translate(question, translation_dict, reverse_translation_dict, 'darija_to_eng')
        print("Initial Translation (Darija to English):", initial_output)

        # Step 2: Use Gemini to refine the English translation
        refinement_prompt = f"Refine this translation to English: {initial_output}"
        gemini_response = model.generate_content(refinement_prompt)
        refined_output_data = gemini_response.text.strip()
        print("Refined Translation by Gemini (English):", refined_output_data)

        # Step 3: Explanation/Description of the question
        explanation_prompt = f"Explain or provide a description for the following question in simple terms: {refined_output_data}"
        explanation_response = model.generate_content(explanation_prompt)
        explanation = explanation_response.text.strip()
        print("Explanation of the question:", explanation)

        # Step 4: Translate back to Darija (English to Darija)
        final_output = translate(refined_output_data, translation_dict, reverse_translation_dict, 'eng_to_darija')
        print("Translated Back to Darija:", final_output)

        # Step 5: Use Gemini to refine the final Darija translation
        refinement_prompt_darija = f"Refine this Darija translation (using Latin letters): {final_output}"
        gemini_response_darija = model.generate_content(refinement_prompt_darija)
        refined_final_output = gemini_response_darija.text.strip()
        print("Final Refined Translation by Gemini (Darija):", refined_final_output)

        # Return the final refined output along with the explanation
        return render_template('try.html', gemini_response=refined_final_output, explanation=explanation, question=question)

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
            print("Initial Translation:", initial_output)

            # Step 3: Refine the translation using Gemini (if direction is Darija to English)
            if direction == 'darija_to_eng':
                refinement_prompt = f"Refine this translation to English: {initial_output}"
                gemini_response = model.generate_content(refinement_prompt)
                refined_output = gemini_response.text.strip()
                print("Refined Translation by Gemini:", refined_output)
            else:
                # For English to Darija, translate back to Darija and refine using Gemini
                refinement_prompt = f"Refine this translation to Darija (using Latin letters): {initial_output}"
                gemini_response = model.generate_content(refinement_prompt)
                refined_output = gemini_response.text.strip()
                print("Refined Translation to Darija:", refined_output)

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
        add_phrase_to_dict(english_phrase, darija_phrase, 'dataset.csv')  # Add phrase to dictionary
        return render_template('try.html')

if __name__ == '__main__':
    # Load both dictionaries (English → Darija and Darija → English)
    translation_dict, reverse_translation_dict = load_translation_dict('dataset.csv')
    app.run(debug=True)
