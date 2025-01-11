document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("confirmModal");
  modal.addEventListener("show.bs.modal", function (event) {
    const button = event.relatedTarget;
    const undoUrl = button.getAttribute("data-url");
    const confirmButton = modal.querySelector("#confirmButton");
    confirmButton.setAttribute("href", undoUrl);
  });
});
