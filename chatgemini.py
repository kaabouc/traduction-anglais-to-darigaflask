import os
import google.generativeai as genai
from dotenv import load_dotenv  # Importer dotenv

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()
GENAI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=os.getenv('GENAI_API_KEY'))

# Initialize the Gemini model
generation_config = {
    'temperature': 0.2,
    'max_output_tokens': 100,
    'top_p': 0.8,
    'top_k': 40
}

model = genai.GenerativeModel('gemini-pro', generation_config=generation_config)
