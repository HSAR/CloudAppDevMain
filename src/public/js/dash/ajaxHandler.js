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
	songs: 'http://jinglr-music.appspot.com/users/self/songs',
	collabs: 'http://jinglr-music.appspot.com/users/self/collabs',
	invites: 'http://jinglr-music.appspot.com/users/self/invites' 
}