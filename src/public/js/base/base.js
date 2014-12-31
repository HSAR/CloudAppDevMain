//The user entity of the currently active user
var currentUserEntity = null;

var setUser = function(response) {
	var data = jQuery.parseJSON(response);
	if (!data) {
        data = {username: "testuserplsignore", user_id: "testuidplsignore" }; //test case
    } 
    currentUserEntity = data;
}

var connectionFailureMessage = function() {
	$('#connection-failure-modal').modal('show');
	$('#connection-failure-button').click(function() {
		location.reload();
	})  
}

var getCurrentUser = function(cb) {
	commonAjax('http://jinglr-music.appspot.com/api/users/self/', cb);
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
				//#failwhale
			}
		},
		failure : cb(null)
	});
}

getCurrentUser(setUser);
$( document ).ready(function() {
	if(!currentUserEntity) {
		connectionFailureMessage();
	} else {
		$("#userWelcome").text(currentUserEntity.username);
		$("#profile-url").attr("href", "http://jinglr-music.appspot.com/users/self");
	}
});

$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading"); },
 	ajaxStop: function() { $body.removeClass("loading"); }    
});


