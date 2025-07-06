
document.getElementById("speechForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = document.getElementById("text").value.trim();
  const language = document.getElementById("language").value;
  const loader = document.getElementById("loader");
  const audio = document.getElementById("audio");

  loader.classList.remove("hidden");
  audio.classList.add("hidden");

  try {
    const res = await fetch("/speak", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, language })
    });

    if (!res.ok) throw new Error("Error al generar el audio");

    const blob = await res.blob();
    audio.src = URL.createObjectURL(blob);
    audio.classList.remove("hidden");
  } catch (err) {
    alert("OcurriÃ³ un error. Intenta de nuevo.");
  } finally {
    loader.classList.add("hidden");
  }
});
