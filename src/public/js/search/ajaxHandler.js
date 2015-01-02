function AjaxHandler() {
	this.search = function(query, sort, token, cb) {
		$.ajax({
			type : 'GET',
			url : 'http://jinglr-music.appspot.com/api/songs/search',
			data: { query: query, sort: sort, token: token },
			dataType : 'JSON',
			success : function(data) {
				console.log(data);
				if(data) {
					cb(data);
				} else {
					//deal with error here
				}
			},
			failure: cb(null)
		});
	};
}