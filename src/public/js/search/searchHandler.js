$( document ).ready(function() {
	var ajax = new AjaxHandler();
	ajax.search(showResults);
});

var showResults = function(response) {
	var data = jQuery.parseJSON(response);
	if (!data) {
        $('#results').append('<tr><td>No songs found. Why not create one?</td><td></td><td></td><td></td></tr>');
    } else {
	    for (var i = 0; i < data.length; i++) {
	        $('#results').append('<tr><td> <a href="http://localhost:8080/editor/' + data[i].title + '">' + data[i].title + '</a></td><td>' + data[i].owner + "</td><td>" + data[i].tags + "</td><td>" + data[i].genre + "</td></tr>");
	        //need to deal with pagination
	    }
	}
}