select_header = function(element) {
    var topNav_element = document.getElementById(element);
    topNav_element.setAttribute("class", "active");
}


random_question = function(form) {
    var mainForm = document.getElementById(form);
    mainForm.action = '/bankdomain/random_questions_submit';
    mainForm.submit();
}


function move_to_page(page_id, form) {
    var mainForm = document.getElementById(form);
    document.getElementById("page_id").value = page_id
    mainForm.target= "";
    mainForm.submit();
}

find_similar = function(question) {
    var mainForm = document.getElementById('question_form');
    document.getElementById("question").value = question;
    mainForm.method="POST";
    mainForm.submit();
}
