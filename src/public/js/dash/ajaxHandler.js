function AjaxHandler() {

	this.getUserSongs = function(cb, error) {
		commonAjax(requesturls.songs, cb, error);
	}
	//sort = date_created&descending=true
	
	this.getUserCollabs = function(cb, error) {
		commonAjax(requesturls.collabs, cb, error);
	}

	this.getUserInvites = function(cb, error) {
		commonAjax(requesturls.invites, cb, error);
	}

	this.getLatestSongs = function(cb,error) {
		commonAjax(requesturls.latest,cb,error);
	}

	this.createJingle = function(title, genre, tags, cb, error) {
		$.ajax({
			type : 'PUT',
			url : window.location.protocol + '//' + window.location.host + '/api/songs',
			data : JSON.stringify({ title: title, genre: genre, tags: tags }),
			success : cb,
			error : function(data) {
				error(data);
			}
		});
	}

	this.updateJingle = function(jingle_id,title, genre, tags, cb, error) {
		$.ajax({
			type : 'PATCH',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + jingle_id,
			data : JSON.stringify({title : title, genre : genre, tags : tags}),
			success : cb,
			error : function(data) {
				error(data);
			}
		});
	}

	this.respondToInvite = function(jingleId, response, cb, error) {
		$.ajax({
			type : 'DELETE',
			url : window.location.protocol + '//' + window.location.host + '/api/users/self/invites/' + jingleId + '?response=' + response,
			success : function(data) {
				cb(data);
			},
			error : function(data) {
				error(data);
			}
		});
	}

	var requesturls = { 
		songs: window.location.protocol + '//' + window.location.host + '/api/users/self/songs',
		collabs: window.location.protocol + '//' + window.location.host + '/api/users/self/collabs',
		invites: window.location.protocol + '//' + window.location.host + '/api/users/self/invites',
		latest: window.location.protocol + '//' + window.location.host + '/api/songs/search?sort=date_created&descending=true' 
	}
}

