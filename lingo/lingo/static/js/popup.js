var popupButton = document.getElementById('popupButton');
var popup = document.getElementById('popup');
var closeButton = [document.getElementById('closeButton'), document.getElementById('ghost')];
var submitButton = document.getElementById('submitButton');

popupButton.addEventListener('click', function() {
  popup.style.display = 'block';
  document.body.classList.add('popup-lock');
});

closeButton.forEach(function(element)
{ element.addEventListener('click', function() {
  popup.style.display = 'none';
  document.body.classList.remove('popup-lock');
})});

// submitButton.addEventListener('click', function() {
//   popup.style.display = 'none';
//   document.body.classList.remove('popup-lock');
// });