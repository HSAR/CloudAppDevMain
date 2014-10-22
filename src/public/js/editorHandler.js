/*
Handler script for the music editor. Still in early stages
*/
var barHTML = '<div class="bar">' + '<div class="pitch"></div>'.repeat(12) + '</div>';


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

	});
}


$(function() {
	loadPalette();
	loadCanvas();



});