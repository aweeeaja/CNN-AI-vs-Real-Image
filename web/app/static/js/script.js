document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("file-input");
    const imagePreview = document.getElementById("image-preview");
    const form = document.getElementById("single-upload-form");
    const loadingScreen = document.getElementById("loading-screen");

    // Preview image
    fileInput.addEventListener("change", (event) => {
        const files = event.target.files;
        imagePreview.innerHTML = ""; // Clear previous previews
        if (files.length > 0) {
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
        } else {
            imagePreview.innerHTML = "<p>No image selected</p>";
        }
    });

    // Show loading screen on form submit
    form.addEventListener("submit", () => {
        loadingScreen.style.display = "flex";
    });
});
