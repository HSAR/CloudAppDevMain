function AjaxHandler() {
	this.getUser = function(path, cb, error) {
		commonAjax(window.location.protocol + '//' + window.location.host + '/api/users/' + path, cb, error);
	};

	this.getUserSongs = function(path, cb, error) {
		commonAjax(window.location.protocol + '//' + window.location.host + '/api/users/' + path + '/songs', cb, error);
	};
	
	this.getUserCollabs = function(path, cb, error) {
		commonAjax(window.location.protocol + '//' + window.location.host + '/api/users/' + path + '/collabs', cb, error);
	};

	this.updateProfile = function(uid, data) {
		$.ajax({
			type : 'PATCH',
			url : window.location.protocol + '//' + window.location.host + '/api/users/' + uid,
			data : JSON.stringify(data),
			success : function(data) {
				console.log("success");
				console.log(data);
			},
			error : function(data, something, something2) {
				console.log("failure");
				console.log(data);
				console.log(something);
				console.log(something2);
			}
		});
	}
}
