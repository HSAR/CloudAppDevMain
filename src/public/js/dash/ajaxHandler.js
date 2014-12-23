var userID = null;

function AjaxHandler() {
	this.setUserID = function(id) {
		userID = id;
		$("#dashTitle h3 #userHeader").text(" " + userID + "'s Dashboard");
		$("#userWelcome").text("Welcome, " + userID)
	}

	//yet more code repetition - this really could be one function...
	this.getUserByID = function(cb) {
		$.ajax({
			type : 'GET',
			url : 'http://localhost:8080/users/' + userID + "/",
			dataType : 'JSON',
			success : function(data) {
				console.log(data);
				if(data) {
					console.log('got user info');
					//perhaps we should do something with this entity.
					//christ knows what
				} else {
					//deal with error here
				}
			}
		});
	};
	this.getUserSongs = function(cb) {
		$.ajax({
			type : 'GET',
			url : 'http://localhost:8080/users/' + userID + '/songs',
			dataType : 'JSON',
			success : function(data) {
				console.log(data);
				if(data) {
					cb(data);
				} else {
					//deal with error here
				}
			},
			failure : cb(null)
		});
	};
	this.getUserCollabs = function(cb) {
		//gets songs user has collaborated on
		$.ajax({
			type : 'GET',
			url : 'http://localhost:8080/users/' + userID + '/collabs',
			dataType: 'JSON',
			success : function(data) {
				if(data) {
					//do some tings
					cb(data);
				} else {
					//deal with error here
				}
			},
			failure : cb(null)
		});
	};

	this.getUserInvites = function(cb) {
		$.ajax({
			type : 'GET',
			url : 'http://localhost:8080/users/' + userID + '/invites',
			dataType  : 'JSON',
			success : function(data) {
				if (data) {
					cb(data);
				} else {
					//#failwhale
				}
			},
			failure : cb(null)
		});
	}

}