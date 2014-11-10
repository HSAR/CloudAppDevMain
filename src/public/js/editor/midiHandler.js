function MidiHandler() {
	var instruments = [];
	var startingPitch = 48; //one octave below middle C

	instruments[1]  = 'Acoustic Grand Piano';
	instruments [2] = 'Bright Acoustic Piano';
	instruments [3] =	'Electric Grand Piano';
	instruments [4] =	'Honky-tonk Piano';
	instruments [5] = 	'Rhodes Piano';
	instruments [6] = 	'Chorused Piano';
	instruments [7] =	'Harpsichord';
	instruments [8] =	'Clavinet';
	instruments [9] = 	'Celesta';
	instruments [10] =	'Glockenspiel';
	instruments [11] =	'Music Box';
	instruments [12] =	'Vibraphone';
	instruments [13] =	'Marimba';
	instruments [14] =	'Xylophone';
	instruments [15] =	'Tubular Bells';
	instruments [16] =	'Dulcimer';
	instruments [17] =	'Hammond Organ';
	instruments [18] =	'Percussive Organ';
	instruments [19] =	'Rock Organ';
	instruments [20] =	'Church Organ';
	instruments [21] =	'Reed Organ';
	instruments [22] =	'Accordion';
	instruments [23] =	'Harmonica';
	instruments [24] =	'Tango Accordion';
	instruments [25] =	'Acoustic Nylon Guitar';
	instruments [26] =	'Acoustic Steel Guitar';
	instruments [27] =	'Electric Jazz Guitar';
	instruments [28] =	'Electric Clean Guitar';
	instruments [29] =	'Electric Muted Guitar';
	instruments [30] =	'Overdriven Guitar';
	instruments [31] =	'Distortion Guitar';
	instruments [32] =	'Guitar Harmonics';

	this.getInstrumentName = function(number) {
		var name = instruments[number];
		return name;//TODO check for exceptions
	}

	
	this.convertPitchToIndex = function(pitch) {
		//takes a midi pitch number and converts it to index of pitch div in dom
		var index = 35 - (pitch - startingPitch);
		return index;
	}

	this.convertIndexToPitch = function(index) {
		return (35 - index) + startingPitch;
	}

	this.writeKey = function() {
		htmlString = '<div class="key">';
		for(var i = 0; i < 36; i++) {
			var pitch;
			var note;
			if(i < 12) {
				pitch = "High";
			} else if(i < 24) {
				pitch = "Middle";
			} else {
				pitch = "Low";
			}
			if(i%12 === 0) {
				note = "C";
			} else if(i%12 === 1) {
				note = "B";
			} else if(i%12 === 2) {
				note = "A#";
			} else if(i%12 === 3) {
				note = "A";
			} else if(i%12 === 4) {
				note = "G#";
			} else if(i%12 === 5) {
				note = "G";
			} else if(i%12 === 6) {
				note = "F#";
			} else if(i%12 === 7) {
				note = "F";
			} else if(i%12 === 8) {
				note = "E";
			} else if(i%12 === 9) {
				note = "D#";
			} else if(i%12 === 10) {
				note = "D";
			} else {
				note = "C#";
			}
			htmlString += '<div class="key-pitch">' + pitch + ' ' + note + "</div>"; 
		}
		htmlString += '</div>';
		return htmlString;
	};
	
}


