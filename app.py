from flask import Flask, render_template, request, send_file
import tempfile
import os
from TTS.api import TTS

app = Flask(__name__)

# Instancia global del modelo
tts = TTS(model_name="tts_models/en/jenny/jenny", progress_bar=False, gpu=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/synthesize', methods=['POST'])
def synthesize():
    text = request.form['text']
    voice = request.form['voice']
    style = request.form['style']
    is_spanish = voice.startswith("tts_models/es")

    tts_instance = TTS(model_name=voice, progress_bar=False, gpu=False)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as fp:
        if style and style != "default":
            tts_instance.tts_to_file(text=text, file_path=fp.name, speaker_wav=None, style_wav=None, style=style)
        else:
            tts_instance.tts_to_file(text=text, file_path=fp.name)
        return send_file(fp.name, as_attachment=True, download_name="output.wav")

if __name__ == '__main__':
    app.run(debug=True)
