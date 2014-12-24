function ChannelHandler() {
	this.socket = null;
	/*
	 *	Handler function called when channel initially opened
	 */
	this.onOpened = function() {
		//we can now make call to server to get notes json
		if(!ajaxHelper) {
			var ajaxHelper = new AjaxHandler();
		}
		ajaxHelper.getTuneJSON(pageData.songId,function(data) {
			loadNotesFromJSON(data);
		});
		
	}
	this.onMessage = function(message) {
		console.log("message received via channels");
		
		msg = JSON.parse(message.data);
		for(var i = 0; i < msg.length; i++) {
			this.processMessage(msg[i]);
		}
		console.log(msg);
		
	}
	this.onError = function() {

	}
	this.onClose = function() {

	}
	this.initSocket = function(token) {
		channel = new goog.appengine.Channel(token);
		console.log(channel);
	    this.socket = channel.open();
		this.socket.onopen = this.onOpened;
		this.socket.onmessage = this.onMessage;
		this.socket.onerror = this.onError;
		this.socket.onclose = this.onClose;
	}

	this.processMessage = function(msg) {
		//split this up based on what type of message we receive
		for(var i = 0; i < pageData.quarantinedChanges.length; i++) {
			if(msg.actionId && pageData.quarantinedChanges[i].actionId === msg.actionId) {
				quarantinedChanges.splice(i,1);
				return;//remove for change list and return as already done locally
			}
		}
		if(msg.action === 'noteAdd') {
			var track = msg.note.track;
			delete msg.note.track;//we dont want to add the track field into the tune json
			tuneJSON.tracks[track].notes.push(msg.note);//add to tune json
			
			drawNote(msg.note,$('#track' + track));
		} else if(msg.action === 'noteRm') {
			var deletedNote = deleteNote(msg.id);
			$('#' + msg.data.id).remove();
		} else if(msg.action === 'instrumentAdd') {
			addInstrument(msg.instrument.inst,msg.instrument.track);
		} else if(msg.action === 'instrumentRm') {
			deleteInstrument(msg.instrumentTrack,true);
		} else if(msg.action === 'instrumentEdit') {	
			changeInstrument(msg.instrumentNumber,msg.instrumentTrack);
		} else if(msg.action === 'tempo') {
			$('#tempo-select').val(msg.tempo);
		}
	}
}
