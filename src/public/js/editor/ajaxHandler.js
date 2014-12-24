function AjaxHandler() {
	this.getToken = function(id,cb) {
		$.ajax({
			type : 'GET',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/token',
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
			}

		});
	};
	this.getTuneJSON = function(id,cb) {
		$.ajax({
			type : 'GET',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/json',
			dataType : 'JSON',
			success : function(data) {
				console.log(data);
				if(data) {
					//we can now open up a socket using the token
					cb(data);
				} else {
					//deal with error here
				}
			}
		});
	};
	
	this.addNote = function(id,msg) {
		msg.action = 'noteAdd';
		console.log(msg);
		$.ajax({
			type : 'PUT',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/notes',
			data : JSON.stringify(msg),
			dataType : 'JSON'
		});
	};
	this.deleteNote = function(id,msg) {
		console.log(msg);
		$.ajax({
			type : 'DELETE',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/notes?actionId=' + msg.actionId +
			'&track=' + msg.trackId + '&noteId=' + msg.noteId
		});
	};
	this.compileTune = function(id,cb) {
		//asks the server to compile the tune into a midi file and send it back
		$.ajax({
			type : 'GET',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/midi',
			success : function(data) {
				if(true) {
					//TODO add some file validation here
					cb(data);
				} else {
					//deal with error here
				}
			}
		});
	};

	this.changeInstrument = function(id,msg) {
		msg.action = 'instrumentEdit';
		$.ajax({
			type : 'PATCH',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/instruments',
			data  : JSON.stringify(msg),
			success : function() {
				//TODO
			}
		});
	}

	this.addInstrument = function(id,msg) {
		msg.action = 'instrumentAdd';

		$.ajax({
			type : 'PUT',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/instruments',
			data  : JSON.stringify(msg),
			success : function() {
				//TODO
			}
		});
	}

	this.deleteInstrument = function(id,msg) {
		console.log(msg);
		$.ajax({
			type : 'DELETE',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/instruments?action=instrumentRm&actionId=' +
			msg.actionId + '&instrumentTrack=' + msg.instrumentTrack
		});
	}

	this.changeTempo = function(id,msg) {
		msg.action = "tempo";
		$.ajax({
			type : 'PUT',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/tempo',
			data : msg
		});
	}

}