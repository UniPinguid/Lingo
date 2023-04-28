function addDaySuffix(day) {
    if (day % 10 === 1 && day !== 11) {
      return day + 'st';
    } else if (day % 10 === 2 && day !== 12) {
      return day + 'nd';
    } else if (day % 10 === 3 && day !== 13) {
      return day + 'rd';
    } else {
      return day + 'th';
    }
  }
  
  const today = new Date();
  const dayWithSuffix = addDaySuffix(today.getDate());
  const options = { month: 'long', day: 'numeric', year: 'numeric' };
  const formattedDate = today.toLocaleDateString('en-US', options);
  
  document.write(formattedDate.replace(/(\d+)(st|nd|rd|th)/, dayWithSuffix));