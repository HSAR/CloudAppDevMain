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
}