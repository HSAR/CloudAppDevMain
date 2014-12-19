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
	this.onMessage = function(msg) {
		console.log("message received via channels");
		console.log(msg);
		//split this up based on what type of message we receive
		for(var i = 0; i < pageData.quarantinedChanges.length; i++) {
			if(msg.actionId && pageData.quarantinedChanges[i].actionId === msg.actionId) {
				quarantinedChanges.splice(i,1);
				return;//remove for change list and return as already done locally
			}
		}
		if(msg.topic === 'token') {

		} else if(msg.topic === 'add') {
			var tab = $('.tab-pane.active').index();
			tuneJSON.tracks[tab].notes.push(msg.data);
			drawNote(msg.data,$('.tab-pane.active'));
			//probably want to check quarantined changes at this point
			//TODO check for conflicts with local version
		} else if(msg.topic === 'delete') {
			console.log('reached delete case');
			var deletedNote = deleteNote(msg.data.id);
			$('#' + msg.data.id).remove();
			//then check quarantined changes
		}
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
}
