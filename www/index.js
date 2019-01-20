import "./index.css";

import { newClose } from "./sketch";

const inputs = document.getElementsByTagName("input");

function pad(num, size) {
  var s = "000" + num;
  return s.substr(s.length - size);
}

document.getElementById("submit").addEventListener("click", e => {
  e.preventDefault();

  const dropdowns = document.getElementsByClassName("dropdown");
  const values = document.getElementsByClassName("value");

  document.getElementById("setup").classList.add("hide");

  setTimeout(() => {
    const source = document.getElementById("source").innerHTML;
    const target = document.getElementById("target").innerHTML;

    const inSeconds = 60 * 60 * 24 * 7;
    let sourceAmount = Array.from(inputs)
      .reverse()
      .reduce((accumulator, element, i) => {
        return accumulator + parseInt(element.value) * Math.pow(10, i - 2);
      }, 0);
    let targetAmount = 0;

    for (let i = 0; i < 2; i++) {
      values[i].getElementsByTagName("span")[0].innerHTML =
        pad((i == 0 ? sourceAmount : targetAmount).toFixed(2), 6) +
        " " +
        dropdowns[i].getElementsByTagName("span")[0].innerHTML;
      values[i].getElementsByTagName("img")[0].src = dropdowns[i].getElementsByTagName("img")[0].src;
    }

    document.getElementById("status").classList.add("show");

    // fetch("/api/history?source=" + source + "&target=" + target).then(data => {
    //   const closes = JSON.parse(data);
    //   closes.forEach(close => newClose(parseInt(close)));
    // });

    // fetch(
    //   "/api/transfer?source=" +
    //     source +
    //     "&target=" +
    //     target +
    //     "&timeFrame=" +
    //     inSeconds +
    //     "&amount=" +
    //     sourceAmount +
    //     "&demoMode=true"
    // ).then(data => {
    //   transactionId = data;
    // });

    for (let i = 0; i < 100; i++) {
      newClose(2 * Math.random() - 1, Math.random());
    }

    setInterval(() => {
      // fetch("/api/status?demoMode=true&id=" + transactionId).then(data => {
      //   newClose(parseInt(data));
      // });

      newClose(2 * Math.random() - 1, Math.random());
    }, 5000);
  }, 1000);
});

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

let dropdown;

Array.from(document.getElementsByClassName("dropdown")).forEach(element => {
  element.addEventListener("click", e => {
    e.preventDefault();
    dropdown = element;

    document.getElementById("overlay").classList.add("show");
    document.getElementById("currency").classList.add("show");
  });
});

Array.from(document.getElementsByClassName("dropdown-option")).forEach(element => {
  element.addEventListener("click", e => {
    e.preventDefault();
    dropdown.getElementsByTagName("span")[0].innerHTML = element.getElementsByTagName("span")[0].innerHTML;
    dropdown.getElementsByTagName("img")[0].src = element.getElementsByTagName("img")[0].src;

    document.getElementById("overlay").classList.remove("show");
    document.getElementById("currency").classList.remove("show");
  });
});
