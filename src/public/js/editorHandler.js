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
				var noteValue = getNoteValue($(ui.helper));
				if(noteValue) {
					drawPreview(event,noteValue);
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
				$('.preview').remove();
			}
			$('.preview').addClass('music-note').removeClass('preview');

		}
	});
}

function drawPreview(event,noteLength) {
	//ok so we can use event.pageX - ui.offset and ignore ones where we get minus values as these are false events
	var distanceFromLeft = event.pageX - $('.preview').parent().offset().left;
	var width = $('.preview').parent().width();
	if(distanceFromLeft >=0) { //if we are dragging over the correct box
		var position = Math.floor((distanceFromLeft / width) * barLength);

		if(position + noteLength > barLength) {
			position = barLength - noteLength;//if overflows limit it to end of bar
		}
		var leftPos = ((position / barLength) * 100) + "%";
		var length = ((noteLength / barLength) * 100) + "%";

		$('.preview').css({
			"position" : 'absolute',
			'left' : leftPos,
			'width' : length,
			'visibility' : 'visable'
		});
		$('.preview').removeClass('no-display');
	}
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