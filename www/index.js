import "./index.css";

import { addCloses, newEntry } from "./sketch";

const HOSTNAME = "http://localhost:5000/";
const inputs = document.getElementsByTagName("input");

document.getElementsByTagName("body")[0].classList.add("show");

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

    const time = 100;
    let transactionId;

    fetch(HOSTNAME + "api/history?source=" + source + "&target=" + target + "&time=" + time)
      .then(response => response.json())
      .then(closes => {
        console.log(closes);
        addCloses(closes);
      });

    fetch(
      HOSTNAME +
        "api/transfer?source=" +
        source +
        "&target=" +
        target +
        "&timeFrame=" +
        inSeconds +
        "&amount=" +
        sourceAmount +
        "&demoMode=true" +
        "&time=" +
        time
    )
      .then(response => response.text())
      .then(data => {
        transactionId = data;
      });

    // addCloses(Array.apply(null, Array(101)).map(() => 50 * Math.random()));

    let c = 50;
    let timeElapsed = 0;
    setInterval(() => {
      timeElapsed += 1;

      fetch(HOSTNAME + "api/demo-update?transferId=" + transactionId + "&timeElapsed=" + timeElapsed)
        .then(response => response.json())
        .then(pair => {
          console.log(pair.price);
          newEntry(pair.price, pair.sellAmount);
        });

      // newEntry(c, c);
      c += 10;
    }, 1000);
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
