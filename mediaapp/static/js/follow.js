let placeholder = $('#follow-button');
let existingFollow;

function createButton() {
    $.getJSON(window.location.origin + `/api/follow/?target=${targetUser}`, function (data) {
		let button = `<a class = "follow-button">Follow</a>`;
		if(data.length>0) {	
			existingFollow = data[0];
            button = `<a class = "follow-button">Unfollow</a>`;	
		}
		$(button).appendTo('#follow-button');
		$('.follow-button').click(function() {
			let selected = event.target;
			if(selected.text=="Follow") {
				selected.text="Unfollow";
				follow(targetUser);
			}
			else {
				selected.text="Follow";
				unfollow(existingFollow.id);
			}
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
		url:`/api/follow/${id}`,
		type: 'DELETE'				
	})
}

$(document).ready(function () {
	createButton();
});
