document.addEventListener("DOMContentLoaded", function () {
  var userData = {
    table: [],
  };

  page = 1;

  var nextButton = document.getElementById("nextButton");
  var taskBox = document.getElementById("robotTask");
  var extraBox = document.getElementById("extraInfo");

  var textMode = document.getElementById("textModeButton");
  var audioMode = document.getElementById("audioModeButton");

  var talkBox = document.getElementById("talkBox");
  var talkButton = document.getElementById("talkButton");

  var recordButton = document.getElementById("recordButton");
  textMode.style.display = "none";
  audioMode.style.display = "none";

  extraBox.style.display = "none";
  talkBox.style.display = "none";
  talkButton.style.display = "none";
  recordButton.style.display = "none";
  // Add click event listener to the button
  nextButton.addEventListener("click", function () {
    // Navigate to the next page
    //user.table.push({ task: taskBox.textContent });

    if (page == 1) {
      userData.table.push({ role: taskBox.value });

      document.getElementById("maintext").textContent =
        "Tell me about yourself!\nWhat is your name?";
      extraBox.style.display = "flex";
      taskBox.value = "What is your name?";
      extraBox.value = "What else should I know?";
    } else if (page == 2) {
      userData.table.push({ name: taskBox.value });
      userData.table.push({ extra_info: extraBox.value });

      document.getElementById("maintext").textContent =
        "How will you talk to me?";
      taskBox.style.display = "none";
      extraBox.style.display = "none";
      textMode.style.display = "block";
      audioMode.style.display = "block";
      nextButton.style.display = "none";
    }

    page += 1;
    //window.location.href = "page" + pgNo + ".html"; // Replace 'nextpage.html' with the URL of your next page
  });

  textMode.addEventListener("click", function () {
    textMode.style.display = "none";
    audioMode.style.display = "none";
    document.getElementById("maintext").textContent = "Lets chat...";

    var xhr = new XMLHttpRequest();

    xhr.open("POST", "/process_text", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ background_info: userData.table }));
    talkBox.style.display = "flex";
    talkButton.style.display = "block";
  });
  audioMode.addEventListener("click", function () {
    textMode.style.display = "none";
    audioMode.style.display = "none";
    document.getElementById("maintext").textContent = "Lets chat...";

    var xhr = new XMLHttpRequest();
    userData.table.forEach(function (element, index) {
      // Print each element to the console
      console.log("Element at index " + index + ": ", element);
    });
    xhr.open("POST", "/process_text", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ background_info: userData.table }));
    recordButton.style.display = "block";
    //speechButton.style.display = "block";
  });

  talkButton.addEventListener("click", function () {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/process_talk", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify({ talk_response: talkBox.value }));
    taskBox.value = "";
  });
});
