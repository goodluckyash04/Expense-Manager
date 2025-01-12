let CATEGORY
// Get the current date and time in ISO format (YYYY-MM-DD)
var currentDate = new Date().toISOString().split('T')[0]

document.getElementById('beneficiary').addEventListener('change', beneficiary);

function beneficiary() {
    var bene = document.getElementById("beneficiary");
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


function payType() {
    document.getElementById("transactionBody").removeAttribute('style')
    document.getElementById("date").value = currentDate

    var submit_button = document.getElementById("submitButton");
    var categorySelect = document.getElementById("category");
    var beneficiary = document.getElementById("beneficiary");
    var other = document.getElementById("beneficiary_text");
    var mode = document.getElementById("mode");
    var mode_detail = document.getElementById("mode_detail");
    var status = document.getElementById("status");

    // Default values
    submit_button.textContent = "Add Income";
    var categories = ['Salary', 'Other'];
    beneficiary.style.display = 'none';
    other.style.display = 'none';
    mode.style.display = 'none';
    mode_detail.style.display = 'none';
    status.style.display = 'none';

    if (Expense.checked) {
        submit_button.textContent = "Add Expense";
        categories = ['Shopping', 'Food', 'Investment', 'Utilities', 'Groceries','Medical', 'General', 'Gifts', 'Entertainment', 'Other'];
        beneficiary.style.display = '';
        mode.style.display = '';
        mode_detail.style.display = '';
        status.style.display = '';
    }

    // Update category options
    categorySelect.innerHTML = categories.map(function(category) {
        return `<option value="${category}">${category}</option>`;
    }).join('');
}










