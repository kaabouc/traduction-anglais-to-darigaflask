import pandas as pd
from flask import Flask, request, render_template

# Initialisation de l'application Flask
app = Flask(__name__)

# Chemin du dataset CSV
dataset_path = "../dataset.csv"

# Charger le dataset dans un DataFrame
try:
    df = pd.read_csv(dataset_path)
except FileNotFoundError:
    # Créer un fichier vide si le dataset n'existe pas
    df = pd.DataFrame(columns=["english", "darija"])
    df.to_csv(dataset_path, index=False)

# Fonction pour rechercher une traduction
def translate(word, source_lang, target_lang):
    row = df[df[source_lang] == word]
    if not row.empty:
        return row[target_lang].values[0]
    return f"No translation found for '{word}'"

# Fonction pour ajouter une nouvelle phrase au dataset
def add_phrase(english, darija):
    global df
    # Vérifier si la phrase existe déjà
    if ((df["english"] == english) & (df["darija"] == darija)).any():
        return "Phrase already exists in the dataset."

    # Ajouter une nouvelle ligne au DataFrame
    new_row = pd.DataFrame({"english": [english], "darija": [darija]})
    df = pd.concat([df, new_row], ignore_index=True)

    # Sauvegarder le DataFrame dans le fichier CSV
    df.to_csv(dataset_path, index=False)
    return "Phrase added successfully."

# Route pour afficher l'interface utilisateur
@app.route("/")
def index():
    return render_template("index.html", output="")

# Route pour traiter les requêtes de traduction
@app.route("/translate", methods=["POST"])
def handle_translation():
    english_word = request.form.get("english-input", "").strip()
    if english_word:
        result = translate(english_word, "english", "darija")
    else:
        result = "Please enter a word to translate."
    return render_template("index.html", output=result)

# Route pour ajouter une nouvelle phrase au dataset
@app.route("/add_phrase", methods=["POST"])
def handle_add_phrase():
    english_phrase = request.form.get("english-phrase", "").strip()
    darija_phrase = request.form.get("darija-phrase", "").strip()

    if english_phrase and darija_phrase:
        result = add_phrase(english_phrase, darija_phrase)
    else:
        result = "Both English and Darija phrases are required."

    return render_template("index.html", output=result)

if __name__ == "__main__":
    app.run(debug=True)
