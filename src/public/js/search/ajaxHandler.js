function AjaxHandler() {
	this.search = function(query, sort, token, cb, error) {
		$.ajax({
			type : 'GET',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/search',
			data: { query: query, sort: sort, token: token },
			dataType : 'JSON',
			success : function(data) {
				cb(data);
			}
			//failure case is fired every time for some reason, so removed
		});
	};
}
