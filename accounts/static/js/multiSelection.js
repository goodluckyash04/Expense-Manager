  // Select All Checkboxes Logic
  document.getElementById("select-all-checkbox").addEventListener("change", function() {
    const checkboxes = document.querySelectorAll('input[name="record_ids"]');
    checkboxes.forEach(checkbox => checkbox.checked = this.checked);
  });