window.addEventListener('DOMContentLoaded', function () {
  const textarea = document.querySelector('#editor');
  
  textarea.style.height = textarea.scrollHeight -24 + 'px';

  textarea.addEventListener('input', function (e) {
    e.preventDefault(); // Prevent page scrolling

    textarea.style.height = 'auto'; /* Reset the height to auto */
    textarea.style.height = (textarea.scrollHeight - 24) + 'px'; /* Set the new height based on content */

  });
});

// Get references to HTML elements
const textArea = document.getElementById('editor');
const labelButton = document.getElementById('labelButton');

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
    wrapSelectionWithTag('span', { class: 'labeledText', 'data-label': label });
  }
  
}

