// Get all the table elements
const tables = document.querySelectorAll('table');

// Iterate over each table
tables.forEach((table, index) => {
  // Get the necessary elements for each table
  const allMemberCheckbox = table.querySelector('#all-member-checkbox');
  const memberCheckboxes = table.querySelectorAll('#member-checkbox');
  const numSelectedElement = document.getElementById(`num-selected-${index + 1}`);

  // Add event listener to the 'all-member-checkbox'
  allMemberCheckbox.addEventListener('change', function() {
    const isChecked = allMemberCheckbox.checked;
    memberCheckboxes.forEach(checkbox => {
      checkbox.checked = isChecked;
    });
    updateNumSelected();
  });

  // Add event listener to each member checkbox
  memberCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
      updateNumSelected();
    });
  });

  // Function to update the number of selected checkboxes
  function updateNumSelected() {
    const numSelected = table.querySelectorAll('#member-checkbox:checked').length;
    numSelectedElement.textContent = `${numSelected} Selected`;
  }
});
