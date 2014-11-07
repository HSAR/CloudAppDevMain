function AjaxHandler() {
	this.getToken = function(cb) {
		$.ajax({
			type : 'GET',
			url : 'http://example.com',
			dataType : 'JSON',
			success : function(data) {
				if(data.token) {
					//we can now open up a socket using the token
					cb(data.token);
				} else {
					//deal with error here
				}
			}

		});
	};
	this.notifySever = function(data) {
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