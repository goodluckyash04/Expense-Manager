function generateCSV() {
    // Get the table and key elements by their IDs
    var table = document.getElementById("myTable");
    var filename = document.getElementById("key")
    if (filename){
        filename = filename.textContent.trim() + ".csv";
    }else{
        filename = "mhb-report.csv";
    }
    // Initialize an empty array for the CSV content
    var csvRows = [];
  
    // Loop through each row in the table
    for (var i = 0; i < table.rows.length; i++) {
      var row = table.rows[i];
      var rowData = [];
  
      // Loop through each cell in the row
      for (var j = 0; j < row.cells.length; j++) {
        var cell = row.cells[j];
        // Push the cell's text content, escaped for CSV
        rowData.push('"' + cell.textContent.trim().replace(/"/g, '""') + '"');
      }
  
      // Join the row data with commas and add to the csvRows array
      csvRows.push(rowData.join(","));
    }
  
    // Join all rows with newline characters
    var csvContent = csvRows.join("\n");
  
    // Create a Blob with the CSV content
    var blob = new Blob([csvContent], { type: "text/csv" });
  
    // Create a temporary download link for the CSV file
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
  
    // Trigger a click event on the link to initiate the download
    a.click();
  }
  