function myFunction() {
  var x = document.getElementById("topnav");
  console.log(document.getElementById("topnav").clientHeight);
  if (x.className === "topnav") {
    x.className += " responsive";
    document.getElementById("spacer").style.height = "5px";
  } else {
    x.className = "topnav";
    var height = document.getElementById("topnav").clientHeight + 10;
    document.getElementById("spacer").style.height = height + "px";
  }
  console.log(document.getElementById("topnav").clientHeight);
}
var height = document.getElementById("topnav").clientHeight + 10;
document.getElementById("spacer").style.height = height + "px";
window.addEventListener("resize", setCalendarLocation);
function setCalendarLocation() {
  var height = document.getElementById("topnav").clientHeight + 10;
  document.getElementById("spacer").style.height = height + "px";
}
