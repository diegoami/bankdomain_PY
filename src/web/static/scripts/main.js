select_header = function(element) {
    var topNav_element = document.getElementById(element);
    topNav_element.setAttribute("class", "active");
}





function move_to_page(page_id, form) {
    var mainForm = document.getElementById(form);
    document.getElementById("page_id").value = page_id
    mainForm.target= "";
    mainForm.submit();
}
