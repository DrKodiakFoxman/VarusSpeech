document.getElementById("speechForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  formData.append("voice_en", document.getElementById("voice_en").value);
  formData.append("voice_es", document.getElementById("voice_es").value);

  const audio = document.getElementById("audio");
  const download = document.getElementById("download");

  const btn = form.querySelector("button[type='submit']");
  btn.textContent = "Procesando...";

  const res = await fetch("/speak", {
    method: "POST",
    body: formData
  });

  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  audio.src = url;
  audio.style.display = "block";
  download.href = url;
  download.style.display = "inline-block";

  btn.textContent = "🔊 Reproducir";
});

function testVoice(lang) {
  const voice = document.getElementById(`voice_${lang}`).value;
  const audio = new Audio();
  const sample = lang === "es" ? "Hola, ¿cómo estás?" : "Hello, how are you?";
  alert(`Esta función será agregada pronto. Voz seleccionada: ${voice}`);
}
