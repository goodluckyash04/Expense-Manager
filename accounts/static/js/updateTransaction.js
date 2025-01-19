CATEGORIES = ['Shopping', 'Food', 'Investment', 'Utilities', 'Groceries','Medical', 'General', 'Gifts', 'Entertainment','EMI', 'Other'];
MODE = ['CreditCard' , 'Online', 'Cash']
STATUS = ['Pendiing','Completed']




 function openModalAndGetExpense(Id) {
     document.getElementById("updateExpenseForm").action = `/update-transaction/${Id}`

     fetch(`/update-transaction/${Id}`)
                .then(response => response.json())
                .then(data => {
                    console.log("data",data)
                 // title
                 document.getElementById("title").textContent = `Update ${data.type}`

                    // category
                    var categorySelect = document.getElementById("category");
                if (data.type == "Income"){
                    CATEGORIES = ['Salary','Other']
                }
            categorySelect.innerHTML = CATEGORIES.map(function(category) {
                return `<option value="${category}" ${category === data.category ? 'selected' : ''}>${category}</option>`;
            }).join('');

            // beneficiary
            document.getElementById("beneficiary_data").value = data.beneficiary

                // date
                document.getElementById("date").value = data.date

                // amount
                document.getElementById("amount").value = data.amount

                // description
                document.getElementById("description").value = data.description

                // mode_detail
                document.getElementById("mode_detail").value = data.mode_detail

                // mode
                 var modeSelect = document.getElementById("mode");
            modeSelect.innerHTML = MODE.map(function(mode) {
                return `<option value="${mode}" ${mode === data.mode ? 'selected' : ''}>${mode}</option>`;
            }).join('');



                });
        };




















































//function beneficiary(){
//    var pay = document.getElementById("payment_for")
//    var other = document.getElementById("payment_for_text")
//
//    if (pay.value == "Other"){
//        pay.removeAttribute("name")
//        other.setAttribute("name","payment_for")
//        other.removeAttribute('style')
//    }else{
//        other.removeAttribute("name")
//        other.style.display= "none"
//        pay.setAttribute("name","payment_for")
//    }
//}
//
//function loanCategory(){
//var selectedValue = document.getElementById("category")
//var btn = document.getElementById("submitButton")
//var desc = document.getElementById("description")
//var p_for = document.getElementById("payment_for")
//var loan = document.getElementById("loan_name")
//
//if (selectedValue.value == "Loan"){
//    btn.textContent = "Convert To EMI"
//    desc.placeholder = "No. of EMIS"
//    desc.type = "number"
//    p_for.style.display = "none"
//    loan.removeAttribute("style")
//}else{
//    btn.textContent = "Add"
//    desc.placeholder = "Expense Description"
//    desc.type = "text"
//    p_for.removeAttribute('style')
//    loan.style.display = "none"
//}
//}
//
//
//function payType(){
//var Expense = document.getElementById("Expense")
//var category = document.getElementById("category")
//var Income = document.getElementById("Income")
//var Loan = document.getElementById("Loan")
//var Payment_for = document.getElementById("payment_for")
//
//if (Income.checked){
//    category.removeAttribute('style')
//
//    category.options[1].text = "Salary"
//    category.options[1].value = "Salary"
//    category.options[3].style.display="none"
//    category.options[4].style.display="none"
//
//    Payment_for.options[3].setAttribute('selected',true)
//    Payment_for.setAttribute('disabled',true)
//
//} else if(Expense.checked) {
//    category.removeAttribute('style')
//
//    category.options[1].text = "Loan"
//    category.options[1].value = "M_Loan"
//    category.options[3].removeAttribute('style')
//    category.options[4].removeAttribute('style')
//    Payment_for.options[3].removeAttribute('style')
//    Payment_for.options[4].removeAttribute('style')
//
//    Payment_for.options[3].removeAttribute('selected')
//    Payment_for.removeAttribute('disabled')
//
//} else if(Loan.checked){
//    category.options[1].value = "Loan"
//    category.style.display="none"
//    Payment_for.options[3].removeAttribute('selected')
//    Payment_for.removeAttribute('disabled')
//    Payment_for.options[3].style.display="none"
//    Payment_for.options[4].style.display="none"
//
//}
//}
//
//function payment(){
//    console.log("hello")
//    var pay = document.getElementById("payment_for")
//    var other = document.getElementById("payment_for_text")
//    if (pay.value == "Other"){
//      pay.removeAttribute("name")
//      other.setAttribute("name","payment_for")
//      other.removeAttribute('style')
//  }else{
//      other.removeAttribute("name")
//      other.style.display= "none"
//      pay.setAttribute("name","payment_for")
//  }
//  }
//
//
//function onloadPaymentType(){
//    payment()
//
//    var category = document.getElementById("category")
//    var Income = document.getElementById("Income")
//    var Loan = document.getElementById("Loan")
//    var Payment_for = document.getElementById("payment_for")
//
//    if (Income.checked){
//        category.options[1].text = "Salary"
//        category.options[1].value = "Salary"
//        category.options[3].style.display="none"
//        category.options[4].style.display="none"
//
//    } else if(Loan.checked){
//        category.options[1].value = "Loan"
//        category.style.display="none"
//        Payment_for.options[3].style.display="none"
//        Payment_for.options[4].style.display="none"
//
//    }
//
//  }
//
//
////   window.onload = payment;
//  window.onload = onloadPaymentType;
//
//
//

























