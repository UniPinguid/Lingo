var timer;

// Get the toast element
var toast = document.getElementById('toast');

// Get the undo button and add an event listener
var undoButton = document.getElementById('undoButton');
undoButton.addEventListener('click', function () {
    // Undo logic goes here
    // Hide the toast
    toast.classList.remove('show');
});

// Get the close button and add an event listener
var closeButtonPopup = document.getElementById('closeButtonPopup');
closeButtonPopup.addEventListener('click', function () {
    // Hide the toast
    toast.classList.remove('slide-in');
    toast.classList.add('slide-out');
    clearTimeout(timer);
});

// Function to show the toast
function showToast() {
    // Show the toast
    toast.classList.add('show');
    toast.classList.add('slide-in');
    // Set a timeout to hide the toast after a certain duration
    timer = setTimeout(function () {
        toast.classList.remove('slide-in');
        toast.classList.add('slide-out');
    }, 15000); // Adjust the duration as needed (here it's set to 5 seconds)

    toast.classList.remove('slide-out');
}