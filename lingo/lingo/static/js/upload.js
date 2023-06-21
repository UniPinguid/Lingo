var fileInput = document.getElementById('fileInput');
var fileInputSmall = document.getElementById('fileInputSmall');
var uploadStatus = document.getElementById('uploadStatus');
var uploadBox = document.getElementById('uploadBox');

if (fileInput) {
    fileInput.addEventListener('change', function () {
        handleFileInputChange(fileInput);
    });
}

if (fileInputSmall) {
    fileInputSmall.addEventListener('change', function () {
        handleFileInputChange(fileInputSmall);
    });
}

function handleFileInputChange(inputElement) {
    // Check if a file is selected
    if (inputElement.files.length > 0) {
        var uploadedFile = inputElement.files[0];

        uploadStatus.style.display = "block";
        uploadBox.style.display = "none";
        // Perform further actions with the uploaded file
        // For example, you can display the file name and other details
        uploadStatus.innerHTML =
            "<div style='display: flex; flex-direction: row; gap: 8px; align-items: center; padding-right: 16px'>" +
            "<div class='file-icon'>" +
            "<div class='icon light size48px' id='search'></div>" +
            "</div>" +
            "<div class='uploadedFile'>" +
            "<div id='uploadFileName'>" + uploadedFile.name + "</div>" +
            "<div id='fileSize'>" + formatFileSize(uploadedFile.size) + "</div>" +
            "</div>" +
            "<div style='width:50%'></div>" +
            "<div style='display: flex; align-items: center; float:right;'>" +
            "<button class='button-small' id='uploadButton'>Upload</button>" +
            "<button class='icon' id='closeButton'><div class='icon size32px' id='close'></div></button>" +
            "</div></div>";

        // Attach event listeners to the buttons
        var uploadButton = document.getElementById("uploadButton");
        var closeButton = document.getElementById("closeButton");

        closeButton.addEventListener('click', function () {
            // Hide upload status and show upload box
            uploadStatus.style.display = "none";
            uploadBox.style.display = "flex";
        });

        uploadButton.addEventListener('click', function () {
            // Hide upload status and show upload box
            uploadStatus.style.display = "none";
            uploadBox.style.display = "flex";
        });


    } else {
        // If no file is selected, display an error message
        uploadStatus.style.display = "hidden";
        uploadBox.style.display = "block";
    }
}


function formatFileSize(size) {
    if (size === 0) return '0 Bytes';

    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(size) / Math.log(k));

    return parseFloat((size / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}
