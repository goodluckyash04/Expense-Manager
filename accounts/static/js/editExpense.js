function paymentFor(){
    var pay = document.getElementById("payment_for")
    var other = document.getElementById("payment_for_text")

    if (pay.value == "Other"){
        pay.removeAttribute("name")
        other.setAttribute("name","payment_for")
        other.removeAttribute('style')
    }else{
        other.removeAttribute("name")
        other.style.display= "none"
        pay.setAttribute("name","payment_for")
    }
}

function loanCategory(){
var selectedValue = document.getElementById("category")
var btn = document.getElementById("submitButton")
var desc = document.getElementById("description")
var p_for = document.getElementById("payment_for")
var loan = document.getElementById("loan_name")

if (selectedValue.value == "Loan"){
    btn.textContent = "Convert To EMI"
    desc.placeholder = "No. of EMIS"
    desc.type = "number"
    p_for.style.display = "none"
    loan.removeAttribute("style")
}else{
    btn.textContent = "Add"
    desc.placeholder = "Expense Description"
    desc.type = "text"
    p_for.removeAttribute('style')
    loan.style.display = "none"
}
}


function payType(){
var Expense = document.getElementById("Expense")
var category = document.getElementById("category")
var Income = document.getElementById("Income")
var Loan = document.getElementById("Loan")
var Payment_for = document.getElementById("payment_for")

if (Income.checked){
    category.removeAttribute('style')

    category.options[1].text = "Salary"
    category.options[1].value = "Salary"
    category.options[3].style.display="none"
    category.options[4].style.display="none"
    
    Payment_for.options[3].setAttribute('selected',true)
    Payment_for.setAttribute('disabled',true)

} else if(Expense.checked) {
    category.removeAttribute('style')

    category.options[1].text = "Loan"
    category.options[1].value = "M_Loan"
    category.options[3].removeAttribute('style')
    category.options[4].removeAttribute('style')
    Payment_for.options[3].removeAttribute('style')
    Payment_for.options[4].removeAttribute('style')

    Payment_for.options[3].removeAttribute('selected')
    Payment_for.removeAttribute('disabled')

} else if(Loan.checked){
    category.options[1].value = "Loan"
    category.style.display="none"
    Payment_for.options[3].removeAttribute('selected')
    Payment_for.removeAttribute('disabled')
    Payment_for.options[3].style.display="none"
    Payment_for.options[4].style.display="none"

}
}

function payment(){
    console.log("hello")
    var pay = document.getElementById("payment_for")
    var other = document.getElementById("payment_for_text")
    if (pay.value == "Other"){
      pay.removeAttribute("name")
      other.setAttribute("name","payment_for")
      other.removeAttribute('style')
  }else{
      other.removeAttribute("name")
      other.style.display= "none"
      pay.setAttribute("name","payment_for")
  }
  }


function onloadPaymentType(){
    payment()

    var category = document.getElementById("category")
    var Income = document.getElementById("Income")
    var Loan = document.getElementById("Loan")
    var Payment_for = document.getElementById("payment_for")

    if (Income.checked){
        category.options[1].text = "Salary"
        category.options[1].value = "Salary"
        category.options[3].style.display="none"
        category.options[4].style.display="none"

    } else if(Loan.checked){
        category.options[1].value = "Loan"
        category.style.display="none"
        Payment_for.options[3].style.display="none"
        Payment_for.options[4].style.display="none"

    }

  }


//   window.onload = payment;
  window.onload = onloadPaymentType;



