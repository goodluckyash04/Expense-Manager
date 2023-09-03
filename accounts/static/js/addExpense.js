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
    console.log(selectedValue.name)
    if (selectedValue.value == "M_Loan"){
        btn.textContent = "Convert To EMI"
        desc.placeholder = "No. of EMIS"
        desc.type = "number"
        p_for.style.display = "none"
        loan.removeAttribute("style")
    }else{
        btn.textContent = "Add Expense"
        desc.placeholder = "Expense Description"
        desc.type = "text"
        p_for.removeAttribute('style')
        loan.style.display = "none"
    }
}


  function payType(){
    var data = document.getElementById("data")
    
    if (Income.checked){
        data.innerHTML=`
        <select
        class="form-select mb-3"
        id="category"
        name="category"
        aria-label="Default select example"
        >
        <option selected value="">-- Category --</option>
        <option value="Salary">Salary</option>
        <option value="Personal">Personal</option>
        </select>


        <div class="mb-3">
        <input
            type="datetime-local"
            class="form-control"
            name="payment_date"
            id="payment_date"
            value = ${currentDatetime}
            aria-describedby="emailHelp"
        />
        </div> 


        <div class="mb-3">
        <input
            type="number"
            class="form-control"
            name="amount"
            placeholder="Amount"
            id="amount"
            aria-describedby="emailHelp"
            required
        />
        </div>


        <select
        class="form-select mb-3"
        name="payment_for"
        id = "payment_for"
        aria-label="Default select example"
        onchange="paymentFor()"
        >      
        <option value="Myself" selected>Myself</option>
        
        </select>
        

        <div class="mb-3">
        <input
            type="text"
            class="form-control"
            name="description"
            placeholder="Income Description"
            id="description"
            required
        />
        </div>


        <button
        id = "submitButton"
        type="submit"
        style="background-color: #2b6b32; border: none"
        class="btn btn-primary"
        >
        Add Income
        </button>
        `
    } else if(Expense.checked) {
        data.innerHTML=`
        <select
        class="form-select mb-3"
        id="category"
        name="category"
        onchange="loanCategory()"
        aria-label="Default select example"
        >
        <option selected value="">-- Category --</option>
        <option value="M_Loan">Loan</option>
        <option value="Personal">Personal</option>
        <option value="Food">Food</option>
        <option value="Shopping">Shopping</option>
        </select>


        <div class="mb-3">
        <input
            type="datetime-local"
            class="form-control"
            name="payment_date"
            id="payment_date"
            value = ${currentDatetime}
            aria-describedby="emailHelp"
        />
        </div> 


        <div class="mb-3">
        <input
            type="number"
            class="form-control"
            name="amount"
            placeholder="Amount"
            id="amount"
            aria-describedby="emailHelp"
            required
        />
        </div>


        <select
        class="form-select mb-3"
        name="payment_for"
        id = "payment_for"
        aria-label="Default select example"
        onchange="paymentFor()"
        >
        <option selected>- Payment For -</option>
        <option value="Mom">Mom</option>
        <option value="Dad">Dad</option>
        <option value="Myself">Myself</option>
        <option value="Home">Home</option>
        <option value="Other">Other</option>
        </select>
        
        
        <div class="mb-3">
            <input
                type="text"
                class="form-control"
                name="payment_for"
                style="display: none;"
                id="payment_for_text"
                placeholder="payment_for"
                aria-describedby="emailHelp"
            />
            </div>

        <div class="mb-3">
        <input
            type="text"
            class="form-control"
            name="description"
            placeholder="Expense Description"
            id="description"
            required
        />
        </div>
        
        <div class="mb-3" >
        <input
            type="text"
            class="form-control"
            name="loan_name"
            style="display:none"
            placeholder="Loan Name"
            id="loan_name"
            value=""
        />
        </div>


        <button
        id = "submitButton"
        type="submit"
        style="background-color: #2b6b32; border: none"
        class="btn btn-primary"
        >
        Add Expense
        </button>`

    } else if(Loan.checked){
       data.innerHTML=`
       <select
        class="form-select mb-3"
        id="category"
        name="category"
        aria-label="Default select example"
        >
        <option value="Loan" selected>Loan</option>
       
        </select>
       <div class="mb-3">
       <input
           type="datetime-local"
           class="form-control"
           name="payment_date"
           id="payment_date"
           value = ${currentDatetime}
           aria-describedby="emailHelp"
       />
       </div> 

       <div class="mb-3">
       <input
           type="number"
           class="form-control"
           name="amount"
           placeholder="Amount"
           id="amount"
           aria-describedby="emailHelp"
           required
       />
       </div>


       <select
       class="form-select mb-3"
       name="payment_for"
       id = "payment_for"
       aria-label="Default select example"
       onchange="paymentFor()"
       >
       <option selected>- Payment For -</option>
       <option value="Mom">Mom</option>
       <option value="Dad">Dad</option>
       <option value="Other">Other</option>
       </select>
       
       
       <div class="mb-3">
           <input
               type="text"
               class="form-control"
               name="payment_for"
               style="display: none;"
               id="payment_for_text"
               placeholder="payment_for"
               aria-describedby="emailHelp"
           />
           </div>

       <div class="mb-3">
       <input
           type="text"
           class="form-control"
           name="description"
           placeholder="Loan Description"
           id="description"
           required
       />
       </div>


       <button
       id = "submitButton"
       type="submit"
       style="background-color: #2b6b32; border: none"
       class="btn btn-primary"
       >
       Add Loan
       </button>`
    }
  }

  // Get the current date and time in ISO format (YYYY-MM-DDTHH:MM)
  var tzoffset = (new Date()).getTimezoneOffset() * 60000; //offset in milliseconds
  var currentDatetime = (new Date(Date.now() - tzoffset)).toISOString().slice(0, 16);



