function AjaxHandler() {
	this.getUser = function(path, cb) {
		commonAjax('http://jinglr-music.appspot.com/' + path + '/json', cb);
	}

	this.getUserSongs = function(path, cb) {
		commonAjax('http://jinglr-music.appspot.com/' + path + '/songs', cb);
	}
	
	this.getUserCollabs = function(path, cb) {
		commonAjax('http://jinglr-music.appspot.com/' + path + '/collabs', cb);
	}
}