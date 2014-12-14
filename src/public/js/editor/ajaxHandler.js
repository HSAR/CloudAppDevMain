function AjaxHandler() {
	this.getToken = function(cb) {
		$.ajax({
			type : 'GET',
			url : 'http://localhost:9080/auth/token',
			dataType : 'JSON',
			success : function(data) {
				console.log(data);
				if(data.token) {
					console.log('token retreived via ajax');
					//we can now open up a socket using the token
					cb(data.token);
				} else {
					//deal with error here
				}
			}

		});
	};
	this.getTuneJSON = function(cb) {
		$.ajax({
			type : 'GET',
			url : 'http://localhost:9080/songs/0',
			dataType : 'JSON',
			success : function(data) {
				console.log(data);
				if(data) {
					//we can now open up a socket using the token
					cb(data);
				} else {
					//deal with error here
				}
			}
		});
	};
	this.notifyServer = function(data) {
		var url;
		switch(data.topic) {
			case 'add':
				url = 'http://jinglr-music.appspot.com/tune/add';
				break;
			case 'delete':
				url = 'http://jinglr-music.appspot.com/tune/delete';
				break;
			case 'edit':
				url = 'http://example-edit.com';
				break;

			default :
				console.log("Ajax error");
				console.log(data);
				return;
				//put error case here
				break;		
		}
		console.log(data);
		console.log(url);
		$.ajax({
				type : 'POST',
				url : url,
				data : data,
				dataType : 'JSON',
				success : function() {
					//TODO	
				}
			});
	};
	this.compileTune = function(cb) {
		//asks the server to compile the tune into a midi file and send it back
		$.ajax({
			type : 'GET',
			url : 'http://localhost:9080/songs/0/midi',
			success : function(data) {
				if(true) {
					//TODO add some file validation here
					cb(data);
				} else {
					//deal with error here
				}
			}
		});
	};

	this.changeInstrument = function(data) {
		$.ajax({
			type : 'POST',
			url : 'http://example-change.com',
			data  : data,
			success : function() {
				//TODO
			}
		});
	}

	this.addInstrument = function(data) {
		$.ajax({
			type : 'POST',
			url : 'http://example-cadd-instrument.com',
			data  : data,
			success : function() {
				//TODO
			}
		});
	}

	this.deleteInstrument = function(data) {
		$.ajax({
			type : 'POST',
			url : 'http://example-delete-instrument.com',
			data  : data,
			success : function() {
				//TODO
			}
		})
	}

}