function StaticPlayer() {
	//the html appended to the page for the player
	this.playerHTML = '<div class="playback-panel"><button class="play-button fresh-button"><span class="glyphicon glyphicon-play"></span></button>';
	this.compiledFile = null;
	this.instruments = null;
	this.ready = false;//whether player is ready to play

	var preload = new Image();
	preload.src = '/public/img/player-load.gif';//preload loading spinner for smoothness
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
			var $button = $(this);
			$button.html('<img src="/public/img/player-load.gif"></img>');
			setTimeout(function() {
				$button.html('<span class="glyphicon glyphicon-play"></span>');
			},12000);//stop displaying loading sign if timed out
			handler.loadMidi(function(){
				if(handler.ready && (!MIDI.Player.playing)) {//if we have something to play and not already playing
					handler.ready = false;//reset ready flag
					MIDI.Player.stop();//cancel anything already playing
					$button.html('<span class="glyphicon glyphicon-play"></span>');
					MIDI.Player.start();//and begin playback
				}
				
				
			});
		});
			
		
		$('button.play-button').removeClass("fresh-button");//remove tag used to identify new button
	}

	this.loadMidi = function(cb) {//internal method called on play button click
		if(MIDI) {
			handler.requiredInstruments = [];
			for(var i = 0; i < handler.instruments.length; i++) {
				handler.requiredInstruments.push(handler.instruments[i].instrument);
			}
			MIDI.Player.loadFile('data:audio/midi;base64,' + this.compiledFile,function() {
				MIDI.loadPlugin({
					soundfontUrl : '/public/soundfonts/',
					instruments : handler.requiredInstruments,
					callback : function() {
						for(var i = 0; i < handler.instruments.length; i++) {
							var trackNum = handler.instruments[i].track;
							if(trackNum < 9) {
								MIDI.programChange(trackNum,handler.instruments[i].instrument);
							} else {
								MIDI.programChange(trackNum + 1,handler.instruments[i].instrument);
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