from flask import Flask, request, send_file, render_template
import uuid
import os
import asyncio
from edge_tts import Communicate

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/synthesize", methods=["POST"])
def synthesize():
    data = request.json
    text = data.get("text")
    voice_en = data.get("voice_en", "en-US-JennyNeural")
    voice_es = data.get("voice_es", "es-MX-DaliaNeural")

    if not text:
        return {"error": "No text provided"}, 400

    filename = f"output_{uuid.uuid4().hex}.mp3"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(process_segments(text, voice_en, voice_es, filename))

    return send_file(filename, as_attachment=True, download_name="tts_output.mp3")

@app.route("/preview", methods=["POST"])
def preview():
    data = request.json
    voice = data.get("voice")
    lang = data.get("lang", "en")
    if lang == "en":
        text = "This is a sample of the selected English voice."
    else:
        text = "Esta es una muestra de la voz seleccionada en español."

    filename = f"preview_{uuid.uuid4().hex}.mp3"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(generate_audio(text, voice, filename))

    return send_file(filename, download_name="preview.mp3", mimetype="audio/mpeg")

async def process_segments(text, voice_en, voice_es, output_file):
    import re
    segments = re.split(r"(\[es\].*?\[/es\])", text, flags=re.DOTALL)
    files = []

    for i, segment in enumerate(segments):
        segment = segment.strip()
        if not segment:
            continue

        if segment.startswith("[es]") and segment.endswith("[/es]"):
            clean_text = segment[4:-5].strip()
            voice = voice_es
        else:
            clean_text = segment
            voice = voice_en

        filename = f"seg_{uuid.uuid4().hex}.mp3"
        await generate_audio(clean_text, voice, filename)
        files.append(filename)

    with open(output_file, "wb") as outfile:
        for fname in files:
            with open(fname, "rb") as infile:
                outfile.write(infile.read())
            os.remove(fname)

async def generate_audio(text, voice, filename):
    communicate = Communicate(text, voice=voice)
    await communicate.save(filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
