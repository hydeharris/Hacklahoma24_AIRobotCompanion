document.addEventListener("DOMContentLoaded", function () {
  navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
    handlerFunction(stream);
  });

  function handlerFunction(stream) {
    rec = new MediaRecorder(stream);
    rec.ondataavailable = (e) => {
      audioChunks.push(e.data);
      if (rec.state == "inactive") {
        let blob = new Blob(audioChunks, { type: "audio/mpeg-3" });
        sendData(blob);
      }
    };
  }

  function sendData(data) {
    let formData = new FormData();
    formData.append("audio", data, "recorded-audio.mp3");

    fetch("/upload_audio", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          console.log("Audio uploaded successfully");
        } else {
          console.error("Error uploading audio");
        }
      })
      .catch((error) => {
        console.error("Error uploading audio:", error);
      });
  }

  recording = false;
  recordButton.onclick = (e) => {
    if (recording) {
      recording = false;
      recordButton.innerText = "Record Voice";
      console.log("Endw was record");
      rec.stop();
    } else {
      recording = true;
      console.log("Start was recrod");
      recordButton.innerText = "End Recording";
      audioChunks = [];
      rec.start();
    }
  };
});
