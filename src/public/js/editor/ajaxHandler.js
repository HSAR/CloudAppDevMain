function AjaxHandler() {
	this.handleError = function() {
		if(!channelHelper) {
			channelHelper = new ChannelHandler();
		}
		channelHelper.onError();//call channel error function to deal with loss of conneciton
	}

	this.getToken = function(id,cb) {
		$.ajax({
			type : 'GET',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id + '/token',
			dataType : 'JSON',
			success : function(data) {
				console.log(data);
				if(data.token) {
					console.log('token retreived via ajax');
					//we can now open up a socket using the token
					cb(data.token);
				} else {
					//deal with error here
				}
			},
			error : this.handleError

		});
	};
	this.getTuneJSON = function(id,cb) {
		$.ajax({
			type : 'GET',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id,
			dataType : 'JSON',
			success : function(data) {
				console.log(data);
				if(data) {
					$('.song-title').html(data.title);
					//we can now open up a socket using the token
					cb(data.jingle);
				} else {
					//deal with error here
				}
			},
			error : this.handleError
		});
	};
	
	this.addNote = function(id,msg) {
		msg.action = 'noteAdd';
		console.log(msg);
		$.ajax({
			type : 'PUT',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id + '/notes',
			data : JSON.stringify(msg),
			dataType : 'JSON',
			error : this.handleError
		});
	};
	this.deleteNote = function(id,msg) {
		console.log(msg);
		$.ajax({
			type : 'DELETE',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id + '/notes?actionId=' + msg.actionId +
			'&track=' + msg.trackId + '&noteId=' + msg.noteId,
			error : this.handleError
		});
	};
	this.compileTune = function(id,cb) {
		//asks the server to compile the tune into a midi file and send it back
		$.ajax({
			type : 'GET',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id + '/midi',
			success : function(data) {
				if(true) {
					//TODO add some file validation here
					cb(JSON.parse(data));
				} else {
					//deal with error here
				}
			},
			error : this.handleError
		});
	};

	this.changeInstrument = function(id,msg) {
		msg.action = 'instrumentEdit';
		$.ajax({
			type : 'PATCH',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id + '/instruments',
			data  : JSON.stringify(msg),
			success : function() {
				//TODO
			},
			error : this.handleError
		});
	}

	this.addInstrument = function(id,msg) {
		msg.action = 'instrumentAdd';

		$.ajax({
			type : 'PUT',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id + '/instruments',
			data  : JSON.stringify(msg),
			success : function() {
				//TODO
			},
			error : this.handleError
		});
	}

	this.deleteInstrument = function(id,msg) {
		console.log(msg);
		$.ajax({
			type : 'DELETE',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id + '/instruments?action=instrumentRm&actionId=' +
			msg.actionId + '&instrumentTrack=' + msg.instrumentTrack,
			error : this.handleError
		});
	}

	this.changeTempo = function(id,msg) {
		msg.action = "tempo";
		$.ajax({
			type : 'PUT',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id + '/tempo',
			data : JSON.stringify(msg),
			error : this.handleError
		});
	}

	this.sendInvite = function(id,uid,error) {
		$.ajax({
			url : window.location.protocol + '//' + window.location.host + '/api/users/' + uid + '/invites/' + id,
			type : 'PUT',
<<<<<<< HEAD
			error : function(err) {
				alertUser('alert-danger',err);
=======
			error: function(data) {
				error(data);
>>>>>>> 446f29e915d31efbc622e9399f57b91eee96e879
			}
		});
	}

	this.getUsers = function(id) {
		$.ajax({
			type : 'GET',
			url : window.location.protocol + '//' + window.location.host + '/api/users',
			success : function(data) {
				pageData.users = JSON.parse(data);
			}
		});
	}

}
