window.addEventListener('DOMContentLoaded', function () {
  const textarea = document.querySelector('#editor-textarea');

  textarea.style.height = textarea.scrollHeight - 24 + 'px';

  textarea.addEventListener('input', function (e) {
    e.preventDefault(); // Prevent page scrolling

    textarea.style.height = 'auto'; /* Reset the height to auto */
    textarea.style.height = (textarea.scrollHeight - 12) + 'px'; /* Set the new height based on content */

    convertToSpan();
  });
});

convertToSpan();

// Get references to HTML elements
const textArea = document.getElementById('editor-textarea');
const labelButton = document.getElementById('labelButton');
const linesElement = document.querySelector('.lines');

// Add event listener to label button
labelButton.addEventListener('click', labelSelectedText);


// Function to get the selected text
function getSelectedText() {
  return textArea.value.substring(textArea.selectionStart, textArea.selectionEnd);
}

// Function to wrap the selected text with a given HTML tag
function wrapSelectionWithTag(tagName, attributes) {
  const selectedText = getSelectedText();

  if (selectedText) {
    const tag = document.createElement(tagName);
    for (const attr in attributes) {
      tag.setAttribute(attr, attributes[attr]);
    }
    const range = getSelectedRange();
    range.surroundContents(tag);
    clearSelection();
  }
}

// Function to get the current selected range
function getSelectedRange() {
  return window.getSelection().getRangeAt(0);
}

// Function to clear the current selection
function clearSelection() {
  window.getSelection().removeAllRanges();
}

// Function to label the selected text
function labelSelectedText() {
  // Prompt the user to enter a label
  const label = prompt('Enter a label for the selected text:');

  if (label) {
    wrapSelectionWithTag('div', { class: 'labeledText', 'data-label': label });
  }

}

function convertToSpan() {
  const textarea = document.getElementById('editor-textarea');
  const targetElement = document.getElementById('listText');

  const textareaContent = textarea.value;

  // Split the content into an array of lines
  const lines = textareaContent.split('\n');

  // Create an array to store the modified HTML for each line
  const linesHTML = [];

  // Loop through the lines
  for (const line of lines) {
    const words = line.split(' ');

    // Create a new array with <span> elements for each word or empty span for multiple white spaces
    const spans = words.map((word) => {
      if (word === '') {
        // Create an empty <span> element for multiple white spaces
        return `<span class='word empty'>&nbsp;</span>`;
      } else {
        // Create a <span> element for the word
        return `<span class='word'>${word}</span>`;
      }
    });

    // Join the array of <span> elements into a single string
    const spansHTML = spans.join(' ');

    // Create a <div> element for the line with the spans
    const lineHTML = `<div class='line'>${spansHTML}</div>`;

    // Push the line HTML to the array
    linesHTML.push(lineHTML);
  }

  // Join the array of line HTML into a single string
  const linesHTMLString = linesHTML.join('');

  // Set the HTML content of the target element with the generated line HTML
  targetElement.innerHTML = linesHTMLString;

  // Attach click event listeners to the spans
  const spanElements = targetElement.getElementsByClassName('word');
  for (let i = 0; i < spanElements.length; i++) {
    spanElements[i].addEventListener('click', handleSelection);
  }
}



// Store the existing highlights
const existingHighlights = new Map();

// Function to update the lines element based on textarea content
function updateLines() {
  const content = textArea.value;
  const lines = content.split('\n');

  textArea.cols = 122;

  // Calculate the number of wrapped lines
  const wrappedLines = lines.reduce((accumulator, line) => {
    const lineLength = Math.ceil(line.length / textArea.cols);
    return accumulator + lineLength;
  }, 0);

  // Generate the line numbers HTML
  const linesHTML = Array.from({ length: wrappedLines }, (_, index) => `<div>${index + 1}</div>`).join('');
  linesElement.innerHTML = linesHTML;

  // Restore existing highlights
  CSS.highlights.clear();
  existingHighlights.forEach((highlight) => {
    CSS.highlights.set("sample", highlight);
  });
}

// Add event listener for textarea input
textArea.addEventListener('input', updateLines);

// Initial update
updateLines();

// Handle the selection event
function handleSelection() {
  var selectedText = window.getSelection().toString().toLowerCase().trim();

  if (selectedText === '')
    return;

  var listText = document.getElementById("listText");
  var spans = listText.getElementsByTagName("span");

  // Create an array to store the matching spans
  var matchingSpans = [];

  // Find the matching spans
  for (var i = 0; i < spans.length; i++) {
    var span = spans[i];
    var spanText = span.textContent.toLowerCase();

    if (spanText === selectedText ) {
      matchingSpans.push(span);
    }
  }

  // Create an array to store the ranges
  var ranges = [];

  // Create ranges for the matching spans
  for (var j = 0; j < matchingSpans.length; j++) {
    var span = matchingSpans[j];
    var range = document.createRange();
    range.selectNode(span);
    ranges.push(range);
  }

  // Create a Highlight object for the ranges
  const highlight = new Highlight(...ranges);

  // Register the Highlight object in the CSS.highlights map
  CSS.highlights.set("sample", highlight);

  // Store the highlight in existingHighlights
  existingHighlights.set("sample", highlight);
}
