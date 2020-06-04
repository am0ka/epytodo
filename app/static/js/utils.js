function logout_button() {
    event.preventDefault();
    document.getElementById("logout-form").submit();
}

function select_all_tasks(source) {
    boxes = document.getElementsByName('done');
    for (var i = 0; i < boxes.length; i++) {
        boxes[i].checked = source.checked;
    }
}