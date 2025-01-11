function openModalAndGetInstrument(Id) {
  document.getElementById(
    "editFinanceForm"
  ).action = `/update-finance-detail/${Id}`;

  fetch(`/update-finance-detail/${Id}`)
    .then((response) => response.json())
    .then((data) => {
      console.log("data", data);
      document.getElementById(
        "title"
      ).textContent = `Edit ${data.type}`;
      document.getElementById(
        "submitButton"
      ).textContent = `Update ${data.type}`;
      console.log(document.getElementById("submitButton"))
      // type
      if (data.type == "Loan") {
        document.getElementById("loan").checked = true;
      } else {
        document.getElementById("sip").checked = true;
      }
      // name
      document.getElementById("name").value = data.name;

      // started_on
      document.getElementById("started_on").value = data.started_on;

      // amount
      document.getElementById("amount").value = data.amount;

      // installments
      document.getElementById("installments").value = data.no_of_installments;
    });
}

document.addEventListener("DOMContentLoaded", function () {
  var currentlyOpenBtn = document.getElementById("currentlyOpenBtn");
  var closedBtn = document.getElementById("closedBtn");

  function updateButtonColors() {
    if (currentlyOpenBtn.getAttribute("aria-expanded") === "true") {
      currentlyOpenBtn.style.backgroundColor = "#f3fcf4";
    } else {
      currentlyOpenBtn.style.backgroundColor = "";
    }

    if (closedBtn.getAttribute("aria-expanded") === "true") {
      closedBtn.style.backgroundColor = "#f8f9f8";
    } else {
      closedBtn.style.backgroundColor = "";
    }
  }

  // Initial call to set the correct colors based on the initial state
  updateButtonColors();

  // Add event listeners to buttons to update colors on collapse toggle
  currentlyOpenBtn.addEventListener("click", function () {
    setTimeout(updateButtonColors, 0); // Timeout to match the collapse animation duration
  });

  closedBtn.addEventListener("click", function () {
    setTimeout(updateButtonColors, 0); // Timeout to match the collapse animation duration
  });
});
