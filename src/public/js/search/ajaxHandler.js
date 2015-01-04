function AjaxHandler() {
	this.search = function(query, sort, token, tag, cb, error) {
		var data = {};
		if (tag) {
			data.tag = tag;
		} else if (query) {
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
			},
			error : function(data) {
				error(data);
			}
		});
	};
}
