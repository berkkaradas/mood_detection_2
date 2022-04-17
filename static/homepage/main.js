var video = document.getElementById('video');
var canvas = document.getElementById('myCanvas');
var context  = canvas.getContext('2d');

// Get access to the camera!
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
    //video.src = window.URL.createObjectURL(stream);
    video.srcObject = stream; // assign stream to <video>
    video.play();             // play stream
    });
}

// Trigger photo take
document.getElementById("snap").addEventListener("click", function() {
context.drawImage(video, 0, 0, 640, 400);  // copy video frame to canvas
});

function DownloadCanvasAsImage(){
    let downloadLink = document.createElement('a');
    downloadLink.setAttribute('download', 'emotion_snapshot.png');
    let canvas = document.getElementById('myCanvas');
    let dataURL = canvas.toDataURL('image/png');
    let url = dataURL.replace(/^data:image\/png/,'data:application/octet-stream');
    downloadLink.setAttribute('href',url);
    downloadLink.click();
}