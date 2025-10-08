document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("multi-file-input");
    const imagePreview = document.getElementById("multi-image-preview");
    const form = document.getElementById("multi-upload-form");
    const loadingScreen = document.getElementById("loading-screen");
    const submitButton = document.getElementById("submit-button");

    // Create validation message
    const validationMessage = document.createElement("p");
    validationMessage.className = "validation-message";
    validationMessage.innerText = "Please upload at least two images.";
    form.insertBefore(validationMessage, submitButton);

    // Preview multiple images and validate
    fileInput.addEventListener("change", (event) => {
        const files = event.target.files;
        imagePreview.innerHTML = ""; // Clear previous previews

        if (files.length > 1) {
            Array.from(files).forEach((file) => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const img = document.createElement("img");
                    img.src = e.target.result;
                    img.alt = "Selected Image";
                    img.style.maxWidth = "100px";
                    img.style.margin = "5px";
                    imagePreview.appendChild(img);
                };
                reader.readAsDataURL(file);
            });

            // Enable submit button and hide validation message
            submitButton.disabled = false;
            validationMessage.style.display = "none";
        } else {
            imagePreview.innerHTML = "<p>No images selected</p>";
            submitButton.disabled = true;
            validationMessage.style.display = "block";
        }
    });

    // Show loading screen on form submit
    form.addEventListener("submit", () => {
        loadingScreen.style.display = "flex";
    });
});
