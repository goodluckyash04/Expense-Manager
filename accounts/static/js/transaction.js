CATEGORIES = [
  "Shopping",
  "Food",
  "Investment",
  "Utilities",
  "Groceries",
  "Medical",
  "Generals",
  "Gifts",
  "Entertainment",
  "EMI",
  "Other",
];
MODE = ["CreditCard", "Online", "Cash"];
STATUS = ["Pendiing", "Completed"];

const getCurrentDate = () => new Date().toISOString().split("T")[0];

function getTransactionDetail(Id) {
  document.getElementById(
    "editTransactionForm"
  ).action = `/update-transaction/${Id}`;

  fetch(`/update-transaction/${Id}`)
    .then((response) => response.json())
    .then((data) => {
      // title
      document.getElementById("title").textContent = `${data.type}`;

      document.getElementById(
        "submitButton"
      ).textContent = `Update ${data.type}`;

      // category
      var categorySelect = document.getElementById("category");
      if (data.type == "Income") {
        CATEGORIES = ["Salary", "Other"];
      }
      categorySelect.innerHTML = CATEGORIES.map(function (category) {
        return `<option value="${category}" ${category === data.category ? "selected" : ""}>${category}</option>`;
      }).join("");

      // beneficiary
      document.getElementById("beneficiary_data").value = data.beneficiary;

      // date
      document.getElementById("date").value = data.date;

      // amount
      document.getElementById("amount").value = data.amount;

      // description
      document.getElementById("description").value = data.description;

      // mode_detail
      document.getElementById("mode_detail").value = data.mode_detail;

      // mode
      var modeSelect = document.getElementById("mode");
      modeSelect.innerHTML = MODE.map(function (mode) {
        return `<option value="${mode}" ${mode === data.mode ? "selected" : ""}>${mode}</option>`;
      }).join("");
    });
}

function transactionType() {
  document.getElementById("transactionBody").removeAttribute("style");
  document.getElementById("date").value = getCurrentDate();

  var submit_button = document.getElementById("submitButton");
  var categorySelect = document.getElementById("category");
  var beneficiary = document.getElementById("add_beneficiary");
  var other = document.getElementById("beneficiary_text");
  var mode = document.getElementById("mode");
  var mode_detail = document.getElementById("mode_detail");
  var status = document.getElementById("status");

  // Default values
  submit_button.textContent = "Add Income";
  beneficiary.style.display = "none";
  other.style.display = "none";
  mode.style.display = "none";
  mode_detail.style.display = "none";
  status.style.display = "none";

  if (Expense.checked) {
    submit_button.textContent = "Add Expense";

    beneficiary.style.display = "";
    mode.style.display = "";
    mode_detail.style.display = "";
    status.style.display = "";
  }

  if (Income.checked) {
    CATEGORIES = ["Salary", "Other"];
  }
  // Update category options
  categorySelect.innerHTML = CATEGORIES.filter((category) => category != "EMI")
    .map((category) => `<option value="${category}">${category}</option>`)
    .join("");
}

if (document.getElementById("add_beneficiary")) {
  document
    .getElementById("add_beneficiary")
    .addEventListener("change", beneficiary);
}

function beneficiary() {
  var bene = document.getElementById("add_beneficiary");
  var other_bene = document.getElementById("other_beneficiary");
  var other_input = document.getElementById("beneficiary_text");
  other_input.removeAttribute("style");
  if (bene.value == "Other") {
    bene.removeAttribute("name");
    other_input.setAttribute("name", "beneficiary");
    other_bene.removeAttribute("style");
    console.log(other_bene);
  } else {
    other_bene.style.display = "none";
    other_input.removeAttribute("name");
    bene.setAttribute("name", "beneficiary");
    console.log(other_bene);
  }
}

function hiddendiscription() {
  td = document.getElementsByClassName("td-desc");
  th = document.getElementById("th-desc");

  if (td[0].hidden == true && th.hidden == true) {
    for (i = 0; i < td.length; i++) {
      td[i].removeAttribute("hidden");
    }
    th.removeAttribute("hidden");
  } else {
    for (i = 0; i < td.length; i++) {
      td[i].setAttribute("hidden", true);
    }
    th.setAttribute("hidden", true);
  }
}
