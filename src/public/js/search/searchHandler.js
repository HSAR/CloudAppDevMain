$(document).ready(function() {
	var ajax = new AjaxHandler();
	ajax.search(getQueryVariable(), showResults);
});

function getQueryVariable() {
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == "query"){return pair[1];}
       }
       return(false);
}

var showResults = function(response) {
	var data = jQuery.parseJSON(response);
	if (!data) {
        $('#results').append('<tr><td>No reults found.</td><td></td><td></td><td></td></tr>');
    } else {
	    for (var i = 0; i < data.length; i++) {
	        $('#results').append('<tr><td> <a href="http://jinglr-music.appspot.com/editor/' + data[i].title + '">' + data[i].title + '</a></td><td>' + data[i].owner + "</td><td>" + data[i].tags + "</td><td>" + data[i].genre + "</td></tr>");
	        //need to deal with pagination
	    }
	}
}