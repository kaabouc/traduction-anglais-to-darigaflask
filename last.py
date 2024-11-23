import csv
import string
import nltk
from collections import defaultdict
from flask import request, render_template
from flask import Flask
from textblob import Word

app = Flask(__name__)

def load_translation_dict(file_path):
    translation_dict = defaultdict(list)
    reverse_translation_dict = defaultdict(list)
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            if len(row) < 2:
                continue
            darija, english = row
            # Ajouter les traductions dans les deux sens
            translation_dict[english.lower()].append(darija)
            reverse_translation_dict[darija.lower()].append(english)
    return translation_dict, reverse_translation_dict


def translate(sentence, translation_dict, reverse_dict, direction="en-to-darija"):
    sentence = sentence.translate(str.maketrans('', '', string.punctuation))
    words = nltk.word_tokenize(sentence.lower())
    translated_words = []
    current_dict = translation_dict if direction == "en-to-darija" else reverse_dict

    for word in words:
        if word in current_dict:
            translated_words.append(current_dict[word][0])  # Utilisez la première traduction disponible
        else:
            # Si le mot n'existe pas, on le garde inchangé
            translated_words.append(word)
    return ' '.join(translated_words)


def add_phrase_to_dict(english_phrase, darija_phrase, file_path):
    with open(file_path, 'a') as file:
        writer = csv.writer(file)
        writer.writerow([english_phrase, darija_phrase])
        
def add_phrase():
    if request.method == "POST":
        english_phrase = request.form['english-phrase']
        darija_phrase = request.form['darija-phrase']
        add_phrase_to_dict(english_phrase, darija_phrase, 'dataset.csv')
        # Reload the translation dictionary
        global translation_dict
        translation_dict = load_translation_dict('dataset.csv')
        return render_template('try.html')