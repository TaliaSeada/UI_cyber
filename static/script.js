document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('classificationForm');
    const output = document.getElementById('output');
    const textInput = document.getElementById('textInput');
    const fileInput = document.getElementById('fileInput');

    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission behavior

        // Create FormData object to send form data asynchronously
        const formData = new FormData(form);

        // Check if file input has a value
        if (fileInput.value) {
            // Send the form data to the server using fetch API
            fetch('/classify', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(result => {
                // Update the content of the output box with the classification result
                output.textContent = result;

                // Clear input fields after classification
                textInput.value = "";
                fileInput.value = ""; // Reset the file input field value
            })
            .catch(error => {
                // Handle errors if any
                console.error('Error:', error);
            });
        } else {
            // If no file is selected, submit the form without sending the file
            fetch('/classify', {
                method: 'POST',
                body: formData
            })
            .then(response => response.text())
            .then(result => {
                // Update the content of the output box with the classification result
                output.textContent = result;

                // Clear input fields after classification
                textInput.value = "";
                fileInput.value = ""; // Reset the file input field value
            })
            .catch(error => {
                // Handle errors if any
                console.error('Error:', error);
            });
        }
    });
});
