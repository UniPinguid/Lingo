const searchBar = document.getElementById('search-bar');
const suggestionsDropdown = document.getElementById('suggestionsDropdown');

// Event listener for input on the search bar
searchBar.addEventListener('input', handleSearchInput);

// Handle search input
function handleSearchInput() {
    const searchText = searchBar.value.trim();

    // Get search suggestions based on the input
    const suggestions = getSearchSuggestions(searchText);

    // Render the suggestions in the dropdown
    renderSuggestions(suggestions);
}

// Function to get search suggestions (replace with your own logic)
function getSearchSuggestions(searchText) {
    // Simulated data source
    const data = ['apple', 'banana', 'orange', 'pineapple'];

    // Filter suggestions based on input
    return data.filter(item => item.toLowerCase().startsWith(searchText));
}

// Function to render the suggestions in the dropdown
function renderSuggestions(suggestions) {
    if (suggestions.length === 0) {
        suggestionsDropdown.style.display = 'none';
        return;
    }

    const dropdownHTML = suggestions
        .map(suggestion => `<div class="dropdown-item"><div class="avatar"><img src="/static/images/sample avatar.png" style="width:24px"></div>${suggestion}</div>`)
        .join('');

    suggestionsDropdown.innerHTML = dropdownHTML;
    suggestionsDropdown.style.display = 'block';
}

// Hide the dropdown when clicking outside of it
document.addEventListener('click', function (event) {
    if (!event.target.closest('.search-container')) {
        suggestionsDropdown.style.display = 'none';
    }
});

// Handle suggestion selection
suggestionsDropdown.addEventListener('click', function (event) {
    const selectedSuggestion = event.target.textContent;
    searchBar.value = selectedSuggestion;
    suggestionsDropdown.style.display = 'none';
});
