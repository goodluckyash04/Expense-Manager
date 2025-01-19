 function openModalAndGetLedger(Id) {
     document.getElementById("myLedgerForm").action = `/update-ledger-transaction/${Id}`
     document.getElementById("submitButton").textContent = "Update"

     fetch(`/update-ledger-transaction/${Id}`)
                .then(response => response.json())
                .then(data => {
                    console.log("data",data)
                document.getElementById("tname").textContent = `Edit ${data.transaction_type}`

                 // type
                if (data.transaction_type == 'Receivable'){
                    document.getElementById("receivable").checked = true
                }else if (data.transaction_type == 'Payable'){
                    document.getElementById("payable").checked = true
                } else if (data.transaction_type == 'Received'){
                    document.getElementById("received").checked = true
                }else{
                    document.getElementById("paid").checked = true
                }

                // Counterparty
                document.getElementById("counterparty").style.display = 'none'
                document.getElementById("counterparty").required = false

                // no_of_installments
                document.getElementById("no_of_installments").style.display = 'none'

                // transaction_date
                document.getElementById("transaction_date").value = data.transaction_date

                 // amount
                document.getElementById("amount").value = data.amount

                // description
                document.getElementById("description").textContent = data.description

                });
        };