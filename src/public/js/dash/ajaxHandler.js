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

	this.createJingle = function(title, genre, tags, cb) {
		$.ajax({
			type : 'PUT',
			url : window.location.protocol + '//' + window.location.host + '/api/songs',
			data : JSON.stringify({ title: title, genre: genre, tags: tags }),
			dataType  : 'JSON',
			complete : cb
		});
	}

	this.respondToInvite = function(jingleId, response, cb, error) {
		$.ajax({
			type : 'DELETE',
			url : window.location.protocol + '//' + window.location.host + '/api/users/self/invites/' + jingleId + '?response=' + response,
			success : function(data) {
				cb(data);
			}
		});
	}

	var requesturls = { 
		songs: window.location.protocol + '//' + window.location.host + '/api/users/self/songs',
		collabs: window.location.protocol + '//' + window.location.host + '/api/users/self/collabs',
		invites: window.location.protocol + '//' + window.location.host + '/api/users/self/invites' 
	}
}

