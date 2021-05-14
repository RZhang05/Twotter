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
				follow(targetUser);
			} else {
				unfollow(existingFollow.id);
			}
		});
    });
}

function follow(subject) {
	$.post('/api/follow/', {
        subject:subject
	}, function(){window.location.href=window.location.href;} )
}

function unfollow(id) {
	$.ajax({
		url:`/api/follow/${id}/`,
		type: 'DELETE',
		success: function(){window.location.href=window.location.href;}
	})
}

$(document).ready(function () {
	createButton();
});
