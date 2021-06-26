let placeholder = $('#follow-button');
let follower = $('#follower');
let following = $('#following');
let existingFollow;

function updateFollow() {
	$.getJSON(`/api/follow/?req=followers&target=${targetUser}`, function(data) {
		follower.text(data.length)
	});	
	$.getJSON(`/api/follow/?req=following&target=${targetUser}`, function(data) {
		following.text(data.length)
	});
}

function changeText() {
	$.getJSON(window.location.origin + `/api/follow/?target=${targetUser}`, function (data) {
		let but = $('#folbut');
		but.text('Follow');
		if(data.length>0) {	
			existingFollow = data[0];
			but.text('Unfollow');
		}
	});
}

function createButton() {
	$.getJSON(window.location.origin + `/api/follow/?target=${targetUser}`, function (data) {
		let button = `<a class = "follow-button" id="folbut">Follow</a>`;
		if(data.length>0) {	
			existingFollow = data[0];
            button = `<a class = "follow-button" id="folbut">Unfollow</a>`;	
		}
		$(button).appendTo('#follow-button');
		$('.follow-button').click(function() {
			let selected = event.target;
			if(selected.text=="Follow") {
				follow(targetUser);
			} else {
				unfollow(existingFollow.id);
			}
			updateFollow();
			changeText();
		});	
    });
}

function follow(subject) {
	$.post('/api/follow/', {
        subject:subject
	})
}

function unfollow(id) {
	$.ajax({
		url:`/api/follow/${id}/`,
		type: 'DELETE'
	})
}

$(document).ready(function () {
	createButton();
	updateFollow();
});
