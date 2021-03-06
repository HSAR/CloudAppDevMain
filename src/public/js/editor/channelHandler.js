/**
Handler class which sets up a channel connection with the gae and then handles incoming messages
*/
function ChannelHandler() {
	this.socket = null;
	this.initialLoad = true;//keep track of if this is the intial loading of the page
	var handler = this;//to get hold of handler inside socket scope
	/*
	 *	Handler function called when channel initially opened
	 */
	this.processMessage = function(msg) {
		//split this up based on what type of message we receive
		for(var i = 0; i < pageData.quarantinedChanges.length; i++) {
			if(msg.actionId && pageData.quarantinedChanges[i].actionId === msg.actionId) {
				pageData.quarantinedChanges.splice(i,1);
				return;//remove for change list and return as already done locally
			}
		}
		if(msg.action === 'noteAdd') {
			var track = msg.note.track;
			delete msg.note.track;//we dont want to add the track field into the tune json
			tuneJSON.tracks[track].notes.push(msg.note);//add to tune json
			
			drawNote(msg.note,$('#track' + track));
		} else if(msg.action === 'noteRm') {
			var deletedNote = deleteNote(msg.noteId);
			$('#' + msg.noteId).remove();
		} else if(msg.action === 'instrumentAdd') {
			addInstrument(msg.instrument.inst,msg.instrument.track);
		} else if(msg.action === 'instrumentRm') {
			deleteInstrument(msg.instrumentTrack,true);
		} else if(msg.action === 'instrumentEdit') {	
			changeInstrument(msg.instrumentNumber,msg.instrumentTrack);
		} else if(msg.action === 'tempo') {
			$('#tempo-select').val(msg.tempo);
		}
	};

	this.onOpened = function() {
		//we can now make call to server to get notes json
		if(!handler.initialLoad) {//if page already loaded just call function to reload tune json
			$('.connection-button').addClass('btn-success').removeClass('btn-warning').html('Connected').unbind();
			reloadTune();
			return;
		}
		if(!ajaxHelper) {
			ajaxHelper = new AjaxHandler();
		}
		ajaxHelper.getTuneJSON(pageData.songId,function(data) {
			loadNotesFromJSON(data);
			loadRemainingUI();//load pallette and playback buttons etc
		});
		$('.connection-button').addClass('btn-success').removeClass('btn-warning').html('Connected');
		handler.initialLoad = false;
	};
	this.onMessage = function(message) {
		//first bin any quarantined changes who have been around for more than a set time
		for(var i = 0; i < pageData.quarantinedChanges.length; i++) {
			if(pageData.quarantinedChanges[i].time < Date.now() - 2 * 60 * 1000) { //if over two minutes ago
				pageData.quarantinedChanges.splice(i,1);//remove from list of changes
			}
		}
		
		msg = JSON.parse(message.data);
		var serverChecksum;
		for(var i = 0; i < msg.length; i++) {
			handler.processMessage(msg[i]);
			serverChecksum = msg[i].checksum;//keep updating checksum so that will finish equal to latest one
		}


		//if no quarantined changes compare checksums
		if(pageData.quarantinedChanges.length === 0) {
			if(serverChecksum !== handler.checksum(tuneJSON)) {
				reloadTune();
			}
		}
		
	};
	this.onError = function() {
		try {
			this.socket.close();//if socket not closed, do it now
		} catch(err) {
			//no need to do anything
		}

		//set connection status button
		$('button.connection-button').removeClass('btn-success').addClass('btn-danger').html('Disconnected').unbind().click(function() {
			$('button.connection-button').removeClass('btn-danger').addClass('btn-warning').html('Connecting').unbind();
			getToken();
		});
	};
	this.onClose = function() {
		//socket never closed deliberately, only on error so handled there
	};
	this.initSocket = function(token) {
		this.channel = new goog.appengine.Channel(token);
	    this.socket = this.channel.open({onopen : this.onOpened, onmessage : this.onMessage, onerror : this.onError, onclose : this.onClose});
		
	};

	this.checksum = function(object) {
  	/* Sort the notes */
  	var bars = object.head.bars;
  	delete object.head.bars;//wipe bars before comparison as serverside checksum doesn't have it
	for(var i=0; i<object.tracks.length; i++) {
	    if('notes' in object.tracks[i]) {
	      object.tracks[i].notes.sort(function (a, b) {
	        return a.id < b.id ? -1 : a.id > b.id ? 1 : 0;
	      });
	    }
	  }
	  /* canonicalJson returns JSON in a known order with no spaces. The escaping
	   * and URI functions are the most compatible hack to convert the string to
	   * UTF-8. Sum is part of the adler32 library. 1 is a magic number shared with
	   * the Python (it's actually default in both but I don't want to rely on it
	   * staying that way). */
		
	  var returnVal = sum(unescape(encodeURIComponent(canonicalJson(object))), 1);
	  object.head.bars = bars;
	  return returnVal;
	};
}
