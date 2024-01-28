// Establish SocketIO connection with the server
// const socket = io.connect("http://127.0.0.1:5000");

// Listen for 'download_progress' events emitted by the server
// socket.on("download_progress", (data) => {
//   const progress = data.progress;
//   // Update the UI with the download progress
//   document.getElementById(
//     "progress"
//   ).innerText = `Download Progress: ${progress.toFixed(2)}%`;
// });

// Function that Checks Link, if it's a youtube Link
function isYouTubeLink(link) {
  // Regular expression to match YouTube video URLs
  let youtubeRegex =
    /^(http(s)?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]{11}$/;

  // Test if the link matches the YouTube URL pattern
  return youtubeRegex.test(link);
}

let downloadButton = document.getElementById("downloadButton");
let body = document.querySelector("body");

downloadButton.addEventListener("click", (e) => {
  e.preventDefault();

  let inputField = document.getElementById("myInputField");
  let videoLink = inputField.value;

  if (videoLink === "") {
    let fieldEmptyDiv = document.createElement("div");
    fieldEmptyDiv.setAttribute("class", "warning");
    fieldEmptyDiv.textContent = "This Input Link field is empty";
    body.appendChild(fieldEmptyDiv);
  } else if (isYouTubeLink(videoLink) === false) {
    let linkErrorDiv = document.createElement("div");
    linkErrorDiv.setAttribute("class", "warning");
    linkErrorDiv.textContent = "This is not a youtube link";
    body.appendChild(linkErrorDiv);
  } else {
    isYouTubeLink(videoLink);
    // Initiate the download process if it's a valid YouTube link
    console.log(videoLink);

    const socket = new WebSocket("http://127.0.0.1:5000");

    socket.onopen = function (event) {
      console.log("WebSocket connection opened:", event);
    };

    socket.onmessage = function (event) {
      const data = JSON.parse(event.data);
      console.log("Received data from server:", data);
      // Process the data as needed
    };

    // socket.emit("start_download", { videoLink: videoLink });
  }
});
