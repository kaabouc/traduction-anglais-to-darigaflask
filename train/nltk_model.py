import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
import string

# Assurez-vous d'avoir téléchargé les ressources nécessaires de NLTK
nltk.download('punkt')

# Étape 1 : Charger le fichier CSV
file_path = "../dataset.csv"  # Remplacez par le chemin vers votre fichier
data = pd.read_csv(file_path)

# Vérifiez que le CSV contient les colonnes 'english' et 'darija'
if 'english' not in data.columns or 'darija' not in data.columns:
    raise ValueError("Le fichier CSV doit contenir les colonnes 'english' et 'darija'.")

# Étape 2 : Créer un dictionnaire de traduction
translation_dict = dict(zip(data['english'], data['darija']))

# Étape 3 : Fonction pour traduire un paragraphe
def translate_paragraph(paragraph):
    # Prétraitement : Tokenization
    tokens = word_tokenize(paragraph.lower())
    
    # Nettoyage : suppression de la ponctuation
    tokens = [word for word in tokens if word not in string.punctuation]
    
    # Traduction : remplacer les mots par leurs équivalents en darija
    translated_tokens = [translation_dict.get(word, word) for word in tokens]
    
    # Reconstruction de la phrase traduite
    translated_paragraph = ' '.join(translated_tokens)
    return translated_paragraph

# Exemple de paragraphe en anglais
english_paragraph = "Hello, how are you? I want to learn Darija!"

# Traduction
darija_translation = translate_paragraph(english_paragraph)

print("Original:", english_paragraph)
print("Translated:", darija_translation)
