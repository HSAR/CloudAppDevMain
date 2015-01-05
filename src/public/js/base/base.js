//Globals
var currentUserEntity //the current user entity from datastore
var ajax; //ajax handlers for this page

var setUser = function(response) {
    currentUserEntity = response;
	$(".username").text(currentUserEntity.username);
	$("#logout-url").attr("href", currentUserEntity.logout);
	if (typeof init == 'function') { 
		init();
	}
}

var ajaxFailure = function(data) {
	console.log(data);
	console.log(jQuery.parseJSON(data.responseText));
	//sometimes responseJSON is missing - responseText is parsed instead
	if (!data.responseJSON) {
		data.responseJSON = jQuery.parseJSON(data.responseText);
	}

	alertUser('alert-danger', 'Error ' + data.responseJSON.status + ': ' + data.responseJSON.message);
};

var alertUser = function(style, message) {
	$('#page-content').prepend(
        '<div id="ajax-alert" role="alert" class="alert' + style + 'alert-dismissible fade in">'
        + '<button aria-label="Close" data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span></button>'
        + '<p>' + message + '</p>'
        + '</div>'
    );
}

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


