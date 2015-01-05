/**
Handler class containing midi utiliies, such as converting an istrument number to name etc
*/
function MidiHandler() {
	var instruments = [];
	var startingPitch = 48; //one octave below middle C

	instruments = [ 'Invalid Instrument', 'Acoustic Grand Piano', 'Bright Acoustic Piano', 'Electric Grand Piano', 'Honky-tonk Piano',
	'Rhodes Piano', 'Chorused Piano', 'Harpsichord', 'Clavinet', 'Celesta', 'Glockenspiel', 'Music Box', 'Vibraphone', 'Marimba', 'Xylophone',
	'Tubular Bells', 'Dulcimer', 'Hammond Organ', 'Percussive Organ', 'Rock Organ', 'Church Organ', 'Reed Organ', 'Accordion', 'Harmonica',
	'Tango Accordion', 'Acoustic Nylon Guitar', 'Acoustic Steel Guitar', 'Electric Jazz Guitar', 'Electric Clean Guitar',
	'Electric Muted Guitar', 'Overdriven Guitar', 'Distortion Guitar', 'Guitar Harmonics', 'Acoustic Bass', 'Electric Bass (finger)',
	'Electric Bass (pick)', 'Fretless Bass', 'Slap Bass 1', 'Slap Bass 2', 'Synth Bass 1', 'Synth Bass 2', 'Violin', 'Viola', 'Cello',
	'Contrabass', 'Tremolo Strings', 'Pizzicato Strings', 'Orchestral Harp', 'Timpani', 'String Ensemble 1', 'String Ensemble 2',
	'SynthStrings 1', 'SynthStrings 2', 'Choir Aahs', 'Voice Oohs', 'Synth Voice', 'Orchestra Hit', 'Trumpet', 'Trombone', 'Tuba',
	'Muted Trumpet', 'French Horn', 'Brass Section', 'SynthBrass 1', 'SynthBrass 2', 'Soprano Sax', 'Alto Sax', 'Tenor Sax', 'Baritone Sax',
	'Oboe', 'English Horn', 'Bassoon', 'Clarinet', 'Piccolo', 'Flute', 'Recorder', 'Pan Flute', 'Blown Bottle', 'Shakuhachi', 'Whistle',
	'Ocarina', 'Lead 1 (square)', 'Lead 2 (sawtooth)', 'Lead 3 (calliope)', 'Lead 4 (chiff)', 'Lead 5 (charang)', 'Lead 6 (voice)',
	'Lead 7 (fifths)', 'Lead 8 (bass + lead)', 'Pad 1 (new age)', 'Pad 2 (warm)', 'Pad 3 (polysynth)', 'Pad 4 (choir)', 'Pad 5 (bowed)',
	'Pad 6 (metallic)', 'Pad 7 (halo)', 'Pad 8 (sweep)', 'FX 1 (rain)', 'FX 2 (soundtrack)', 'FX 3 (crystal)', 'FX 4 (atmosphere)',
	'FX 5 (brightness)', 'FX 6 (goblins)', 'FX 7 (echoes)', 'FX 8 (sci-fi)', 'Sitar', 'Banjo', 'Shamisen', 'Koto', 'Kalimba',
	'Bag pipe', 'Fiddle', 'Shanai', 'Tinkle Bell', 'Agogo', 'Steel Drums', 'Woodblock', 'Taiko Drum', 'Melodic Tom', 'Synth Drum',
	'Reverse Cymbal', 'Guitar Fret Noise', 'Breath Noise', 'Seashore', 'Bird Tweet', 'Telephone Ring', 'Helicopter', 'Applause', 'Gunshot']
	
	this.getInstrumentName = function(number) {
		var name = instruments[number + 1];
		return name;
	}

	
	this.convertPitchToIndex = function(pitch) {
		//takes a midi pitch number and converts it to index of pitch div in dom
		var index = 36 - (pitch - startingPitch);
		return index;
	}

	this.convertIndexToPitch = function(index) {
		return (36 - index) + startingPitch;
	}

	this.writeKey = function() {
		htmlString = '<div class="key">';
		for(var i = 0; i < 37; i++) {
			var pitch;
			var note;
			if(i == 0) {
				pitch = "Very High";
			}
			else if(i <= 12) {
				pitch = "High";
			} else if(i <= 24) {
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


