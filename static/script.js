// Define the classify function
function classify() {
    var textInput = document.getElementById("textInput").value;
    var fileInput = document.getElementById("fileInput").value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/classify", true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function() {
        if (xhr.readyState == XMLHttpRequest.DONE) {
            if (xhr.status == 200) {
                document.getElementById("output").innerText = xhr.responseText;
                // Clear input fields after classification
                document.getElementById("textInput").value = "";
                document.getElementById("fileInput").value = "";
            } else {
                console.error('Error:', xhr.status);
            }
        }
    }
    xhr.send("textInput=" + textInput);
}

// Wait for the DOM to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
    // Attach the classify function to the button click event
    document.getElementById("classifyButton").addEventListener("click", classify);
});
