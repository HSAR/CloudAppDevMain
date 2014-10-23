/*
Handler script for the music editor. Still in early stages
*/
String.prototype.repeat = function( num )
{
    return new Array( num + 1 ).join( this );
}



var barHTML = '<div class="bar">' + '<div class="pitch"></div>'.repeat(12) + '</div>';

var noteValues = {
	quaver : 1,
	crotchet : 2
}

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
				var noteValue = getNoteValue($(this));
				if(noteValue) {
					drawPreview(ui.offset,noteValue);
				}
				
			}
		}
	}); //could be a dangerous game as moved out of pallete
	//console.log($('.pallete'))
	console.log('test');
}

function loadCanvas() {
	for(var i = 1; i<9; i++) {
		$('.canvas').append(barHTML);
	}
	
	$('.pitch').droppable({
		over : function(event,ui) {
			var note;
			if(ui.draggable.hasClass('note-crotchet')) {
				note = noteValues.crotchet;
			} else if(ui.draggable.hasClass('note-quaver')) {
				note = noteValues.quaver;
			}
			//rawPreview($(this),ui,note);
			console.log($(this).offset());
			console.log(event.pageX + "   " + event.pageY);
		}
	});
}

function drawPreview(offset,noteLength) {
	//ok so we can use event.pageX - ui.offset and ignore ones where we get minus values as these are false events
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


$(function() {
	loadPalette();
	loadCanvas();



});