//The user entity of the currently active user
var currentUserEntity = null;

var setUser = function(response) {
	var data = jQuery.parseJSON(response);
	if (!data) {
        data = {username: "testuserplsignore", user_id: "testuidplsignore" }; //test case
    } 
    currentUserEntity = data;
}

var getCurrentUser = function(cb) {
	commonAjax('http://jinglr-music.appspot.com/users/self/', cb);
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
	$("#userWelcome").text(currentUserEntity.username);
});

$body = $("body");

$(document).on({
    ajaxStart: function() { $body.addClass("loading");    },
 	ajaxStop: function() { $body.removeClass("loading"); }    
});


