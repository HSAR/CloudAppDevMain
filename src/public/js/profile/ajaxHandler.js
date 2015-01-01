function AjaxHandler() {
	this.getUser = function(path, cb) {
		commonAjax('http://jinglr-music.appspot.com/api/users/' + path + '/json', cb);
	}

	this.getUserSongs = function(path, cb) {
		commonAjax('http://jinglr-music.appspot.com/api/users/' + path + '/songs', cb);
	}
	
	this.getUserCollabs = function(path, cb) {
		commonAjax('http://jinglr-music.appspot.com/api/users/' + path + '/collabs', cb);
	}

	this.updateProfile = function(uid, username, bio, tags, cb) {
		$.ajax({
		type : 'PATCH',
		url : 'http://jinglr-music.appspot.com/api/users/' + uid,
		data : { bio: bio, tags: tags, username: username},
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
}