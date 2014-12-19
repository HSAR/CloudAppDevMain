	/*
	Handler script for the music editor. Still in early stages
	*/

	//TODO call draw preview on dragged between pitches divs so they dont disappear
	String.prototype.repeat = function( num )
	{
	    return new Array( num + 1 ).join( this );
	}
	var ajaxHelper = new AjaxHandler();
	var midiHelper = new MidiHandler();
	var channelHelper = new ChannelHandler();

	var barHTML = '<div class="bar">' + '<div class="pitch"></div>'.repeat(36) + '</div>';
	var keyHTML = '<div class="key">' + '<div class="key-pitch"></div>'.repeat(36) + '</div>';

	var tuneJSON;

	var noteValues = {
		quaver : 0.5,
		crotchet : 1
	}

	var pageData = {
		scrollLeft : 0,
		quarantinedChanges : [],
		instrumentFunction : null,
		tabCount : 0,
		maxTabs : 6,
		songId : 0//TODO
	};

	function loadPalette() {
		//we need to load the pallete items and then make em draggable etc.
		buildDialogs();
		$('.editor .note').draggable({
			helper : 'clone',
			appendTo : 'body',
			revert : 'invalid',
			drag : function(event,ui) {
				//ok so we want to see if a preview div has been drawn, and if it has we will update it
				if($('.preview').length) {
					var noteValue = getNoteValue($(ui.helper));
					if(noteValue) {
						drawPreview(event,noteValue,$('.preview'));
					}
					
				}
			}
		}); //could be a dangerous game as moved out of pallete
		//console.log($('.pallete'))
	}

	function loadCanvas() {
		//this loads canvas from the json we got sent
		//need to iterate through each track and add tabs (we will need at least one tab regardless)
		//if tracks is empty add default tab otherwise add tabs as per usual
		$('.canvas').children().remove(); //get rid of loading message
		tuneJSON.head.bars = 8;//TODO TEMPORARY DEV FIX
		tuneJSON.head.barLength = 4;//TODO TEMPORARY DEV FIX
		loadTabs();
		$('.canvas .tab-pane').each(function() {loadBars($(this))});//load bars for each tab
		loadNotes();
		updateKey();

		setUpDroppable();

		loadPalette();
		setPlayButton();
	}

	function setUpDroppable() {

		$('.pitch').droppable({//remove any previous droppable handlers
			tolerance : 'pointer',
			over : function(event,ui) {
				pageData.$currentPreviewDiv = $(this);
				$(event.target).append("<div class='preview no-display'></div>");
			},
			out : function(event,ui) {
				$(event.target).children('.preview').remove();
			},
			drop : function(event,ui) {
				//we need to reclass the preview div here and add it to the model

				//ajax some shit here

				//also need to handle two notes being dropped on top of each other.
				if($('.preview').length !== 1) {
					$('.preview').remove();
					return;//something has gone wrong with drawing code so do not carry on!
				}
				var conflict = false;
				$(event.target).children('.music-note').each(function(i) {
					if($(this).attr('id') !== ui.draggable.attr('id') && isConflicting($(this),$('.preview'))) {
						conflict = true;
					}
				});
				if(conflict) {
					if(ui.draggable.hasClass('music-note')) {
						ui.draggable.removeClass('no-display');//make original position visible again
					}
					$('.preview').remove();
				} else {
					if(ui.draggable.hasClass('music-note')) {
						//deal with moving note here. Easiest thing is going to be to remove it and
						//send a delete ajax
						var oldId = ui.draggable.attr('id');
						var oldNote = deleteNote(oldId);//will also delete the note from json
						$('#' + oldId).remove();
						
						var actionId = generateId('delete');//generate action id

						var deleteData = {
							noteId : oldNote.id,
							actionId : actionId,
							trackId : $('.tab-pane.active').index()
						};

						
						ajaxHelper.deleteNote(pageData.songId,deleteData);
						pageData.quarantinedChanges.push(actionId : actionId, note : oldNote);
					}
					
					//we need to turn preview's position into a json to send to server
					var left = $('.preview').position().left / $('.preview').parent().width();
					console.log("left " + left);
					var width = $('.preview').width() / $('.preview').parent().width();
					var bar = $('.preview').parent().parent().index();//gets index of bar
					
					var subDivisions = (tuneJSON.head.barLength * tuneJSON.head.subDivisions)
					var notePosition = (bar * subDivisions) + Math.round(left * subDivisions);
					var noteLength = Math.round(width * subDivisions);
					var noteTrack = $('.tab-pane.active').attr('id').substring(5);//get trackid from dom element id
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
					pageData.quarantinedChanges.push(data);
					addNoteUI($('.preview'));//make it draggable etc
					$('.preview').attr('id',noteId);
					$('.preview').addClass('music-note').removeClass('preview').removeClass('no-display');
					delete data.note.track; //not needed for tune json
					tuneJSON.tracks[noteTrack].notes.push(data.note);

				}
				

			}
		});
	}

	function setPlayButton() {
		$('.play-button').click(function(event,ui) {
			ajaxHelper.compileTune(pageData.songId,function(data) {
				playMidi(data);
			});
		});
	}

	function playMidi(data) {
		if(MIDI) {
			MIDI.player.loadFile(data,function() {
				MIDI.player.start();
			});
		}
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
		})
	}

	/*
	We can use this to to keep track of moving draggable elements whether on initial drop or subsequent moves
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

			$target.css({
				"position" : 'absolute',
				'left' : leftPos,
				'width' : length,
				'visibility' : 'visable'
			});
			$target.removeClass('no-display');
		}
	}

	function loadTabs() {
		//lets handle the lack of tracks here if necessary
		var currentTabCount = pageData.tabCount;//save the current tab count
		var htmlToAppend = '';
		htmlToAppend += '<ul class="nav nav-tabs">';
		if(tuneJSON.tracks.length > 0) {
			for(var i = 0; i <tuneJSON.tracks.length; i++) {
				if(typeof tuneJSON.tracks[i].instrument !== 'undefined') {
					if(i === 0) {
						htmlToAppend +='<li class="active"><a href="#track' + i +
						 '"  data-toggle="tab"><span class="instrument-name">' + midiHelper.getInstrumentName(tuneJSON.tracks[i].instrument) + 
						 '</span></a></li>';
					} else {
						htmlToAppend += '<li role="presentation"><a href="#track' + i + '" role="tab" data-toggle="tab"><span class="instrument-name">' +
						midiHelper.getInstrumentName(tuneJSON.tracks[i].instrument) + 
						'</span><button class="remove-tab-button"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></a></li>';
					}
					pageData.tabCount++;
				}
				
				
			}
		} else {//add default tab
			$('.canvas').append('<li class="active"><a href="#default"  data-toggle="tab"></a></li>');
		}
		htmlToAppend += '</ul><div class="tab-content">';
		//now add the tab panels
		if(tuneJSON.tracks.length > 0) {
			pageData.tabCount = currentTabCount;
			for(var i = 0; i <tuneJSON.tracks.length; i++) {
				if(typeof tuneJSON.tracks[i].instrument !== 'undefined') {
					if(i === 0) {
						htmlToAppend += '<div  class="tab-pane active" id="track' + i +'"></div>';
					} else {
						htmlToAppend+= '<div  class="tab-pane" id="track' + i +'"></div>';
					}
					pageData.tabCount++;
				}
				
				
			}
		} else {
			$('.canvas').append('<div class="tab-pane" id="default"></div>');
		}
		htmlToAppend += '</div>';
		$('.canvas').append(htmlToAppend);

		$('.remove-note-button').click(function() {
			deleteInstrument($(this).parent().parent().index());
		});
	}

	function loadBars($target) {
		$target.append(midiHelper.writeKey());
		$target.append(barHTML.repeat(tuneJSON.head.bars));
	}

	function loadNotes() {
		for(var i = 0; i < tuneJSON.tracks.length; i++) {
			if(typeof tuneJSON.tracks[i].instrument !== 'undefined') {
				for(var j = 0; j<tuneJSON.tracks[i].notes.length; j++){
					$tab = $('#track' + i);
					drawNote(tuneJSON.tracks[i].notes[j],$tab);
				}
			} 
			
		}
	}

	function drawNote(note,$tab) {
		//first we need to work out what bar note is in and where

		var subDivisions = tuneJSON.head.subDivisions * tuneJSON.head.barLength;
		var bar = Math.floor(note.pos / subDivisions);
		var pitch =  midiHelper.convertPitchToIndex(note.pitch);
		var left = ((note.pos % subDivisions) / subDivisions) * 100 + '%';//could potentially divide by 0 but js protects us
		var length = (note.length / subDivisions) * 100 + '%';
		console.log("bar " + bar);
		console.log("subDivisions " + subDivisions);
		$tab.children('.bar').eq(bar).children('.pitch').eq(pitch).append('<div class="newNote" id="note' + note.id +'"></div>');

		$('.newNote').css({
			'position' : 'absolute',
			'left' : left,
			'width' : length
		});
		addNoteUI($('.newNote'));
		$('.newNote').attr('id', note.id);
		$('.newNote').addClass('music-note').removeClass('newNote');
	}

	function drawLoadScreen() {
		$('.canvas').append('<h1>Connecting to server<h1>');
	}

	function addNoteUI($note) {
		$note.draggable({
			helper : 'clone',
			appendTo : 'body',
			revert : 'invalid',
			start : function(event,ui) {
				$note.addClass('no-display');
				ui.helper.addClass('no-display');
			},
			drag : function(event,ui) {
				//ok so we want to see if a preview div has been drawn, and if it has we will update it
				if($('.preview').length) {
					var noteValue = Math.round($note.width() / $note.parent().width() * getsubDivisions());
					if(noteValue) {
						drawPreview(event,noteValue,$('.preview'));
					}
					
				}
			},
			stop : function(event, ui) {
				$note.removeClass('no-display');
			}
		});
		
		$note.resizable({
			handles : 'w,e',
			containment : 'parent',
			start : function(event,ui) {
				var subDivisions = getsubDivisions();
				pageData.previousLeft = Math.round(subDivisions * (ui.originalPosition.left / ui.element.parent().width()));
				pageData.previousLength = Math.round(subDivisions * (ui.originalElement.width() / ui.element.parent().width()));
				pageData.previousLeftRaw = ui.element.position().left;
				pageData.originalLeft = pageData.previousLeft;
				pageData.originalLength = pageData.previousLength;
			},
			resize : function(event,ui) {
				var subDivisions = getsubDivisions();//saves overhead of repeated function calls
				var left = Math.round(subDivisions * (ui.element.position().left / ui.element.parent().width()));
				var leftPercent = (left / subDivisions) * 100 + '%';
				var length;
				if(left === pageData.previousLeft) {
					if(ui.element.position().left !== pageData.previousLeftRaw) {
						length = pageData.previousLength;
					} else {
						length = Math.round(subDivisions * (ui.element.width() / ui.element.parent().width()));
					}
				} else {
					var leftDifference = left - pageData.previousLeft;
					console.log(leftDifference);
					length = pageData.previousLength - leftDifference;
				}
				var lengthPercent = (length / subDivisions) * 100 + '%';
				ui.element.css({
					'left' : leftPercent,
					'width' : lengthPercent
				});
				pageData.previousLeft = left;
				pageData.previousLength = length;
				pageData.previousLeftRaw = ui.element.position().left;
			},
			stop : function(event,ui) {
				var conflict = false;
				ui.element.parent().children().each(function(i) {
					if($(this).attr('id') !== ui.element.attr('id') && isConflicting(ui.element,$(this))) {
						//check for possible conflicts
						conflict = true;
					}
				}); 
				if(conflict) {
					var originalLeft = (pageData.originalLeft / getsubDivisions()) * 100 + '%';
					var originalLength = (pageData.originalLength / getsubDivisions()) * 100 + '%';
					ui.element.css({
						'left' : originalLeft,
						'width' : originalLength
					});
					return;
				}	
				var id = $note.attr('id');	
				console.log(id);
				var oldNote = deleteNote(id);
				var trackId = $('.tab-pane.active').attr('id').substring(5);//get tab index in json
				var action = generateId('delete');
				var deleteData = {noteId : oldNote.id, trackId : trackId, actionId : action };

				ajaxHelper.deleteNote(pageData.songId,deleteData);
				pageData.quarantinedChanges.push({actionId : action, note : oldNote });
				var newId = generateId();
				$note.attr('id',newId);
				//need to put new size into a data and ajax it and update id of div
				var subDivisions = getsubDivisions();//saves overhead of repeated function calls
				var left = pageData.previousLeft;
				var bar = $note.parent().parent().index();
				var newPosition = bar * subDivisions + left;
				var newLength = pageData.previousLength;
				var newNoteData = {
					id : newId,
					pos : newPosition,
					pitch : oldNote.pitch,
					length : newLength,
				};
				tuneJSON.tracks[trackId].notes.push(newNoteData);
				newNoteData.track = trackId;//set the track

				var actionId = generateId('add');
				var newNoteToSend = { actionId : actionId, note : newNoteData};
				ajaxHelper.addNote(pageData.songId,newNoteToSend);
				pageData.quarantinedChanges.push(newNoteToSend);
			}
			
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
		console.log(left + " " + right + " " + newLeft + " " + newRight);
		if((left < newLeft && right > newLeft) || (left >= newLeft && left <= newRight )) {
			return true;
		}
		return false;
	}

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

	function buildDialogs() {


		$('.instrument-dialog').dialog({
			modal : true,
			title : 'Add Instrument',
			autoOpen : false,
			buttons : [{text : 'OK', click : function() {
				//need to work out the instrument to add/change
				var familyIndex  = parseInt($('select#instrument-class').val());
				var instrumentIndex = parseInt($('select#instrument-choice').val());
				//TODO check cast is safe
				console.log(familyIndex);
				console.log(instrumentIndex);
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
			for(var i = 0; i < 8; i++) {//loop through family of instruments
				var instrumentNo = index * 8 + i;
				$('select#instrument-choice').append("<option value='" + i + "'>" + midiHelper.getInstrumentName(instrumentNo) + "</option>");
			}
		});
		$('select#instrument-class').change();//call it once to set fill it in initially

		$('button.add-instrument').click(function() {
			if($('.tab-content').children().length >= pageData.maxTabs) {
				return;//we have reached maximum number of tabs
			}
			$('.ui-dialog-titlebar').html("Add Instrument");
			pageData.instrumentFunction = addInstrument;
			$('.instrument-dialog').removeClass('no-display');
			$('.instrument-dialog').dialog('open');
		});

		$('button.change-instrument').click(function() {
			$('.ui-dialog-titlebar').html("Change Instrument");
			pageData.instrumentFunction = changeInstrument;
			$('.instrument-dialog').removeClass('no-display');
			$('.instrument-dialog').dialog('open');
		});
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

	function addInstrument(id) {
		var tabsLength = pageData.tabCount;

		//find an empty track for our new instrument to reside in
		var trackId;
		for(var i = 0; i < tuneJSON.tracks.length && !trackId; i++) {//stop once trackId is set
			if(typeof tuneJSON.tracks[i].instrument === 'undefined') {
				trackId = i;
			}
		}

		var htmlToAppend ='<li><a href="#track' + trackId +
					 '"  data-toggle="tab"><span class="instrument-name">' + midiHelper.getInstrumentName(id) + 
					 '</span><button class="remove-tab-button newtag"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></a></li>';
		$('.nav-tabs').append(htmlToAppend);
		htmlToAppend = '<div class="tab-pane" id="track' + trackId +'"></div>';
		$('.tab-content').append(htmlToAppend);
		loadBars($('.tab-content').children().last());
		pageData.tabCount++;

		$('.nav-tabs a:last').tab('show');

		//enable event listeners on the new tab content
		setUpDroppable();

		tuneJSON.tracks[trackId].instrument = id;
		var actionId = generateId("instrumentAdd");
		var instrument = {inst : id, track : trackId};
		var data = {actionId : actionId, instrument : instrument};
		ajaxHelper.addInstrument(pageData.songId,data);//TODO might need to send where also
		pageData.quarantinedChanges.push(data);
		$('.newtag').click(function() {
			deleteInstrument(trackId);
		});
		$('.newtag').removeClass('newtag');//class is just used for flagging the new button created

		if($('.tab-content').children().length >= pageData.maxTabs) {
			$('button.add-instrument').attr("disabled","disabled");
		}
	}

	function changeInstrument(id) {
		$('li.active a span.instrument-name').html(midiHelper.getInstrumentName(id));
		var track = $('.tab-pane.active').attr('id').substring(5);
		tuneJSON.tracks[track].instrument = id;
		actionId = generateId('instrumentEdit');
		var data = {actionId : actionId, instrumentTrack : track, instrumentNumber : id};
		ajaxHelper.changeInstrument(pageData.songId,data);
		pageData.quarantinedChanges.push(data);

		
	}

	function deleteInstrument(tabId) {
		var tabIndex = $('#track' + tabId).index();
		if(!tabIndex) {
			return;
		}
		if($('.tab-pane.active').attr('id').substring(5) === tabId) {//if deleting the active tab
			$('.nav-tabs li a').eq(tabIndex - 1).tab("show");//show the tab to the left
		} 
		$('.nav-tabs').children().eq(tabIndex).remove();
		$('.tab-content').children().eq(tabIndex).remove();

		 tuneJSON.tracks[tabId].notes = [];
		 delete tuneJSON.tracks[tabId].instrument;//wipe the track clean

		 var actionId = generateId('deleteInstrument');
		 var data = {actionId : actionId, instrumentTrack : tabId};
		 $('button.add-instrument').removeAttr("disabled");//removes the disable on the button if it exists
		 ajaxHelper.deleteInstrument(pageData.songId,data);
		 pageData.quarantinedChanges.push(data);
		 
	}

	function loadNotesFromJSON(data) {
		tuneJSON = data;
		loadCanvas();
	}

	function getToken() {
		ajaxHelper.getToken(pageData.songId,function(token) {
			channelHelper.initSocket(token);
		});
	}

	function getsubDivisions() {
		return tuneJSON.head.subDivisions * tuneJSON.head.barLength;
	}

	function initEditor() {
		//first thing to do is set up loading page until we can establish a connection
		drawLoadScreen();
		getToken();
	}

	//what do we want to test? loading notes from JSON

	$(function() {
		//set song id before doing anything else
		if($('div#songid').length > 0) {
			pageData.songId = $('div#songid').html();
		}

		initEditor();




	});