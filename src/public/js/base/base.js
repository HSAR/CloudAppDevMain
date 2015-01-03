//The user entity of the currently active user
var currentUserEntity = null;

var setUser = function(response) {
    currentUserEntity = response;
	if(!currentUserEntity) {
		connectionFailureMessage();
	} else {
		$(".username").text(currentUserEntity.username);
		if (typeof init == 'function') { 
 			init();
 		}
	}

};

var connectionFailure = function() {
	$('#connection-failure-modal').modal('show');
	$('#connection-failure-button').click(function() {
		location.reload();
	})  
};

var getCurrentUser = function(cb, error) {
	commonAjax(window.location.protocol + '//' + window.location.host + '/api/users/self', cb, error);
};

var commonAjax = function(url, cb, error) {
	$.ajax({
		type : 'GET',
		url : url,
		dataType  : 'JSON',
		success : function(data) {
			cb(data);
		},
		error: function() {
			if (typeof error == 'function') { 
 				error(null);
 			}
 		}
	});
};

$( document ).ready(function() {
	getCurrentUser(setUser, connectionFailure);
});

$(document).on({
    ajaxStart: function() { $("body").addClass("loading"); },
 	ajaxStop: function() { $("body").removeClass("loading"); }
});


