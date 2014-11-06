function initSocket(token) {
	channel = new goog.appengine.Channel(token);
    socket = channel.open();
	socket.onopen = onOpened;
	socket.onmessage = onMessage;
	socket.onerror = onError;
	socket.onclose = onClose;

	
}

/*
 *	Handler function called when channel initially opened
 */
function onOpened() {
	//we can now make call to server to get notes json
	$.ajax({
		type : 'GET',
		url : 'http://example.com',
		dataType : 'JSON',
		success : function(data) {
			if(data.topic === 'tune') {
				//we can now open up a socket using the token
				loadNotesFromJSON(data);
				loadPalette();
			} else {
				//deal with error here
			}
		}
	});
}

function onMessage(msg) {
	//split this up based on what type of message we receive
	if(msg.topic = 'token') {

	} else if(msg.topic = '') {
		
	}
}

function onError() {

}

function onClose() {

}