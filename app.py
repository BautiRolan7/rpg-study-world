import os
from flask import Flask, render_template
from dotenv import load_dotenv

# Cargar variables de entorno desde .env (si existe localmente)
load_dotenv()
app = Flask(__name__)

# Configuración de Gemini (Placeholder)
gemini_api_key = os.getenv('GEMINI_API_KEY')
print("API Configurada") # Confirmación en consola al iniciar

@app.route('/')
def index():
    # Flask busca automáticamente en la carpeta 'templates'
    return render_template('index.html')

if __name__ == '__main__':
    # debug=True permite ver cambios sin reiniciar manualmente el servidor
    app.run(debug=True)