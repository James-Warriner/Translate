document.addEventListener("DOMContentLoaded", function () {
  filterDropdown(1);
  filterDropdown(2);

  let mediaRecorder;
  let chunks = [];
  let isRecording = false;

  document.getElementById("record").addEventListener("click", async function () {
    const recordBtn = this;

    if (!isRecording) {
   ///this starts recording
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      chunks = [];

      mediaRecorder.ondataavailable = (e) => chunks.push(e.data);

      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: "audio/webm" });
        const formData = new FormData();
        formData.append("audio", blob, "audio.webm");

        const targetLang = document.getElementById("languageSelect2").value;
        formData.append("target_lang", targetLang);

        const res = await fetch("/speech/translate", {
          method: "POST",
          body: formData,
        });

        const data = await res.json();

        document.getElementById("in").value = data.transcript || "No speech detected";
        document.getElementById("out").value = data.translation || "No translation returned";
      };

      mediaRecorder.start();
      recordBtn.textContent = "Stop Recording";
      isRecording = true;
    } else {
      // this Stops recording
      mediaRecorder.stop();
      recordBtn.textContent = "Start Recording";
      isRecording = false;
    }
  });


});

async function filterDropdown(num) {
  const query = document.getElementById("dropdownSearch" + num).value;

  const res = await fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ q: query }),
  });

  const data = await res.json();

  const select = document.getElementById("languageSelect" + num);
  select.innerHTML = "";

  data.forEach((lang) => {
    const option = document.createElement("option");
    option.value = lang.code;
    option.textContent = lang.language;
    select.appendChild(option);
  });
}