let keyInput;
const dataRowClass = ".data-row";
const dataInputClass = ".input";
const dataOutputClass = ".output";

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("form").addEventListener("change", () => {
    generateHMAC();
    updateUrlPath();
  });

  keyInput = document.getElementById("keyInput");
  const urlParams = new URLSearchParams(window.location.search);
  const key = urlParams.get("key");
  const moves = urlParams.get("messages");

  if (key) keyInput.value = key;

  if (moves) {
    moves.split(",").forEach((move, i) => {
      i && duplicateElement();
      const row = document.querySelectorAll(dataRowClass)[i];
      row.querySelector(dataInputClass).value = move;
    });
  }

  generateHMAC();
});

function duplicateElement() {
  const original = document.querySelector(`${dataRowClass}:last-child`);
  const clone = original.cloneNode(true);
  original.parentNode.appendChild(clone);
}

function generateHMAC() {
  const key = keyInput.value;
  var hmac = CryptoJS.algo.HMAC.create(CryptoJS.algo.SHA256, key);

  const rows = document.querySelectorAll(dataRowClass);
  rows.forEach((row) => {
    hmac.reset();
    const input = row.querySelector(dataInputClass);
    hmac.update(input.value);

    const output = row.querySelector(dataOutputClass);
    output.value = hmac.finalize();
  });
}

function updateUrlPath() {
  let messages = Array.from(document.querySelectorAll(dataInputClass))
    .map((element) => element.value)
    .join();

  let url = new URL(window.location.href);
  url.searchParams.set("key", keyInput.value);
  url.searchParams.set("messages", messages);

  history.replaceState(null, null, url.href);
}

function findNode(element) {
  let parent = element.parentNode;
  if (parent.classList.contains("data-row")) return parent;
  return findNode(parent);
}

function deleteRow(e) {
  if (document.querySelectorAll(dataRowClass).length === 1) return;
  findNode(e.target).remove();

  updateUrlPath();
}
