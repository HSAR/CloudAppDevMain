function AjaxHandler() {
	//yet more code repetition - this really could be one function...

	this.getUserSongs = function(cb) {
		commonAjax(requesturls.songs, cb);
	}
	
	this.getUserCollabs = function(cb) {
		commonAjax(requesturls.collabs, cb);
	}

	this.getUserInvites = function(cb) {
		commonAjax(requesturls.invites, cb);
	}
}

var requesturls = { 
	songs: 'http://jinglr-music.appspot.com/users/' + currentUserEntity.user_id + '/songs',
	collabs: 'http://jinglr-music.appspot.com/users/' + currentUserEntity.user_id + '/collabs',
	invites: 'http://jinglr-music.appspot.com/users/' + currentUserEntity.user_id + '/invites' 
}

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