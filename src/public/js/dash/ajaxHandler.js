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

	this.createJingle = function(title, genre, tags, cb, error) {
		$.ajax({
			type : 'PUT',
			url : 'http://jinglr-music.appspot.com/api/songs',
			data : { title: title, genre: genre, tags: tags },
			dataType  : 'JSON',
			success : function(data) {
				cb(data);
			},
			error : error(null)
		});
	}

	var requesturls = { 
		songs: 'http://jinglr-music.appspot.com/api/users/self/songs',
		collabs: 'http://jinglr-music.appspot.com/api/users/self/collabs',
		invites: 'http://jinglr-music.appspot.com/api/users/self/invites' 
	}
}

