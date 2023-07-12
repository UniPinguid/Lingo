var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (this.classList.contains("active")) {
      content.style.maxHeight = content.scrollHeight + "px";
      content.style.opacity = "1";
      content.style.margin = "0px";
    } else {
      content.style.maxHeight = "0";
      content.style.opacity = "0";
      content.style.margin = "-16px 0px";
    }
  });
}
