async function playAudio() {
  const text = document.getElementById("text-input").value;
  const voice_en = document.getElementById("voice-en").value;
  const voice_es = document.getElementById("voice-es").value;

  document.getElementById("loading").style.display = "block";

  const res = await fetch("/synthesize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, voice_en, voice_es })
  });

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);

  const audio = document.getElementById("audio-player");
  audio.src = url;
  audio.style.display = "block";
  document.getElementById("loading").style.display = "none";
  audio.play();
}

async function downloadAudio() {
  const text = document.getElementById("text-input").value;
  const voice_en = document.getElementById("voice-en").value;
  const voice_es = document.getElementById("voice-es").value;

  document.getElementById("loading").style.display = "block";

  const res = await fetch("/synthesize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, voice_en, voice_es })
  });

  const blob = await res.blob();
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "tts_output.mp3";
  link.click();
  document.getElementById("loading").style.display = "none";
}

async function previewVoice(lang) {
  const voice = document.getElementById(lang === "en" ? "voice-en" : "voice-es").value;

  const res = await fetch("/preview", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ voice, lang })
  });

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);

  const audio = new Audio(url);
  audio.play();
}
