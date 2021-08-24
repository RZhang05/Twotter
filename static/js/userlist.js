let userList = $('#user-list');

function updateUserList() {
    $.getJSON(window.location.origin + '/api/user/', function (data) {
        userList.children('.user').remove();
        for (let i = 0; i < data.length; i++) {
			let uname = data[i]['username'];
			const userItem = `<a href="${window.location.origin}/profile/${uname}/">${uname}</a><br>`;
            $(userItem).appendTo('#user-list');
        }
    });
}


$(document).ready(function () {
	updateUserList();
});
