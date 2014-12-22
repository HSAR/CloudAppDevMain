function AjaxHandler() {
	this.search = function(cb) {
		$.ajax({
			type : 'GET',
			url : 'http://localhost:8080/search/' + query,
			dataType : 'JSON',
			success : function(data) {
				console.log(data);
				if(data) {
					console.log('results found for ' + query);
					//at this point we need to populate the results table
					cb(data);
				} else {
					//deal with error here
				}
			}

		});
	};
}