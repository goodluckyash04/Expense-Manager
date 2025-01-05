function openModalAndGetTask(Id) {
     document.getElementById("myTaskForm").action = `/editTask/${Id}`
     document.getElementById("submitbutton").textContent = "Update Task"
     document.getElementById("exampleModalLabel").textContent = "Edit Task"

     fetch(`/editTask/${Id}`)
                .then(response => response.json())
                .then(data => {
                    console.log("data",data)
             // Priority
                    var prioritySelect = document.getElementById("priority");

                    PRIORITY = ['High','Medium','Low']

            prioritySelect.innerHTML = PRIORITY.map(function(priority) {
                return `<option value="${priority}" ${priority === data.priority ? 'selected' : ''}>${priority}</option>`;
            }).join('');

                // name
                document.getElementById("title").value = data.name

                // complete_by_date
                document.getElementById("complete_by").value = data.complete_by_date

                // description
                document.getElementById("descirption").value = data.description

                });
        };