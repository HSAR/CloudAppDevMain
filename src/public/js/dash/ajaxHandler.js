function AjaxHandler() {

	this.getUserSongs = function(cb, error) {
		commonAjax(requesturls.songs, cb, error);
	}
	
	this.getUserCollabs = function(cb, error) {
		commonAjax(requesturls.collabs, cb, error);
	}

	this.getUserInvites = function(cb, error) {
		commonAjax(requesturls.invites, cb, error);
	}

	var requesturls = { 
		songs: 'http://jinglr-music.appspot.com/api/users/self/songs',
		collabs: 'http://jinglr-music.appspot.com/api/users/self/collabs',
		invites: 'http://jinglr-music.appspot.com/api/users/self/invites' 
	}
}

