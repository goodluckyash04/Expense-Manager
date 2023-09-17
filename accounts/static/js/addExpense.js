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

    function loanCategory() {
        var categoryValue = document.getElementById("category");
        var btn = document.getElementById("submitButton");
        var desc = document.getElementById("description");
        var p_for = document.getElementById("payment_for");
        var loan = document.getElementById("loan_name");
    
        var isLoanCategory = categoryValue.value === "Loan";
        
        btn.textContent = isLoanCategory ? "Convert To EMI" : "Add Expense";
        desc.placeholder = isLoanCategory ? "No. of EMIs" : "Expense Description";
        desc.type = isLoanCategory ? "number" : "text";
        p_for.style.display = isLoanCategory ? "none" : "";
        loan.style.display = isLoanCategory ? "" : "none";
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
        <option value="Salary">Salary</option>
        <option value="Other">Other</option>
        </select>

        <div class="mb-3">
        <input
            type="text"
            class="form-control"
            name="payment_for"
            readonly
            id="payment_for"
            value = "Myself"
        />
        </div> 

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
        <option value="Shopping">Shopping</option>
        <option value="Food">Food</option>
        <option value="Other">Other</option>
        <option value="Loan">Loan</option>
        </select>

        <select
        class="form-select mb-3"
        name="payment_for"
        id = "payment_for"
        onchange="paymentFor()"
        >
        <option value="Myself" selected >Myself</option>
        <option value="Home">Home</option>
        <option value="Other">Other</option>
        </select>
           
        <div class="mb-3">
            <input
                type="text"
                class="form-control"
                style="display: none;"
                id="payment_for_text"
                placeholder="Payment For"
                aria-describedby="emailHelp"
            />
            </div>

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
        <option value="Debit" >Debit</option>
        <option value="Credit" >Credit</option>
       
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
           type="text"
           class="form-control"
           name="payment_for"
           placeholder="Paid For"
           id="payment_for"
           aria-describedby="emailHelp"
           required
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



