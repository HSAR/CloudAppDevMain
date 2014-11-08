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
		ajaxHelper.getTuneJSON(function(data) {
			loadNotesFromJSON(data);
		});
		
	}
	this.onMessage = function(msg) {
		//split this up based on what type of message we receive
		if(msg.topic = 'token') {

		} else if(msg.topic = '') {
			
		}
	}
	this.onError = function() {

	}
	this.onClose = function() {

	}
	this.initSocket = function(token) {
		channel = new goog.appengine.Channel(token);
	    this.socket = channel.open();
		this.socket.onopen = this.onOpened;
		this.socket.onmessage = this.onMessage;
		this.socket.onerror = this.onError;
		this.socket.onclose = this.onClose;
	}
}
