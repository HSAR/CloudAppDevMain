//The user entity of the currently active user
var currentUserEntity = null;

var setUser = function(response) {
    currentUserEntity = response;
	if(!currentUserEntity) {
		connectionFailureMessage();
	} else {
		$(".username").text(currentUserEntity.username);
		init();
	}

};

var connectionFailureMessage = function() {
	$('#connection-failure-modal').modal('show');
	$('#connection-failure-button').click(function() {
		location.reload();
	})  
};

var getCurrentUser = function(cb) {
	commonAjax('http://jinglr-music.appspot.com/api/users/self', cb);
};

var commonAjax = function(url, cb) {
	$.ajax({
		type : 'GET',
		url : url,
		dataType  : 'JSON',
		success : function(data) {
			if (data) {
				cb(data);
			} else {
				//connectionFailureMessage();
				getCurrentUser(setUser);
			}
		}
		//failure: connectionFailureMessage()
	});
};

$( document ).ready(function() {
	getCurrentUser(setUser);
});

$(document).on({
    ajaxStart: function() { $("body").addClass("loading"); },
 	ajaxStop: function() { $("body").removeClass("loading"); }
});


