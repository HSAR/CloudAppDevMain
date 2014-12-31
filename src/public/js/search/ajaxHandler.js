function AjaxHandler() {
	this.search = function(query, cb) {
		$.ajax({
			type : 'GET',
			url : 'http://jinglr-music.appspot.com/api/search/' + query,
			dataType : 'JSON',
			success : function(data) {
				console.log(data);
				if(data) {
					console.log('results found for ' + query);
					cb(data);
				} else {
					//deal with error here
				}
			},
			failure: cb(null)
		});
	};
}