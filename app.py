from flask import Flask, request, jsonify, send_file
from tts import generate_tts
import os
import uuid

app = Flask(__name__)

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    text = data.get("text")
    voice = data.get("voice")
    style = data.get("style")
    lang = data.get("lang")

    if not text or not voice:
        return jsonify({"error": "Missing text or voice"}), 400

    filename = f"output_{uuid.uuid4().hex}.wav"
    path = generate_tts(text=text, voice=voice, style=style, lang=lang, filename=filename)

    return send_file(path, as_attachment=True)

# 🔧 Esto permite que Render detecte y use el puerto asignado
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
