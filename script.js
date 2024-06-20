function toggleLED(state) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/led?state=" + state, true);
  xhttp.send();
}

