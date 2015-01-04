//The user entity of the currently active user
var currentUserEntity;

var setUser = function(response) {
    currentUserEntity = response;
	$(".username").text(currentUserEntity.username);
	$("#logout-url").attr("href", currentUserEntity.logout);
	if (typeof init == 'function') { 
		init();
	}
}

var ajaxFailure = function(data) {
	$('#page-content').prepend(
			'<div id="ajax-alert" role="alert" class="alert alert-danger alert-dismissible fade in">'
	     	+ '<button aria-label="Close" data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span></button>'
	     	+ '<h4>An error occured</h4>'
      		+ '<p>' + data.responseJSON.status + ': ' + data.responseJSON.message + '</p>'
    		+ '<button class="btn btn-danger" onClick="location.reload();" type="button">Refresh</button>'
	    	+ '</div>'
		);
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
		error: function(data) {
			if (typeof error == 'function') { 
 				error(data);
 			}
 		}
	});
};

$( document ).ready(function() {
	getCurrentUser(setUser, ajaxFailure);
});

$(document).on({
    ajaxStart: function() { $("body").addClass("loading"); },
 	ajaxStop: function() { $("body").removeClass("loading"); }
});


