import "./index.css";

import "./sketch";

document.getElementById("submit").addEventListener("click", e => {
  e.preventDefault();
  document.getElementById("setup").classList.add("hide");
});

const inputs = document.getElementsByTagName("input");

document.addEventListener("keypress", e => {
  e.preventDefault();
  const key = e.which || event.keyCode;

  if (key >= 48 && key <= 57) {
    for (let i = 0; i < inputs.length - 1; i++) {
      inputs[i].value = inputs[i + 1].value;
    }

    inputs[inputs.length - 1].value = String.fromCharCode(e.which);
  }
});
