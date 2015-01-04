function MidiHandler() {
	var instruments = [];
	var startingPitch = 48; //one octave below middle C

	instruments[1]  =	'Acoustic Grand Piano';
	instruments [2] =	'Bright Acoustic Piano';
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
	instruments [33] =	'Acoustic Bass';
	instruments [34] =	'Electric Bass (finger)';
	instruments [35] =	'Electric Bass (pick)';
	instruments [36] =	'Fretless Bass';
	instruments [37] =	'Slap Bass 1';
	instruments [38] =	'Slap Bass 2';
	instruments [39] =	'Synth Bass 1';
	instruments [40] =	'Synth Bass 2';
	instruments [41] =	'Violin';
	instruments [42] =	'Viola';
	instruments [43] =	'Cello';
	instruments [44] =	'Contrabass';
	instruments [45] =	'Tremolo Strings';
	instruments [46] =	'Pizzicato Strings';
	instruments [47] =	'Orchestral Harp';
	instruments [48] =	'Timpani';
	instruments [49] =	'String Ensemble 1';
	instruments [50] =	'String Ensemble 2';
	instruments [51] =	'SynthStrings 1';
	instruments [52] =	'SynthStrings 2';
	instruments [53] =	'Choir Aahs';
	instruments [54] =	'Voice Oohs';
	instruments [55] =	'Synth Voice';
	instruments [56] =	'Orchestra Hit';
	instruments [57] =	'Trumpet';
	instruments [58] =	'Trombone';
	instruments [59] =	'Tuba';
	instruments [60] =	'Muted Trumpet';
	instruments [61] =	'French Horn';
	instruments [62] =	'Brass Section';
	instruments [63] =	'SynthBrass 1';
	instruments [64] =	'SynthBrass 2';
	instruments [65] =	'Soprano Sax';
	instruments [66] =	'Alto Sax';
	instruments [67] =	'Tenor Sax';
	instruments [68] =	'Baritone Sax';
	instruments [69] =	'Oboe';
	instruments [70] =	'English Horn';
	instruments [71] =	'Bassoon';
	instruments [72] =	'Clarinet';
	instruments [73] =	'Piccolo';
	instruments [74] =	'Flute';
	instruments [75] =	'Recorder';
	instruments [76] =	'Pan Flute';
	instruments [77] =	'Blown Bottle';
	instruments [78] =	'Shakuhachi';
	instruments [79] =	'Whistle';
	instruments [80] =	'Ocarina';
	instruments [81] =	'Lead 1 (square)';
	instruments [82] =	'Lead 2 (sawtooth)';
	instruments [83] =	'Lead 3 (calliope)';
	instruments [84] =	'Lead 4 (chiff)';
	instruments [85] =	'Lead 5 (charang)';
	instruments [86] =	'Lead 6 (voice)';
	instruments [87] =	'Lead 7 (fifths)';
	instruments [88] =	'Lead 8 (bass + lead)';
	instruments [89] =	'Pad 1 (new age)';
	instruments [90] =	'Pad 2 (warm)';
	instruments [91] =	'Pad 3 (polysynth)';
	instruments [92] =	'Pad 4 (choir)';
	instruments [93] =	'Pad 5 (bowed)';
	instruments [94] =	'Pad 6 (metallic)';
	instruments [95] =	'Pad 7 (halo)';
	instruments [96] =	'Pad 8 (sweep)';
	instruments [97] =	'FX 1 (rain)';
	instruments [98] =	'FX 2 (soundtrack)';
	instruments [99] =	'FX 3 (crystal)';
	instruments [100]=	'FX 4 (atmosphere)';
	instruments [101]=	'FX 5 (brightness)';
	instruments [102]=	'FX 6 (goblins)';
	instruments [103]=	'FX 7 (echoes)';
	instruments [104]=	'FX 8 (sci-fi)';
	instruments [105]=	'Sitar';
	instruments [106]=	'Banjo';
	instruments [107]=	'Shamisen';
	instruments [108]=	'Koto';
	instruments [109]=	'Kalimba';
	instruments [110]=	'Bag pipe';
	instruments [111]=	'Fiddle';
	instruments [112]=	'Shanai';
	instruments [113]=	'Tinkle Bell';
	instruments [114]=	'Agogo';
	instruments [115]=	'Steel Drums';
	instruments [116]=	'Woodblock';
	instruments [117]=	'Taiko Drum';
	instruments [118]=	'Melodic Tom';
	instruments [119]=	'Synth Drum';
	instruments [120]=	'Reverse Cymbal';
	instruments [121]=	'Guitar Fret Noise';
	instruments [122]=	'Breath Noise';
	instruments [123]=	'Seashore';
	instruments [124]=	'Bird Tweet';
	instruments [125]=	'Telephone Ring';
	instruments [126]=	'Helicopter';
	instruments [127]=	'Applause';
	instruments [128]=	'Gunshot';
	
	this.getInstrumentName = function(number) {
		var name = instruments[number + 1];
		return name;//TODO check for exceptions
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


