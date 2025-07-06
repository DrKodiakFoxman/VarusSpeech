import os
from flask import Flask, request, send_file, jsonify, render_template
from tts import generate_tts

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    file_path = generate_tts(data['text'], data['voiceEn'], data['styleEn'], data['voiceEs'], data['styleEs'])
    return send_file(file_path, as_attachment=False)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render asigna el puerto en la variable de entorno PORT
    app.run(host='0.0.0.0', port=port)
