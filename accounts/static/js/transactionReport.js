function hiddendiscription(){
    td = document.getElementsByClassName("td-desc")
    th = document.getElementById("th-desc")

    if (td[0].hidden == true && th.hidden==true){
    for(i=0;i<td.length;i++){
        td[i].removeAttribute('hidden')
    }
    th.removeAttribute('hidden')
    }
    else{
     for(i=0;i<td.length;i++){
        td[i].setAttribute('hidden',true)
    }
    th.setAttribute('hidden',true)
    }   
}


    document.getElementById("export-csv-button").addEventListener("click", function () {
      // Get the table element by its ID
      var table = document.getElementById("myTable");
      var cont = document.getElementById("key").textContent;


      // Initialize an empty CSV content
      var csvContent = "";

      // Loop through each row in the table
      for (var i = 0; i < table.rows.length; i++) {
        var row = table.rows[i];

        // Loop through each cell in the row
        for (var j = 0; j < row.cells.length; j++) {
          var cell = row.cells[j];

          // Append the cell's text content to the CSV, enclosed in double quotes
          csvContent += '"' + cell.textContent.trim().replace(/"/g, '""') + '"';

          // Add a comma separator, except for the last cell in the row
          if (j < row.cells.length - 1) {
            csvContent += ",";
          }
        }

        // Add a newline character to separate rows
        csvContent += "\n";
      }

      // Create a Blob with the CSV content
      var blob = new Blob([csvContent], { type: "text/csv" });

      // Create a temporary download link for the CSV file
      var a = document.createElement("a");
      a.href = URL.createObjectURL(blob);
      a.download = `${cont}.csv`;

      // Trigger a click event on the link to initiate the download
      a.click();
    });




  document.getElementById("select-all-checkbox").addEventListener("change", function() {
    var checkboxes = document.getElementsByName("record_ids");
    for (var i = 0; i < checkboxes.length; i++) {
      checkboxes[i].checked = this.checked;
    }
  });

  function reviseTotal(){
    actualTotal = document.getElementById("total")
    console.log(actualTotal.textContent)
    newValue = document.getElementById("select")

    console.log(newValue.parentElement.parentElement.children[4])

  }
