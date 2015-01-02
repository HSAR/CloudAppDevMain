function AjaxHandler() {
	this.getUser = function(path, cb, error) {
		commonAjax('http://jinglr-music.appspot.com/api/users/' + path, cb, error);
	};

	this.getUserSongs = function(path, cb, error) {
		commonAjax('http://jinglr-music.appspot.com/api/users/' + path + '/songs', cb, error);
	};
	
	this.getUserCollabs = function(path, cb, error) {
		commonAjax('http://jinglr-music.appspot.com/api/users/' + path + '/collabs', cb, error);
	};

	this.updateProfile = function(uid, username, bio, tags, cb, error) {
		$.ajax({
			type : 'PATCH',
			url : 'http://jinglr-music.appspot.com/api/users/' + uid,
			data : { bio: bio, tags: tags, username: username},
			dataType  : 'JSON',
			success : function(data) {
				cb(data);
			},
			error : error(null)
		});
	}
}