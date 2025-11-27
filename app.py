import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import PyPDF2

# Cargar la llave secreta
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configurar la IA
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No hay archivo"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre vacío"}), 400

    # 1. Leer el PDF
    pdf_text = extract_text_from_pdf(file)

    # 2. Instrucciones para Gemini (Prompt del Sistema)
    prompt = f"""
    Actúa como un motor de videojuegos RPG. Analiza el siguiente texto educativo y genera un nivel de juego.
    
    TEXTO DEL PDF:
    {pdf_text[:10000]}  # Limitamos a 10000 caracteres por seguridad
    
    TU TAREA:
    Responde ÚNICAMENTE con un JSON válido (sin explicaciones extra) que tenga esta estructura exacta:
    {{
        "world_name": "Nombre creativo del mundo basado en el tema",
        "enemies": [
            {{
                "name": "Nombre del enemigo (concepto clave)",
                "visual_desc": "Descripción visual para pixel art",
                "questions": [
                    {{
                        "q": "Pregunta sobre el concepto",
                        "options": ["Opción A", "Opción B", "Opción C", "Opción D"],
                        "correct": 0  
                    }}
                ]
            }}
        ]
    }}
    (Genera al menos 3 enemigos).
    """

    # 3. Enviar a Gemini
    try:
        response = model.generate_content(prompt)
        # Limpiar la respuesta para asegurar que es JSON puro
        json_response = response.text.replace("```json", "").replace("```", "")
        return json_response, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)