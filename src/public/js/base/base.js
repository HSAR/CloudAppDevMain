//The user entity of the currently active user
var currentUserEntity = null;

var setUserId = function(response) {
	var data = jQuery.parseJSON(response);
	if (!data) {
        data = {uid: "testuidplsignore"}; //test case
    } 
	getUserById(data.uid, setUser);
}

var setUser = function(response) {
	var data = jQuery.parseJSON(response);
	if (!data) {
        data = {username: "testuserplsignore", user_id: "testuidplsignore" }; //test case
    } 
    currentUserEntity = data;
}

var getCurrentUserId = function(cb) {
	commonAjax('http://jinglr-music.appspot.com/uid', cb);
}

var getUserById = function(uid, cb) {
	commonAjax('http://jinglr-music.appspot.com/users/' + uid + "/", cb);
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

getCurrentUserId(setUserId);
$( document ).ready(function() {
	$("#userWelcome").text("Welcome, " + currentUserEntity.username);
});



