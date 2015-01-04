function AjaxHandler() {
	this.search = function(query, sort, token, tag, cb, error) {
		var data = {};
		if (tags) {
			data.tag = tag;
		} else {
			data.query = query;
		}
		data.sort = sort;
		data.token = token;
		$.ajax({
			type : 'GET',
			url : window.location.protocol + '//' + window.location.host + '/api/songs/search',
			data: data,
			dataType : 'JSON',
			success : function(data) {
				cb(data);
			}
			//failure case is fired every time for some reason, so removed
		});
	};
}
