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
			url : 'http://jinglr-music.appspot.com/songs/' + id,
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
			data : msg,
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

	this.changeInstrument = function(id,data) {
		$.ajax({
			type : 'PATCH',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/instruments',
			data  : data,
			success : function() {
				//TODO
			}
		});
	}

	this.addInstrument = function(id,data) {
		$.ajax({
			type : 'PUT',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/instruments',
			data  : data,
			success : function() {
				//TODO
			}
		});
	}

	this.deleteInstrument = function(id,data) {
		$.ajax({
			type : 'DELETE',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/instruments',
			data  : data,
			success : function() {
				//TODO
			}
		});
	}

}