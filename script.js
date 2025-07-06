
function testVoice(lang) {
  alert("Esta función probaría la voz seleccionada para: " + lang);
}

function generateAudio() {
  const loader = document.getElementById("loadingIndicator");
  const audio = document.getElementById("audioPlayer");
  const download = document.getElementById("downloadLink");

  loader.classList.remove("hidden");
  setTimeout(() => {
    loader.classList.add("hidden");
    audio.classList.remove("hidden");
    audio.src = "sample.mp3";
    download.classList.remove("hidden");
    download.href = "sample.mp3";
  }, 3000);
}
