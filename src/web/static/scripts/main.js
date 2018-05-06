
function move_to_page(page_id, form) {
    var mainForm = document.getElementById(form);
    document.getElementById("page_id").value = page_id
    mainForm.target= "";
    mainForm.submit();
}
