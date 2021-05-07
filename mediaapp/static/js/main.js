let userList = $('#user-list');

function updateUserList() {
    $.getJSON(window.location.origin + '/api/user/', function (data) {
        userList.children('.user').remove();
        for (let i = 0; i < data.length; i++) {
            const userItem = `<a class="list-group-item user">${data[i]['username']}</a>`;
            $(userItem).appendTo('#user-list');
        }
        $('.user').click(function () {
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
        });
    });
}

$(document).ready(function () {
    updateUserList();
});
