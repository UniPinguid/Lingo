var fileInput = document.getElementById('fileInput');
var uploadStatus = document.getElementById('uploadStatus');
var uploadBox = document.getElementById('uploadBox');

var uploadButton;
var closeButton;

fileInput.addEventListener('change', function () {
    // Check if a file is selected
    if (fileInput.files.length > 0) {
        var uploadedFile = fileInput.files[0];

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
                "<div style='float:right;'>" +
                    "<a class='button-small' id='uploadButton'>Upload</a>" +
                "</div>" +
                "<div class='icon size32px' id='close'></div>" +
            "</div>";
        // You can also initiate an AJAX request to send the file to the server
        // or perform any other desired actions with the file

        uploadButton = document.getElementById("uploadButton");
        closeButton = document.getElementById("close");
    } else {
        // If no file is selected, display an error message
        uploadStatus.style.display = "hidden";
        uploadBox.style.display = "block";
    }
});

uploadButton.addEventListener('click', function()
{
    
})

function formatFileSize(size) {
    if (size === 0) return '0 Bytes';
  
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(size) / Math.log(k));
  
    return parseFloat((size / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
  