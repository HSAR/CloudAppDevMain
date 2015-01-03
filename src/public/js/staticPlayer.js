function StaticPlayer() {
	//the html appended to the page for the player
	this.playerHTML = '<div class="playback-panel"><button class="play-button fresh-button"><span class="glyphicon glyphicon-play"></span></button>';
	this.compiledFile = null;
	this.instruments = null;
	this.ready = false;//whether player is ready to play

	var handler = this;//to refer to class inside event scope

	this.loadFile = function(url) {
		$.ajax({
			url : url,
			type : 'GET',
			success : function(data) {
				parsedData = JSON.parse(data);
				handler.compiledFile = parsedData.midi;
				handler.instruments = parsedData.instruments;
				console.log(parsedData);
			}
		});
	}

	this.attach = function($target) {
		$target.append(this.playerHTML);
		$('button.fresh-button').click(function() {
			handler.loadMidi(function(){
				if(handler.ready && (!MIDI.Player.playing)) {//if we have something to play and not already playing
					handler.ready = false;//reset ready flag
					MIDI.Player.stop();//cancel anything already playing
					MIDI.Player.start();//and begin playback
				}
				
				
			});
		});
			
		
		$('button.play-button').removeClass("fresh-button");//remove tag used to identify new button
	}

	this.loadMidi = function(cb) {//internal method called on play button click
		if(MIDI) {
			console.log(this);
			MIDI.Player.loadFile('data:audio/midi;base64,' + this.compiledFile,function() {
				MIDI.loadPlugin({
					soundfontUrl : '/public/soundfonts/',
					instruments : this.instruments,
					callback : function() {
						for(var i = 0; i < handler.instruments.length; i++) {
							
							if(i < 9) {
								MIDI.programChange(i,handler.instruments[i]);
							} else {
								MIDI.programChange(i + 1,handler.instruments[i]);
							}
							
						}
						handler.ready = true;
						cb();
					}
				});

			});
		}
	}

}