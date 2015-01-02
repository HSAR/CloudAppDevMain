var token = null;
var query = null;
var sort = null;

$(document).ready(function() {
	var ajax = new AjaxHandler();
	query = getUrlParam('query');
    $('#search-query').val(query);
	ajax.search(query, sort, token, showResults);
});

function getUrlParam(parameter) {
       var query = window.location.search.substring(1);
       var vars = query.split("&");
       for (var i=0;i<vars.length;i++) {
               var pair = vars[i].split("=");
               if(pair[0] == parameter){return pair[1];}
       }
       return(false);
}

var showResults = function(response) {
	if (!response) {
		//if this has happened, there's been an error.
        $('#results').append('<tr><td>No results found.</td><td></td><td></td><td></td></tr>');
    } else {
    	var results = response.results;
        token = response.token;
        sort = response.sort;
        
    	if (!results) {
			$('#results').append('<tr><td>No results found.</td><td></td><td></td><td></td></tr>');
			return;
		}
    	if (response.more) {
    		//enable next page link
    		$('#more-results').click(showMore());
    	} else {
    		$('#more-results').unbind('click');
    	}
	    for (var i = 0; i < results.length; i++) {
	        $('#results').append('<tr><td> <a href="http://jinglr-music.appspot.com/editor/' + results[i].title + '">' + results[i].title + '</a></td><td>' + results[i].owner + "</td><td>" + results[i].tags + "</td><td>" + results[i].genre + "</td></tr>");
	    }
	}
}

var showMore = function() {
    ajax.search(query, sort, token, showResults);
}