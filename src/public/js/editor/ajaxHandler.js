/**
Handler class responsible for carrying out ajax calls required by the editor
*/
function AjaxHandler() {
	this.handleError = function() {
		if(!channelHelper) {
			channelHelper = new ChannelHandler();
		}
		channelHelper.onError();//call channel error function to deal with loss of conneciton
	};

	this.getToken = function(id,cb) {
		$.ajax({
			type : 'GET',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id + '/token',
			dataType : 'JSON',
			success : function(data) {
				if(data.token) {
					//we can now open up a socket using the token
					cb(data.token);
				} else {
					this.handleError();
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
				if(data) {
					$('.song-title').html(data.title);
					//we can now open up a socket using the token
					cb(data.jingle);
				} else {
					this.handleError();
				}
			},
			error : this.handleError
		});
	};
	
	this.addNote = function(id,msg) {
		msg.action = 'noteAdd';
		$.ajax({
			type : 'PUT',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id + '/notes',
			data : JSON.stringify(msg),
			dataType : 'JSON',
			error : this.handleError
		});
	};
	this.deleteNote = function(id,msg) {
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
				cb(JSON.parse(data));
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
			},
			error : this.handleError
		});
	};

	this.addInstrument = function(id,msg) {
		msg.action = 'instrumentAdd';

		$.ajax({
			type : 'PUT',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id + '/instruments',
			data  : JSON.stringify(msg),
			error : this.handleError
		});
	};

	this.deleteInstrument = function(id,msg) {
		$.ajax({
			type : 'DELETE',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id + '/instruments?action=instrumentRm&actionId=' +
			msg.actionId + '&instrumentTrack=' + msg.instrumentTrack,
			error : this.handleError
		});
	};

	this.changeTempo = function(id,msg) {
		msg.action = "tempo";
		$.ajax({
			type : 'PUT',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/' + id + '/tempo',
			data : JSON.stringify(msg),
			error : this.handleError
		});
	};

	this.sendInvite = function(id,uid,error) {
		$.ajax({
			url : window.location.protocol + '//' + window.location.host + '/api/users/' + uid + '/invites/' + id,
			type : 'PUT',
			error: function(data) {
				error(data);
			}
		});
	};

	this.getUsers = function(id) {
		$.ajax({
			type : 'GET',
			url : window.location.protocol + '//' + window.location.host + '/api/users',
			success : function(data) {
				pageData.users = JSON.parse(data);
			}
		});
	};
	this.downloadMidi = function(id) {
		//pseudo ajax call
		var currentPath = window.location.pathname;
		window.location.pathname = '/api/songs/' + id + '/file';//download midi file
		window.history.replaceState('Object', 'Title', currentPath);//replace download url in bar with the original url
	}

}
