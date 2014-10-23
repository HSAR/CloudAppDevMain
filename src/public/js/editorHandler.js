/*
Handler script for the music editor. Still in early stages
*/
var barHTML = '<div class="bar">' + '<div class="pitch"></div>'.repeat(12) + '</div>';

var noteValues = {
	quaver : 1,
	crotchet : 2
}

function loadPalette() {
	//we need to load the pallete items and then make em draggable etc.
	$('.editor .note').draggable({
		helper : 'clone',
		appendTo : 'body',
		revert : 'invalid'
	}); //could be a dangerous game as moved out of pallete
	//console.log($('.pallete'))
	console.log('test');
}

function loadCanvas() {
	for(var i = 1; i<9; i++) {
		$('.canvas').append(barHTML);
	}
	
	$('.canvas').droppable({
		over : function(event,ui) {
			var note;
			if(ui.draggable.hasClass('note-crotchet')) {
				note = noteValues.crotchet;
			} else if(ui.draggable.hasClass('note-quaver')) {
				note = noteValues.quaver;
			}
			drawPreview($(this),ui,note);
		}
	});
}

function drawPreview($target,ui,noteLength) {
	
}


$(function() {
	loadPalette();
	loadCanvas();



});