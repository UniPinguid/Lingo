// get the current date
// let today = new Date();

// get the current month and year
let currentDate = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();

function changeMonth(e) {
  if (e.target.id === 'prev' || e.target.id === 'arrow-left') {
    currentDate.setMonth(currentDate.getMonth() - 1);
  } else if (e.target.id === 'next' || e.target.id === 'arrow-right') {
    currentDate.setMonth(currentDate.getMonth() + 1);
  }
  renderCalendar(currentDate);
}

function renderCalendar(date) {
  const currentDate = new Date(date);
  const monthYear = document.getElementById('month-year');
  monthYear.textContent = `${currentDate.toLocaleString('en-US', { month: 'long' })} ${currentDate.getFullYear()}`;
  
  const datesContainer = document.querySelector('.dates');
  datesContainer.innerHTML = '';

  const prevMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1);
  const nextMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1);

  const firstDayIndex = currentDate.getDay();
  const lastDayIndex = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDay();
  const lastDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();
  
  for (let i = firstDayIndex - 1; i >= 0; i--) {
    const date = new Date(prevMonth.getFullYear(), prevMonth.getMonth(), prevMonth.getDate() - i);
    const dateElement = createDateElement(date);
    dateElement.id = "outside";
    datesContainer.appendChild(dateElement);
  }

  for (let i = 1; i <= lastDayOfMonth; i++) {
    const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), i);
    const dateElement = createDateElement(date);
    datesContainer.appendChild(dateElement);
  }

  for (let i = 1; i < 7 - lastDayIndex; i++) {
    const date = new Date(nextMonth.getFullYear(), nextMonth.getMonth(), i);
    const dateElement = createDateElement(date);
    dateElement.id = "outside";
    datesContainer.appendChild(dateElement);
  }
}

function createDateElement(date, className) {
  const dateElement = document.createElement('button');
  dateElement.classList.add('date');
  if (className) {
    dateElement.classList.add(className);
  }
  if (date.toDateString() === new Date().toDateString()) {
    dateElement.id = "today";
  }
  dateElement.textContent = date.getDate();
  return dateElement;
}

renderCalendar(new Date());


const prevBtn = document.getElementById('prev');
prevBtn.addEventListener('click', changeMonth);
const nextBtn = document.getElementById('next');
nextBtn.addEventListener('click', changeMonth);