function AjaxHandler() {
	this.getToken = function(cb) {
		$.ajax({
			type : 'GET',
			url : 'http://jinglr-test.appspot.com/auth/token',
			dataType : 'JSON',
			success : function(data) {
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
			url : 'http://jinglr-test.appspot.com/auth/token',
			dataType : 'JSON',
			success : function(data) {
				if(data.topic === 'tune') {
					//we can now open up a socket using the token
					
					cb(data);
				} else {
					//deal with error here
				}
			}
		});
	};
	this.notifyServer = function(data) {
		var targetURL;
		switch(data.topic) {
			case 'add':
				url = 'http://example-add.com';
				break;
			case 'delete':
				url = 'http://example-delete.com';
				break;
			case 'edit':
				url = 'http://example-edit.com';
				break;

			default :
				//put error case here
				break;		
		}
		console.log(data);
		$.ajax({
				type : 'POST',
				url : targetURL,
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
			url : 'http://example-play.com',
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

}