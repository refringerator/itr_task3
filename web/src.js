document.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("addButton")
    .addEventListener("click", duplicateElement);

  document.getElementById("form").addEventListener("change", () => {
    generateHMAC();
    updateUrlPath();
  });

  const keyInput = document.getElementById("keyInput");
  const dataRowClass = ".data-row";
  const dataInputClass = ".input";
  const dataOutputClass = ".output";

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

  function duplicateElement() {
    const original = document.querySelector(`${dataRowClass}:last-child`);
    const clone = original.cloneNode(true);
    original.parentNode.appendChild(clone);
  }

  function updateUrlPath() {
    let rows = Array.from(document.querySelectorAll(dataInputClass))
      .map((e) => e.value)
      .join();
    const key = keyInput.value;

    let url = new URL(window.location.href);
    url.searchParams.set("key", key);
    url.searchParams.set("messages", rows);

    history.replaceState(null, null, url.href);
  }

  generateHMAC();
});
