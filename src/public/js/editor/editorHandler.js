	/*
	Handler script for the editor page. This script deals with the inital setup of the page and the drawing 
	of DOM elements onto the page from the tune json retreived from the server. The script also handles the UI
	elements used by the page, such as draggables etc. and manages their interaction.

	There are also three helper scripts used by the editor to deal with channels, ajax calls and midi data and 
	instances of the classes created by those scripts are used here to handle those respective areas.
	*/
	var channelHelper = new ChannelHandler();
	var ajaxHelper = new AjaxHandler();
	var midiHelper = new MidiHandler();
	
	var tuneJSON;//the jingle in json format, which is fetched from the server

	var noteValues = {//relative lengths of notes
		quaver : 0.5,
		crotchet : 1
	};

	/* Properties of the page that need to be kept track of */
	var pageData = {
		scrollLeft : 0,//the amount the canvas has been scrolled
		quarantinedChanges : [],//changes made locally not yet approved my server
		instrumentFunction : null,//tracks whether the dialog opened is add or change instrument
		maxTabs : 6,//maxium allowed number of tags
		songId : null,//the id of the song we are editing
		minimumBars : 8//the minimum number of bars to draw on load
	};
	
	/**
	 * Functions for intialising the page
	 */

	 /*
	 Called on document ready, this draws a loading screen and ajax's for the token needed to open a connection
	 */
	function initEditor() {
		//first thing to do is set up loading page until we can establish a connection
		drawLoadScreen();
		getToken();
	}
	
	function getToken() {
		ajaxHelper.getToken(pageData.songId,function(token) {
			channelHelper.initSocket(token);
		});
	}
	
	/*
	Called after the Tune JSON has been retreived from the server. Saves it locally and calls function to load the canvas
	*/
	function loadNotesFromJSON(data) {
		tuneJSON = data;
		loadCanvas();
	}

	/*
	Called after canvas has been loaded and initialises all other ui elements
	*/
	function loadRemainingUI() {
		loadPalette();
		setPlaybackButtons();
	}
	
	function drawLoadScreen() {
		$('.canvas').append('<h1>Connecting to server<h1>');//display a simple loading message
	}

	/*
	Initialises UI components in the left hand palette, this consists largely of the dialogs for adding and 
	changing instruments and the draggable notes and bin
	*/
	function loadPalette() {
		buildDialogs();
		$('.editor .note').draggable({
			helper : 'clone',
			appendTo : 'body',
			revert : 'invalid',//revert if not dropped onto the canvas
			drag : function(event,ui) {
				//we want to see if a preview div has been drawn, and if it has we will update it
				if($('.preview').length) {
					var noteValue = getNoteValue($(ui.helper));//get length of note
					if(noteValue) {
						drawPreview(event,noteValue,$('.preview'));//draw a preview of the note onto canvas
					}
					
				}
			}
		}); 

		$('.note-bin').droppable({
			accept : '.music-note',
			drop : function(event,ui) {
				if(ui.draggable.hasClass('music-note')) {//if the dragged item is a note from the canvas
					var oldId = ui.draggable.attr('id');
					deleteDraggedNote(oldId);//remove note and send a delete ajax
				}
			}
		});

		$('#tempo-select').change(function() {
			var tempo = $(this).val();//get the new tempo
			tuneJSON.head.tempo = tempo;//update tempo locally
			var actionId = generateId('tempo');
			ajaxHelper.changeTempo(pageData.songId,{tempo : parseInt(tempo,10), actionId : actionId});//notify server of change
			pageData.quarantinedChanges.push({actionId : actionId, tempo : parseInt(tempo,10), time : Date.now()});
		});

		$('.add-bar-button').click(function(){
			$('.tab-pane.active').append(barHTML);//apend a further bar to canvas locally
			setUpDroppable();//initialise the droppable on the new bar
		});
	}

	/*
	This loads the canvas, including drawing the tracks and notes from the tune json as dom elements, and then initialises 
	the ui elements in the canvas so that notes can be dropped on it etc
	*/
	function loadCanvas() {
		//this loads canvas from the json we got sent
		//need to iterate through each track and add tabs 
		$('.canvas').children().remove(); //get rid of loading message
		//calculate how many bars are in piece by working out which note has longest position
		var longestPosition = 0;
		for(var i = 0; i < tuneJSON.tracks.length; i++) {
			if(typeof tuneJSON.tracks[i].notes !== 'undefined') {
				for(var j = 0; j < tuneJSON.tracks[i].notes.length;j++) {
					if(tuneJSON.tracks[i].notes[j].pos > longestPosition) {
						longestPosition = tuneJSON.tracks[i].notes[j].pos;
					}
				}
			}
			
		}
		
		var bars = Math.ceil(longestPosition / (tuneJSON.head.subDivisions * tuneJSON.head.barLength));
		if(bars < pageData.minimumBars) {
			bars = pageData.minimumBars;//if bars less than minimum number then draw the minimum number instead
		}

		tuneJSON.head.bars = bars;//update the number of bars in tube json

		$('#tempo-select').val(tuneJSON.head.tempo + '');//set the tempo selector to the tempo specified

		loadTabs();//load a tab for each track
		$('.canvas .tab-pane').each(function() {loadBars($(this));});//load bars for each tab
		loadNotes();//load notes from json into dom
		updateKey();//update the key of notes at the left of the editor

		setUpDroppable();//initialise the droppable ui on canvas elements
	}
	
	/*
	This function creates a tab for every non-empty track in the tune json, appends it to the document and 
	initialises the remove button on each tab
	*/
	function loadTabs() {
		var htmlToAppend = '';
		htmlToAppend += '<ul class="nav nav-tabs">';
		
		var tabsMade = 0;
		for(var i = 0; i <tuneJSON.tracks.length; i++) {//create the nav tabs for each nonempty track
			if(typeof tuneJSON.tracks[i].instrument !== 'undefined') {
				if(tabsMade === 0) {//if first tab add an active class to it
					tabsMade++;
					htmlToAppend +='<li class="active"><a href="#track' + i +
					 '"  data-toggle="tab"><span class="instrument-name">' + midiHelper.getInstrumentName(tuneJSON.tracks[i].instrument) + 
					 '</span></a></li>';
				} else {
					htmlToAppend += '<li role="presentation"><a href="#track' + i + '" role="tab" data-toggle="tab"><span class="instrument-name">' +
					midiHelper.getInstrumentName(tuneJSON.tracks[i].instrument) + 
					'</span><button class="remove-tab-button" id="remove-tab' + i + '"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></a></li>';
				}
			}
			
			
		}
		
		htmlToAppend += '</ul><div class="tab-content">';
		//now add the tab panels
		
		tabsMade = 0;

		for(var i = 0; i <tuneJSON.tracks.length; i++) {//create the tab pane for each nonempty track
			if(typeof tuneJSON.tracks[i].instrument !== 'undefined') {
				if(tabsMade === 0) {
					htmlToAppend += '<div  class="tab-pane active" id="track' + i +'"></div>';
					tabsMade++;
				} else {
					htmlToAppend+= '<div  class="tab-pane" id="track' + i +'"></div>';
				}

			}
			
		}
		
		htmlToAppend += '</div>';
		$('.canvas').append(htmlToAppend);

		$('.remove-tab-button').click(function() {//add remove event to delete button
			deleteInstrument(parseInt($(this).attr('id').substring(10), 10));//get index of track
		});
		
	}

	/*
	Appends a key and blank bars to the target (which will be a tab pane)
	*/
	function loadBars($target) {
		$target.append(midiHelper.writeKey());
		$target.append(barHTML.repeat(tuneJSON.head.bars));
	}

	/*
	Goes through the tune JSON and draws each note onto the canvas in its correct place
	*/
	function loadNotes() {
		for(var i = 0; i < tuneJSON.tracks.length; i++) {
			if(typeof tuneJSON.tracks[i].instrument !== 'undefined') {//if not a blank track
				for(var j = 0; j<tuneJSON.tracks[i].notes.length; j++){
					var $tab = $('#track' + i);
					drawNote(tuneJSON.tracks[i].notes[j],$tab);//calls helper function to draw the note
				}
			} 
			
		}
	}
	
	/*
	Responsible for intialising the add instrument, change instrument and invite friends dialog
	*/
	function buildDialogs() {
		ajaxHelper.getUsers(pageData.songId);//set initial user list as something to fall back on

		/* 
		This dialog is shared between the add and change instrument functions (they just update the title etc)
		*/
		$('.instrument-dialog').dialog({
			modal : true,
			title : 'Add Instrument',
			autoOpen : false,
			buttons : [{text : 'OK', click : function() {
				//need to work out the instrument to add/change
				var familyIndex  = parseInt($('select#instrument-class').val());//the family of instrument
				var instrumentIndex = parseInt($('select#instrument-choice').val());

				//calls either add or change instrument (depending on dialog) with the selected instrument as an argument
				pageData.instrumentFunction(familyIndex * 8 + instrumentIndex);
				$('.instrument-dialog').dialog("close");
			}},
			{text : 'Cancel', click : function() {
				$('.instrument-dialog').dialog("close");
			}}]
		});

		$('select#instrument-class').change(function() {
			var index = $(this).val();
			$('select#instrument-choice').empty();//remove any current entries
			for(var i = 0; i < 8; i++) {//loop through family of instruments and append to lower select box
				var instrumentNo = index * 8 + i;
				$('select#instrument-choice').append("<option value='" + i + "'>" + midiHelper.getInstrumentName(instrumentNo) + "</option>");
			}
		});
		$('select#instrument-class').change();//call it once to set fill it in initially

		$('button.add-instrument').click(function() {//set up dialog to work for add instrument
			if($('.tab-content').children().length >= pageData.maxTabs) {
				return;//we have reached maximum number of tabs
			}
			$('.ui-dialog-titlebar').html("Add Instrument");
			pageData.instrumentFunction = addInstrument;
			$('.instrument-dialog').removeClass('no-display');
			$('.instrument-dialog').dialog('open');
		});

		$('button.change-instrument').click(function() {//set up dialof to work for change instrument
			$('.ui-dialog-titlebar').html("Change Instrument");
			pageData.instrumentFunction = changeInstrument;
			$('.instrument-dialog').removeClass('no-display');
			$('.instrument-dialog').dialog('open');
		});

		/*
		Create invite friends dialog
		*/
		$('div.invite-dialog').dialog({
			modal : true,
			title : 'Invite friends to collaborate',
			autoOpen : false,
			buttons : [{text : 'Cancel', click : function() {
				$('.invite-dialog').dialog("close");
			}}],
			open : function() {
				ajaxHelper.getUsers(pageData.songId);//update list of users
				$(this).removeClass("no-display");
			}
		});

		$('.invite-button').click(function() {
			$('div.invite-dialog').dialog("open");
			$('.ui-dialog-titlebar').html("Invite friends to collaborate");
		});


		$('input.name-bar').keyup(function(){
			//compare name entered to list of users whenever user types something 
			//and draw a list of matches below with invite buttons for each one
			var name = $(this).val();
			var matches = searchForPossibleUser(name);

			if(!matches || matches.length === 0) {
				$('table.results-table tbody').empty();
				$('span.invite-info').html("No results");
				return;
			}
			$('span.invite-info').html("Results");
			$('table.results-table tbody').empty();//get rid of previous matches 
			for(var i = 0; i < matches.length; i++) {
				var html = '<tr><td>' + matches[i].username + '</td><td><button class="btn btn-primary fresh" id="match' +
				matches[i].user_id + '">Invite' + '</button></td></tr>';

				$('table.results-table tbody').append(html);
				$('button.fresh').click(function() {//fresh tag used to mark button out to register callback
					ajaxHelper.sendInvite(pageData.songId,$(this).attr('id').substring(5), ajaxFailure);
					$(this).html("Added").attr("disabled","disabled");
				});
				$('button.fresh').removeClass('fresh');//get rid of tag after used to register callback
			}
		});
	}
	
	/*
	Draw a preview of a note (the target) with length and position controlled by noteLength and event
	This is used to draw a preview in the correct location when a dragged note is moved about on screen
	*/
	function drawPreview(event,noteLength,$target) {
		//ok so we can use event.pageX - ui.offset and ignore ones where we get minus values as these are false events
		var subDivisions = getsubDivisions();
		var distanceFromLeft = event.pageX - $target.parent().offset().left;
		var width = $target.parent().width();
		if(distanceFromLeft >=0) { //if we are dragging over the correct box
			var position = Math.floor((distanceFromLeft / width) * subDivisions);

			if(position + noteLength > subDivisions) {
				position = subDivisions - noteLength;//if overflows limit it to end of bar
			}
			var leftPos = ((position / subDivisions) * 100) + "%";
			var length = ((noteLength / subDivisions) * 100) + "%";

			$target.css({//update css of the preview to match calculated position and length
				"position" : 'absolute',
				'left' : leftPos,
				'width' : length,
				'visibility' : 'visable'
			});
			$target.removeClass('no-display');
		}
	}

	/*
	Helper function which takes a note as a json and a tab and vreates a dom element for the note
	in the correct position
	*/
	function drawNote(note,$tab) {
		//first we need to work out what bar note is in and where
		var subDivisions = tuneJSON.head.subDivisions * tuneJSON.head.barLength;
		var bar = Math.floor(note.pos / subDivisions);//bar the note needs to be drawn in
		if(bar > tuneJSON.head.bars) {//draw extra bars to allow for note
			var barsNeeded = bar - tuneJSON.head.bars;
			$('.tab-pane.active').append(barHTML.repeat(barsNeeded));
			setUpDroppable();
			tuneJSON.head.bars = bar;
		}
		var pitch =  midiHelper.convertPitchToIndex(note.pitch);
		var left = ((note.pos % subDivisions) / subDivisions) * 100 + '%';//left point of note in bar
		var length = (note.length / subDivisions) * 100 + '%';

		//append note to correct pitch div
		$tab.children('.bar').eq(bar).children('.pitch').eq(pitch).append('<div class="newNote" id="note' + note.id +'"></div>');

		$('.newNote').css({//update css of note to give it correct position and length within parent 
			'position' : 'absolute',
			'left' : left,
			'width' : length
		});
		addNoteUI($('.newNote'));//add ui for dragging and resizing
		$('.newNote').attr('id', note.id);
		$('.newNote').addClass('music-note').removeClass('newNote');
	}

	/*
	Helper function for adding resize and darg ui events to notes
	*/
	function addNoteUI($note) {
		$note.draggable({
			helper : 'clone',
			appendTo : 'body',
			revert : 'invalid',
			start : function(event,ui) {
				$note.addClass('no-display');
				ui.helper.addClass('no-display');//hide actual note while dragging and just show helper and previews
				ui.helper.css({//give helper same size as actual note
					'height' : $note.height(),
					'width' : $note.width()
				});
			},
			drag : function(event,ui) {
				//ok so we want to see if a preview div has been drawn, and if it has we will update it
				if($('.preview').length) {
					ui.helper.addClass('no-display');//dont display helper if preview is being shown
					var noteValue = Math.round($note.width() / $note.parent().width() * getsubDivisions());
					if(noteValue) {
						drawPreview(event,noteValue,$('.preview'));//draw the preview
					}
					
				} else {
					ui.helper.removeClass('no-display');//show helper of no preview
				}
			},
			stop : function(event, ui) {
				$note.removeClass('no-display');
			}
		});
		
		$note.resizable({
			handles : 'w,e',//handles to drag the note with on left and right
			containment : 'parent',
			start : function(event,ui) {
				/* 
				It is necessary to track the previous and original position and length of resized note so that 
				the original note can be sent as a delete ajax
				*/
				var subDivisions = getsubDivisions();
				pageData.previousLeft = Math.round(subDivisions * (ui.originalPosition.left / ui.element.parent().width()));
				pageData.previousLength = Math.round(subDivisions * (ui.originalElement.width() / ui.element.parent().width()));
				pageData.previousLeftRaw = ui.element.position().left;
				pageData.originalLeft = pageData.previousLeft;
				pageData.originalLength = pageData.previousLength;
			},
			resize : function(event,ui) {
				/*
				This purpose of this is to ensure that the resize follows the snappable system and keeps the note aligned
				with the grid. the notes left position and length in terms of subdivisions is calculated and
				updated accordingly in the notes style
				*/
				var subDivisions = getsubDivisions();//saves overhead of repeated function calls
				var left = Math.round(subDivisions * (ui.element.position().left / ui.element.parent().width()));//find left point
				var leftPercent = (left / subDivisions) * 100 + '%';
				var length;

				//work out whether length should be updated and if so do it else use previous value
				if(left === pageData.previousLeft) {
					if(ui.element.position().left !== pageData.previousLeftRaw) {
						length = pageData.previousLength;
					} else {
						length = Math.round(subDivisions * (ui.element.width() / ui.element.parent().width()));
					}
				} else {
					var leftDifference = left - pageData.previousLeft;
					length = pageData.previousLength - leftDifference;
				}

				var lengthPercent = (length / subDivisions) * 100 + '%';
				ui.element.css({//update css of element to reflect new position and length
					'left' : leftPercent,
					'width' : lengthPercent
				});
				pageData.previousLeft = left;
				pageData.previousLength = length;
				pageData.previousLeftRaw = ui.element.position().left;
			},
			stop : function(event,ui) {
				var conflict = false;
				ui.element.parent().children().each(function(i) {//check for any overlap conflicts against other notes
					if($(this).attr('id') !== ui.element.attr('id') && isConflicting(ui.element,$(this))) {
						//check for possible conflicts
						conflict = true;
					}
				}); 
				if(conflict) {//if conflict, revert dragged note to original position and stop there
					var originalLeft = (pageData.originalLeft / getsubDivisions()) * 100 + '%';
					var originalLength = (pageData.originalLength / getsubDivisions()) * 100 + '%';
					ui.element.css({
						'left' : originalLeft,
						'width' : originalLength
					});
					return;
				}
				/*
				Delete the note in the tune json and send an ajax of its old position and then add a new
				note to the tune json with the new position and length and send an add ajax with these paramaters
				*/	
				var id = $note.attr('id');	

				var oldNote = deleteNote(id);//deletye from tune json
				var trackId = parseInt($('.tab-pane.active').attr('id').substring(5), 10);//get tab index in json
				var action = generateId('delete');
				var deleteData = {noteId : oldNote.id, trackId : trackId, actionId : action };

				ajaxHelper.deleteNote(pageData.songId,deleteData);//send delete ajax
				pageData.quarantinedChanges.push({actionId : action, note : oldNote , time : Date.now()});
				var newId = generateId();//generate id for the new note
				$note.attr('id',newId);
				//need to put new size into a data and ajax it and update id of div
				var subDivisions = getsubDivisions();//saves overhead of repeated function calls
				var left = pageData.previousLeft;
				var bar = $note.parent().parent().index() - 1;//allow for key
				var newPosition = bar * subDivisions + left;
				var newLength = pageData.previousLength;
				var newNoteData = {
					id : newId,
					pos : newPosition,
					pitch : oldNote.pitch,
					length : newLength,
					track : trackId
				};
				
				newNoteData.track = trackId;//set the track

				var actionId = generateId('add');
				var newNoteToSend = { actionId : actionId, note : newNoteData};
				ajaxHelper.addNote(pageData.songId,newNoteToSend);//notify the server of new note
				newNoteToSend.time = Date.now();//add timestamp for quarentining

				delete newNoteData.track;//delete track before inserting into tune json for checksum reasons
				tuneJSON.tracks[trackId].notes.push(newNoteData);
				pageData.quarantinedChanges.push(newNoteToSend);
			}
			
		});
	}
	
	/*
	This function sets up the droppable ui for the canvas so that it can deal with notes being dragged onto it
	*/
	function setUpDroppable() {

		$('.pitch').droppable({
			tolerance : 'pointer',
			over : function(event,ui) {
				var canvasArea = $('.tab-pane.active').offset();
				var canvasHeight =  $('.tab-pane.active').height();
				var canvasWidth = $('.tab-pane.active').width();
				if(event.pageX < canvasArea.left || event.pageY < canvasArea.top ||//ensure event occured within canvas
				 event.pageX > canvasArea.left + canvasWidth || event.pageY > canvasArea.top + canvasHeight) {
					return;//event is outside the range of the canvas
				}
				pageData.$currentPreviewDiv = $(this);
				$(event.target).append("<div class='preview no-display'></div>");//append preview div to pitch
			},
			out : function(event,ui) {
				$(event.target).children('.preview').remove();//remove preview div from pitch
			},
			drop : function(event,ui) {
				if($('.preview').length !== 1) {//if no preview or more than one preview
					$('.preview').remove();
					return;//something has gone wrong with drawing code so do not carry on!
				}
				var conflict = false;
				$(event.target).children('.music-note').each(function(i) {//check for overlap conflict with other notes

					if($(this).attr('id') !== ui.draggable.attr('id') && isConflicting($(this),$('.preview'))) {
						conflict = true;
					}
				});
				if(conflict) {//if conflict remove the preview
					if(ui.draggable.hasClass('music-note')) {
						ui.draggable.removeClass('no-display');//make original position visible again
					}
					$('.preview').remove();
				} else {
					if(ui.draggable.hasClass('music-note')) {//if we are dragging an existing note
						//deal with moving note here. Easiest thing is going to be to remove it and
						//send a delete ajax
						var oldId = ui.draggable.attr('id');
						deleteDraggedNote(oldId);
					}
					
					//we need to turn preview's position into a json to send to server
					var left = $('.preview').position().left / $('.preview').parent().width();

					var width = $('.preview').width() / $('.preview').parent().width();
					var bar = $('.preview').parent().parent().index() - 1;//gets index of bar, allowing for key
					
					var subDivisions = (tuneJSON.head.barLength * tuneJSON.head.subDivisions);
					var notePosition = (bar * subDivisions) + Math.round(left * subDivisions);
					var noteLength = Math.round(width * subDivisions);
					var noteTrack = parseInt($('.tab-pane.active').attr('id').substring(5), 10);//get trackid from dom element id
					var notePitch = midiHelper.convertIndexToPitch($('.preview').parent().index());
					var noteId = generateId();//need new id even if just dragging
					var actionId = generateId('add');
					var data = {
						actionId : actionId,
						note : {
							pitch : notePitch,
							track : noteTrack,
							length : noteLength,
							pos : notePosition,
							id : noteId
						}
							
					};
					
					ajaxHelper.addNote(pageData.songId,data);
					data.time = Date.now(); //add timestamp for quarantining 
					pageData.quarantinedChanges.push(data);
					addNoteUI($('.preview'));//make it draggable etc
					$('.preview').attr('id',noteId);
					$('.preview').addClass('music-note').removeClass('preview').removeClass('no-display');
					delete data.note.track; //not needed for tune json
					delete data.time;

					tuneJSON.tracks[noteTrack].notes.push(data.note);

				}
				

			}
		});
	}

	/*
	Helper for deleting a dragged note using ther id of the original note
	*/
	function deleteDraggedNote(oldId) {
		var oldNote = deleteNote(oldId);//will also delete the note from json
		$('#' + oldId).remove();
						
		var actionId = generateId('delete');//generate action id

		var deleteData = {
			noteId : oldNote.id,
			actionId : actionId,
			trackId : parseInt($('.tab-pane.active').attr('id').substring(5), 10)
		};

						
		ajaxHelper.deleteNote(pageData.songId,deleteData);
		pageData.quarantinedChanges.push({actionId : actionId, note : oldNote, time : Date.now()});
	}

	/*
	Initialise the playback buttons used to compile and play the jingle
	*/
	function setPlaybackButtons() {
		$('.play-button').click(function(event,ui) {
			if(pageData.compiledMidi && (!MIDI.Player.playing)) {//if we have something to play and not already playing
				if(MIDI.Player.endTime === MIDI.Player.currentTime) {
					MIDI.Player.stop();//reset to start
					MIDI.Player.start();
				} else if(MIDI.Player.currentTime > 0) {//if not at the start
					MIDI.Player.resume();
				} else {
					MIDI.Player.start();
				}
				
			} else if(!pageData.compiledMidi) {
				alert('Please compile your Jingle before trying to play!');
			} 
		});
		$('.pause-button').click(function(event,ui) {
			if(MIDI.Player.playing) {
				MIDI.Player.pause();
			}
		});
		$('.stop-button').click(resetPlayer);
		$('.compile-button').click(function(event,ui) {
			pageData.compiledMidi = false;
			$('.progress-bar').html('Compiling tune').css({
				'width' : '100%'
			});
			ajaxHelper.compileTune(pageData.songId,function(data) {//fetch compiled tune from server and load it
				loadMidi(data);
			});
		});
	}

	function resetPlayer() {//defined explictly as referred to by stop button and finished playing callback
		MIDI.Player.stop();
		$('.progress-bar').html('Ready to play').css({
			'width' : '100%'
		});
	}

	/*
	Load the midi js plugin for the compiled midi fetched from server
	*/
	function loadMidi(data) {
		if(MIDI) {
			MIDI.Player.loadFile('data:audio/midi;base64,' + data.midi,function() {//stick file format on front of data
				var instruments = [];
				for(var i = 0; i < data.instruments.length; i++) {
					instruments.push(data.instruments[i].instrument); 
				}
				MIDI.loadPlugin({
					soundfontUrl : '/public/soundfonts/',
					instruments : instruments,
					callback : function() {
						for(var i = 0; i < data.instruments.length; i++) {
							var trackNum = data.instruments[i].track;
							if(trackNum < 9) {
								MIDI.programChange(trackNum,data.instruments[i].instrument);
							} else {
								MIDI.programChange(trackNum + 1,data.instruments[i].instrument);//track 10 reserved so offset
							}
							
						}
						
						pageData.compiledMidi = true;
						$('.progress-bar').html('Ready to play').css({
							'width' : '100%'
						});

						MIDI.Player.addListener(function(data) {
							if(data.now === data.end) {
								resetPlayer();
								return;
							}
							var playProgress = ((data.now / data.end) * 100) + '%';
							var progressRounded = Math.round((data.now / data.end) * 100) + '%';
							$('.progress-bar').html(progressRounded).css({
								'width' : playProgress
							});	
						});
					}
				});
			});
		}
	}
	
	/*
	Adds an instrument to the jingle by creating a new tab for, updating the tune json and notifying
	the server of the change
	*/
	function addInstrument(id,track) {//optional argument of track for when loading from channels
		//find an empty track for our new instrument to reside in
		var trackId;
		for(var i = 0; i < tuneJSON.tracks.length && !trackId; i++) {//stop once trackId is set
			if(typeof tuneJSON.tracks[i].instrument === 'undefined') {
				trackId = i;
			}
		}
		if(track || track === 0) {//if track supplied, use instead of free track
			trackId = track;
		}

		var htmlToAppend ='<li><a href="#track' + trackId +
					 '"  data-toggle="tab"><span class="instrument-name">' + midiHelper.getInstrumentName(id) + 
					 '</span><button class="remove-tab-button newtag"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></a></li>';
		$('.nav-tabs').append(htmlToAppend);
		htmlToAppend = '<div class="tab-pane" id="track' + trackId +'"></div>';
		$('.tab-content').append(htmlToAppend);
		loadBars($('.tab-content').children().last());
		

		$('.nav-tabs a:last').tab('show');

		//enable event listeners on the new tab content
		setUpDroppable();

		$('.newtag').click(function() {
			deleteInstrument(trackId);
		});
		$('.newtag').removeClass('newtag');//class is just used for flagging the new button created

		if($('.tab-content').children().length >= pageData.maxTabs) {
			$('button.add-instrument').attr("disabled","disabled");
		}

		tuneJSON.tracks[trackId].instrument = id;
		tuneJSON.tracks[trackId].notes = [];

		if(track || track === 0) {
			return;//no need to ajax the change as we are reacting to a channel message not making it ourselves
		}
		var actionId = generateId("instrumentAdd");
		var instrument = {inst : id, track : trackId};
		var data = {actionId : actionId, instrument : instrument};
		ajaxHelper.addInstrument(pageData.songId,data);
		data.time = Date.now();//add timestamp for quarantining
		pageData.quarantinedChanges.push(data);
		

	}

	/*
	Change the current instrument and notify server of change
	*/
	function changeInstrument(id,trackId) {//optional trackId for if dealing with channel message
		$('li.active a span.instrument-name').html(midiHelper.getInstrumentName(id));
		var track = null;
		if(!trackId && trackId !== 0) {//if no track provided use current track
			track = parseInt($('.tab-pane.active').attr('id').substring(5), 10);
		} else {
			track = trackId;
		}
		
		tuneJSON.tracks[track].instrument = id;

		if(trackId || trackId === 0) {
			return;//no need to send ajax as we are reacting to a channel change
		}
		var actionId = generateId('instrumentEdit');
		var data = {actionId : actionId, instrumentTrack : track, instrumentNumber : id};
		ajaxHelper.changeInstrument(pageData.songId,data);
		data.time = Date.now();//add timestamp for quarantining
		pageData.quarantinedChanges.push(data);

		
	}

	/*
	Delete the instrument in the specified track and update server if necessary
	*/
	function deleteInstrument(tabId,fromChannels) {
		var tabIndex = $('#track' + tabId).index();
		if(!tabIndex) {
			return;
		}
		if($('.tab-pane.active').attr('id').substring(5) === tabId + '') {//if deleting the active tab
			$('.nav-tabs li a').eq(tabIndex - 1).tab("show");//show the tab to the left
		} 
		$('.nav-tabs').children().eq(tabIndex).remove();
		$('.tab-content').children().eq(tabIndex).remove();

		 tuneJSON.tracks[tabId].notes = [];
		 delete tuneJSON.tracks[tabId].instrument;//wipe the track clean
		 $('button.add-instrument').removeAttr("disabled");//removes the disable on the button if it exists
		 if(fromChannels) {
		 	return;
		 }
		 var actionId = generateId('deleteInstrument');
		 var data = {actionId : actionId, instrumentTrack : tabId};
		
		 ajaxHelper.deleteInstrument(pageData.songId,data);
		 data.time = Date.now();//add timestamp for quarantining
		 pageData.quarantinedChanges.push(data);
		 
	}

	/*
	This function is responsible for drawing a key to the left of the tabbed area showing which note values go where 
	*/
	function updateKey() {
		$('.canvas .tab-pane').scroll(function() {
			if($(this).scrollLeft() === pageData.scrollLeft) {
				return;//only interested in horizontal scroll
			} 
			var scrollAmount = $(this).scrollLeft();
			pageData.scrollLeft = scrollAmount;
			$('.key').css({
				'left' : scrollAmount
			});
		});
	}

	

	function getNoteValue($target) {
		var note;
		if($target.hasClass('note-crotchet')) {
			note = tuneJSON.head.subDivisions * noteValues.crotchet;
		} else if($target.hasClass('note-quaver')) {
			note = tuneJSON.head.subDivisions * noteValues.quaver;
		}
		return note;
	}

	function isConflicting($element1,$element2) {//helper method to see if 2 elements overlap horizontally
		var left = $element1.position().left;
		var right = left + $element1.width();

		var newLeft = $element2.position().left;
		var newRight = newLeft + $element2.width();

		return (left < newLeft && right > newLeft) || (left >= newLeft && left <= newRight );
	}

	/*
	Generates a random id with the option to supply a prefix
	*/
	function generateId(word) {
		var prefix = 'note-';//default prefix if none supplied
		if(word) {
			prefix = word + '-';
		}

		  function s4() {
		    return Math.floor((1 + Math.random()) * 0x10000)
		               .toString(16)
		               .substring(1);
		  }
		  return prefix + s4() + s4() + '-' + s4() + '-' + s4() + '-' +
		    s4() + '-' + s4() + s4() + s4();
		
		
	}

	function searchForPossibleUser(name) {
		//take a name as a string and do a wildcard search for users with similar names
		var matches = [];

		if(!name || name.length === 0) {//if no input return empty array
			return matches;
		}
		for(var i = 0; i < pageData.users.length; i++) {
			if(pageData.users[i].username.indexOf(name.trim()) !== -1) {//if we have some sort of match
				if($('span#userWelcome').html() !== pageData.users[i].username) {//if not us!
					matches.push(pageData.users[i]);
				}
			}
		}
		return matches;
	}

	function deleteNote(id) {//deletes a note from the tune json and returns the deleted note
		id += ''; //make sure id is a string for comparisons
		var note;
	
		for(var i = 0; i < tuneJSON.tracks.length; i++) {
			if(typeof tuneJSON.tracks[i].notes !== 'undefined') {
				for(var j = 0; j < tuneJSON.tracks[i].notes.length; j++) {
					if(tuneJSON.tracks[i].notes[j].id + '' === id) {//converts any numbers to strings for comparison
						note = tuneJSON.tracks[i].notes[j];
						tuneJSON.tracks[i].notes.splice(j,1);
					}
				}
			}
			
		}
		return note;
	}

	//simple helper to enable us to repeat strings
	//used when appending bar html etc.
	String.prototype.repeat = function( num )
	{
	    return new Array( num + 1 ).join( this );
	};

	var barHTML = '<div class="bar">' + '<div class="pitch"></div>'.repeat(37) + '</div>';
	var keyHTML = '<div class="key">' + '<div class="key-pitch"></div>'.repeat(37) + '</div>';
	
	/*
	Function to deal with getting a new tunejson from the server when something has gone wrong
	*/
	function reloadTune() {
		ajaxHelper.getTuneJSON(pageData.songId,function(data) {
			loadNotesFromJSON(data);
		});
	}

	

	function getsubDivisions() {
		return tuneJSON.head.subDivisions * tuneJSON.head.barLength;
	}

	$(function() {
		//set song id before doing anything else
		if($('div#songid').length > 0) {
			pageData.songId = $('div#songid').html();
		}

		initEditor();

	});
