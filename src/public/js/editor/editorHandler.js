	/*
	Handler script for the music editor. Still in early stages
	*/
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
		quaver : 1,
		crotchet : 2
	}

	var pageData = {
		scrollLeft : 0
	};

	var barLength = 8;

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
		console.log('test');
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
				$(event.target).append("<div class='preview no-display'></div>");
			},
			out : function(event,ui) {
				$(event.target).children('.preview').remove();
			},
			drop : function(event,ui) {
				//we need to reclass the preview div here and add it to the model

				//ajax some shit here

				//also need to handle two notes being dropped on top of each other.
				var conflict = false;
				$(event.target).children('.music-note').each(function(i) {
					var left = $(this).position().left;
					var right = left + $(this).width();

					var newLeft = $('.preview').position().left;
					var newRight = newLeft + $('.preview').width();
					console.log(left + " " + right + " " + newLeft + " " + newRight);
					if((left < newLeft && right > newLeft) || (left >= newLeft && left <= newRight )) {
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
						
					}
					
					//we need to turn preview's position into a json to send to server
					var left = $('.preview').position().left / $('.preview').parent().width();
					var width = $('.preview').width() / $('.preview').parent().width();
					var bar = $('.preview').parent().parent().index();//gets index of bar
					
					var subdivisions = (tuneJSON.head.barLength * tuneJSON.head.subdivisions)
					var notePosition = (bar * subdivisions) + Math.round(left * subdivisions);
					var noteLength = Math.round(width * subdivisions);
					var noteTrack = $('.tab-pane.active').index();
					var notePitch = midiHelper.convertIndexToPitch($('.preview').parent().index());
					var data = {
						topic : 'add',
						data : {
							pitch : notePitch,
							track : noteTrack,
							length : noteLength,
							position : notePitch
						}
					};
					addNoteUI($('.preview'));//make it draggable etc
					$('.preview').addClass('music-note').removeClass('preview');

					$.ajax({
						type : 'POST',
						url : 'http://example.com',
						data : data,
						dataType : 'JSON',
						success : function(data) {
							
						}
					});



				}
				

			}
		});
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
		var distanceFromLeft = event.pageX - $target.parent().offset().left;
		var width = $target.parent().width();
		if(distanceFromLeft >=0) { //if we are dragging over the correct box
			var position = Math.floor((distanceFromLeft / width) * barLength);

			if(position + noteLength > barLength) {
				position = barLength - noteLength;//if overflows limit it to end of bar
			}
			var leftPos = ((position / barLength) * 100) + "%";
			var length = ((noteLength / barLength) * 100) + "%";

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
				if(i === 1) {
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
				if(i === 1) {
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
		$tab.children('.bar').eq(bar).children('.pitch').eq(pitch).append('<div class="newNote" id="note' + note.id +'"></div>');

		$('.newNote').css({
			'position' : 'absolute',
			'left' : left,
			'width' : length
		});
		console.log($('.newNote').attr('id'));
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
					var noteValue = 2;
					if(noteValue) {
						drawPreview(event,noteValue,$('.preview'));
					}
					
				}
			} 
		});
		// $note.resizable({

		// });
	}

	function getNoteValue($target) {
		var note;
		if($target.hasClass('note-crotchet')) {
			note = noteValues.crotchet;
		} else if($target.hasClass('note-quaver')) {
			note = noteValues.quaver;
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

	function initEditor() {
		//first thing to do is set up loading page until we can establish a connection
		drawLoadScreen();
		getToken();
	}

	//what do we want to test? loading notes from JSON

	$(function() {
		initEditor();




	});