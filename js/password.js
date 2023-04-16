const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirm-password');

// Attach an oninput event listener to both input fields
passwordInput.addEventListener("input", checkPasswordMatch);
confirmPasswordInput.addEventListener("input", checkPasswordMatch);

// Define the checkPasswordMatch function
function checkPasswordMatch() {
    // Get the password and confirm password values
    const passwordValue = passwordInput.value;
    const confirmPasswordValue = confirmPasswordInput.value;

    // Get the "prompt-text" error message element
    const errorElement = document.getElementById("prompt-text");

    // Check if field is empty
    if (passwordValue.length === 0) {
        document.getElementById("prompt-text").innerHTML = "Password cannot be left empty.";
    }
    else if (confirmPasswordValue.length === 0) {
        document.getElementById("prompt-text").innerHTML = "Confirm Password cannot be left empty.";
    }
    // Check if the passwords match
    else if (passwordValue !== confirmPasswordValue) {
        // Show the error message and disable the submit button
        document.getElementById("prompt-text").innerHTML = "Password and confirm password do not match.";
    } else {
        // Hide the error message and enable the submit button
        document.getElementById("prompt-text").innerHTML = "Correct password";


        document.getElementById("prompt-text").innerHTML = checkPasswordStrength(passwordValue);
    }
}

function checkPasswordStrength(password) {
    // Define the regex patterns for various strength requirements
    let patterns = [
        /[a-z]+/, // lowercase letters
        /[A-Z]+/, // uppercase letters
        /[0-9]+/, // numbers
        /[\W_]+/  // special characters
    ];

    // Check if the password meets each pattern requirement
    let strength = 0;
    for (let i = 0; i < patterns.length; i++) {
        if (patterns[i].test(password)) {
            strength++;
        }
    }

    if (password.length < 8) {
        return "Your password is too short. Please make sure it must contain at least 8 characters.";
    }

    displayStrength(strength);

    // Determine the strength level based on the number of met requirements
    switch (strength) {
        case 1:
            return "Your password is too weak.";
        case 2:
            return "Moderate";
        case 3:
            return "Strong";
        case 4:
            return "Very strong";
        default:
            return "Unknown"
    }
}

function displayStrength(strength) {
    switch (strength) {
        case 1:
            {
                document.getElementById("lv1").style.backgroundColor = "#DA2D56";
                break;
            }
        case 2:
            {
                document.getElementById("lv1").style.backgroundColor = "#ffd45e";
                document.getElementById("lv2").style.backgroundColor = "#ffd45e";
                break;
            }
        case 3:
            {
                document.getElementById("lv1").style.backgroundColor = "#bded42";
                document.getElementById("lv2").style.backgroundColor = "#bded42";
                document.getElementById("lv3").style.backgroundColor = "#bded42";
                break;
            }
        case 4:
            {
                document.getElementById("lv1").style.backgroundColor = "#3ac427";
                document.getElementById("lv2").style.backgroundColor = "#3ac427";
                document.getElementById("lv3").style.backgroundColor = "#3ac427";
                document.getElementById("lv4").style.backgroundColor = "#3ac427";
                break;
            }
    }
}