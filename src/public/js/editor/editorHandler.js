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
		quarantinedChanges : []
	};

	function loadPalette() {
		//we need to load the pallete items and then make em draggable etc.
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

		loadTabs();
		loadBars();
		loadNotes();
		updateKey();
		
		$('.pitch').droppable({
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
						var oldNoteTrack = { track : $('.tab-pane.active').index() };//could be vulnerable to swift tab switch
						var completeDeleteData = $.extend(oldNote,oldNoteTrack);
						var deleteData = {
							topic : 'delete',
							data : completeDeleteData
						};
						ajaxHelper.notifyServer(deleteData);
						pageData.quarantinedChanges.push(deleteData);
					}
					
					//we need to turn preview's position into a json to send to server
					var left = $('.preview').position().left / $('.preview').parent().width();
					console.log("left " + left);
					var width = $('.preview').width() / $('.preview').parent().width();
					var bar = $('.preview').parent().parent().index();//gets index of bar
					
					var subdivisions = (tuneJSON.head.barLength * tuneJSON.head.subdivisions)
					var notePosition = (bar * subdivisions) + Math.round(left * subdivisions);
					var noteLength = Math.round(width * subdivisions);
					var noteTrack = $('.tab-pane.active').index();
					var notePitch = midiHelper.convertIndexToPitch($('.preview').parent().index());
					var noteId = generateId();//need new id even if just dragging
					var data = {
						topic : 'add',
						data : {
							pitch : notePitch,
							track : noteTrack,
							length : noteLength,
							position : notePosition,
							id : noteId
						}
					};
					ajaxHelper.notifyServer(data);
					pageData.quarantinedChanges.push(data);
					addNoteUI($('.preview'));//make it draggable etc
					$('.preview').attr('id',noteId);
					$('.preview').addClass('music-note').removeClass('preview').removeClass('no-display');
					tuneJSON.tracks[noteTrack].notes.push(data.data);

				}
				

			}
		});

		loadPalette();
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
		var subdivisions = getSubdivisions();
		var distanceFromLeft = event.pageX - $target.parent().offset().left;
		var width = $target.parent().width();
		if(distanceFromLeft >=0) { //if we are dragging over the correct box
			var position = Math.floor((distanceFromLeft / width) * subdivisions);

			if(position + noteLength > subdivisions) {
				position = subdivisions - noteLength;//if overflows limit it to end of bar
			}
			var leftPos = ((position / subdivisions) * 100) + "%";
			var length = ((noteLength / subdivisions) * 100) + "%";

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
		var htmlToAppend = '';
		htmlToAppend += '<ul class="nav nav-tabs" role="tablist">';
		if(tuneJSON.tracks.length > 0) {
			for(var i = 0; i <tuneJSON.tracks.length; i++) {
				if(i === 0) {
					htmlToAppend +='<li role="presentation" class="active"><a href="#track' + i +
					 '" role="tab" data-toggle="tab">' + midiHelper.getInstrumentName(tuneJSON.tracks[i].instrument) + '</a></li>';
				} else {
					htmlToAppend += '<li role="presentation"><a href="#track' + i + '" role="tab" data-toggle="tab">' +
					midiHelper.getInstrumentName(tuneJSON.tracks[i].instrument) + '</a></li>';
				}
				
			}
		} else {//add default tab
			$('.canvas').append('<li role="presentation" class="active"><a href="#default" role="tab" data-toggle="tab"></a></li>');
		}
		htmlToAppend += '</ul><div class="tab-content">';
		//now add the tab panels
		if(tuneJSON.tracks.length > 0) {
			for(var i = 0; i <tuneJSON.tracks.length; i++) {
				if(i === 0) {
					htmlToAppend += '<div role="tabpanel" class="tab-pane active" id="track' + i +'"></div>';
				} else {
					htmlToAppend+= '<div role="tabpanel" class="tab-pane" id="track' + i +'"></div>';
				}
				
			}
		} else {
			$('.canvas').append('<div role="tabpanel" class="tab-pane" id="default"></div>');
		}
		htmlToAppend += '</div>';
		$('.canvas').append(htmlToAppend);
	}

	function loadBars() {
		$('.canvas .tab-pane').append(midiHelper.writeKey());
		$('.canvas .tab-pane').append(barHTML.repeat(tuneJSON.head.bars));
	}

	function loadNotes() {
		for(var i = 0; i < tuneJSON.tracks.length; i++) {
			for(var j = 0; j<tuneJSON.tracks[i].notes.length; j++){
				$tab = $('#track' + i);
				drawNote(tuneJSON.tracks[i].notes[j],$tab);
			}
		}
	}

	function drawNote(note,$tab) {
		//first we need to work out what bar note is in and where

		var subdivisions = tuneJSON.head.subdivisions * tuneJSON.head.barLength;
		var bar = Math.floor(note.position / subdivisions);
		var pitch =  midiHelper.convertPitchToIndex(note.pitch);
		var left = ((note.position % subdivisions) / subdivisions) * 100 + '%';//could potentially divide by 0 but js protects us
		var length = (note.length / subdivisions) * 100 + '%';
		console.log("bar " + bar);
		console.log("subdivisions " + subdivisions);
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
					var noteValue = Math.round($note.width() / $note.parent().width() * getSubdivisions());
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
				var subdivisions = getSubdivisions();
				pageData.previousLeft = Math.round(subdivisions * (ui.originalPosition.left / ui.element.parent().width()));
				pageData.previousLength = Math.round(subdivisions * (ui.originalElement.width() / ui.element.parent().width()));
				pageData.previousLeftRaw = ui.element.position().left;
				pageData.originalLeft = pageData.previousLeft;
				pageData.originalLength = pageData.previousLength;
			},
			resize : function(event,ui) {
				var subdivisions = getSubdivisions();//saves overhead of repeated function calls
				var left = Math.round(subdivisions * (ui.element.position().left / ui.element.parent().width()));
				var leftPercent = (left / subdivisions) * 100 + '%';
				var length;
				if(left === pageData.previousLeft) {
					if(ui.element.position().left !== pageData.previousLeftRaw) {
						length = pageData.previousLength;
					} else {
						length = Math.round(subdivisions * (ui.element.width() / ui.element.parent().width()));
					}
				} else {
					var leftDifference = left - pageData.previousLeft;
					console.log(leftDifference);
					length = pageData.previousLength - leftDifference;
				}
				var lengthPercent = (length / subdivisions) * 100 + '%';
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
					var originalLeft = (pageData.originalLeft / getSubdivisions()) * 100 + '%';
					var originalLength = (pageData.originalLength / getSubdivisions()) * 100 + '%';
					ui.element.css({
						'left' : originalLeft,
						'width' : originalLength
					});
					return;
				}	
				var id = $note.attr('id');	
				console.log(id);
				var oldNote = deleteNote(id);
				console.log(oldNote);	
				var trackInfo = {track : $('.tab-pane.active').index()};
				var deleteData = $.extend(oldNote,trackInfo)
				var deleteInfo = {topic : 'delete', data : deleteData};
				ajaxHelper.notifyServer(deleteInfo);
				pageData.quarantinedChanges.push(deleteInfo);
				var newId = generateId();
				$note.attr('id',newId);
				//need to put new size into a data and ajax it and update id of div
				var subdivisions = getSubdivisions();//saves overhead of repeated function calls
				var left = pageData.previousLeft;
				var bar = $note.parent().parent().index();
				var newPosition = bar * subdivisions + left;
				var newLength = pageData.previousLength;
				var newNoteData = {
					id : newId,
					position : newPosition,
					pitch : deleteData.pitch,
					length : newLength
				};
				tuneJSON.tracks[trackInfo.track].notes.push(newNoteData);
				var newNoteInfo = $.extend(newNoteData,trackInfo);
				var newNoteToSend = { topic: 'add',data : newNoteInfo};
				ajaxHelper.notifyServer(newNoteToSend);
				pageData.quarantinedChanges.push(newNoteToSend);
			}
			
		});
	}

	function getNoteValue($target) {
		var note;
		if($target.hasClass('note-crotchet')) {
			note = tuneJSON.head.subdivisions * noteValues.crotchet;
		} else if($target.hasClass('note-quaver')) {
			note = tuneJSON.head.subdivisions * noteValues.quaver;
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

	function generateId() {
		
		  function s4() {
		    return Math.floor((1 + Math.random()) * 0x10000)
		               .toString(16)
		               .substring(1);
		  }
		  return 'note-' + s4() + s4() + '-' + s4() + '-' + s4() + '-' +
		    s4() + '-' + s4() + s4() + s4();
		
		
	}

	function deleteNote(id) {
		id += ''; //make sure id is a string for comparisons
		var note;
	
		for(var i = 0; i < tuneJSON.tracks.length; i++) {
			for(var j = 0; j < tuneJSON.tracks[i].notes.length; j++) {
				if(tuneJSON.tracks[i].notes[j].id + '' === id) {//converts any numbers to strings for comparison
					note = tuneJSON.tracks[i].notes[j];
					tuneJSON.tracks[i].notes.splice(j,1);
				}
			}
		}
		return note;
	}

	function loadNotesFromJSON(data) {
		tuneJSON = data;
		loadCanvas();
	}

	function getToken() {
		ajaxHelper.getToken(function(token) {
			channelHelper.initSocket(token);
		});
	}

	function getSubdivisions() {
		return tuneJSON.head.subdivisions * tuneJSON.head.barLength;
	}

	function initEditor() {
		//first thing to do is set up loading page until we can establish a connection
		drawLoadScreen();
		getToken();
	}

	//what do we want to test? loading notes from JSON

	$(function() {
		initEditor();




	});