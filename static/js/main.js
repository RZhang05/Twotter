let userList = $('#user-list');
let chatInput = $('#chat-message-input');
let chatButton = $('#chat-message-submit');
let messageList = $('#chat-log');
let targetuser_img = '';

function updateUserList() {
    $.getJSON(window.location.origin + '/api/user/', function (data) {
        userList.children('.user').remove();
        for (let i = 0; i < data.length; i++) {
            let userItem = `<a class="list-group-item user">${data[i]['username']}</a>`;
			if (data[i]['username'] == receiver) {
    			$.getJSON(window.location.origin + `/api/user/?target=${receiver}`, function (data) {
					targetuser_img = data[0]['user_img']+'';	
				});
				setReceiver(receiver);
            	userItem = `<a class="list-group-item user active">${data[i]['username']}</a>`;
			}
            $(userItem).appendTo('#user-list');
        }
        $('.user').click(function () {
    		$.getJSON(window.location.origin + `/api/user/?target=${receiver}`, function (data) {
				targetuser_img = data[0]['user_img']+'';	
			});
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
			setReceiver(selected.text);
        });
    });
}

function addMessage(message) {
	let pos = 'left';
	let user_img = targetuser_img;
	const date = new Date(message.timestamp);
	if(message.sender === currentUser) {
		pos = 'right';
		user_img = userimg;
	}
	const messageItem = `
		<div class = 'container ${pos}'>
			<img src='${user_img}'>	
			<div class = "text_container">
				<p> ${message.body} </p>
				<span class='time'>${date}</span>
			</div>
		</div>`;
	$(messageItem).appendTo('#chat-log');
}

function getMessages(receiver) {
	$.getJSON(`/api/message/?target=${receiver}`, function (data) {
		messageList.children('.container').remove();
        for (let i = 0; i < data.length; i++) {
            	addMessage(data[i]);
        }
		messageList.animate({
			scrollTop: messageList.prop('scrollHeight') - messageList.prop('clientHeight')
		}, 500);
    });
}

function getMessageById(message) {
	id = JSON.parse(message).message;
	$.getJSON(`/api/message/${id}/`, function (data) {
        if (data.receiver === receiver ||
		(data.receiver === receiver && data.sender == currentUser)) {
			addMessage(data);
        }
		messageList.animate({
			scrollTop: messageList.prop('scrollHeight') - messageList.prop('clientHeight')
		}, 500);
    });
}

function sendMessage(receiver, body) {
	$.post('/api/message/', {
        	receiver: receiver,
        	body: body
	})
}

function setReceiver(username) {
	receiver = username;
	getMessages(receiver);
	enableInput();
}

function enableInput() {
	chatInput.prop('disabled', false);
	chatButton.prop('disabled', false);
	chatInput.focus();
}

function disableInput() {
	chatInput.prop('disabled', true);
	chatButton.prop('disabled', true);
}

$(document).ready(function () {
	updateUserList();
	disableInput();
	
	var socket = new WebSocket(
        'wss://' + window.location.host +
        '/ws?session_key=${sessionKey}')
	
	chatInput.keypress(function (e) {
		if (e.keyCode == 13) chatButton.click();
	});

	chatButton.click(function () {
		if (chatInput.val().length > 0) {
			sendMessage(receiver, chatInput.val());
			chatInput.val('');
		}
	});
	
	socket.onmessage = function (e) {
		getMessageById(e.data);
	};
});
