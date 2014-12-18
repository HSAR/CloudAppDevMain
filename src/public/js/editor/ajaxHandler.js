function AjaxHandler() {
	this.getToken = function(id,cb) {
		$.ajax({
			type : 'GET',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/token',
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
	this.getTuneJSON = function(id,cb) {
		$.ajax({
			type : 'GET',
			url : 'http://jinglr-music.appspot.com/songs/' + id,
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
	this.notifyServer = function(id,data) {
		var url;
		var type = null;
		switch(data.topic) {
			case 'add':
				url = 'http://jinglr-music.appspot.com/songs/' + id + '/notes';
				type = 'PUT';
				break;
			case 'delete':
				url = 'http://jinglr-music.appspot.com/songs/' + id + '/notes'
				type = 'DELETE'
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
				type : type,
				url : url,
				data : data,
				dataType : 'JSON',
				success : function() {
					//TODO	
				}
			});
	};
	this.compileTune = function(id,cb) {
		//asks the server to compile the tune into a midi file and send it back
		$.ajax({
			type : 'GET',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/midi',
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

	this.changeInstrument = function(id,data) {
		$.ajax({
			type : 'PATCH',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/instruments',
			data  : data,
			success : function() {
				//TODO
			}
		});
	}

	this.addInstrument = function(id,data) {
		$.ajax({
			type : 'PUT',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/instruments',
			data  : data,
			success : function() {
				//TODO
			}
		});
	}

	this.deleteInstrument = function(id,data) {
		$.ajax({
			type : 'DELETE',
			url : 'http://jinglr-music.appspot.com/songs/' + id + '/instruments',
			data  : data,
			success : function() {
				//TODO
			}
		});
	}

}