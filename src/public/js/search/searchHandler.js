var token = null;
var query = null;
var sort = null;

var init = function() {
	var ajax = new AjaxHandler();
	query = getUrlParam('query');
  sort = getUrlParam('sort');
  $('#search-query').val(query);
  $('a.sort-link').click(function() {
    var sortRule = $(this).attr('id').substring(5);//get what to sort by
    ajax.search(query,sortRule,null,showResults);//update results to be sorted in specified way
  });
	ajax.search(query, sort, token, showResults);

}

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
	$('#results tbody').empty();//clear existing results
  if (!response) {
		//if this has happened, there's been an error.
        $('#results tbody').append('<tr><td>No results found.</td><td></td><td></td><td></td></tr>');
    } else {
    	var results = response.results;
        token = response.token;
        sort = response.sort;
        
    	if (!results || results[0] == null) {
			$('#results tbody').append('<tr><td>No results found.</td><td></td><td></td><td></td></tr>');
			return;
		}
    	if (response.more) {
    		//enable next page link
    		$('#more-results').click(showMore);
    	} else {
    		$('#more-results').unbind('click');
    	}
	    for (var i = 0; i < results.length; i++) {
	        var staticPlayer = new StaticPlayer();
            staticPlayer.loadFile(window.location.protocol + '//' + window.location.host + '/api/songs/' + results[i].jingle_id + '/midi');
          var resultDate = new Date(results[i].date_created * 1000);
          $('#results tbody').append(
                '<tr><td>' + results[i].title + '</td>'
                + '<td><a href="/web/users/' + results[i].author + '">' + results[i].username + '</a></td>'
                + '<td>'+ results[i].tags + '</td>'
                + '<td>' + results[i].genre + '</td>'
                + '<td>' + resultDate.toLocaleDateString() + '<td>'
                + "<td class='preview" + results[i].jingle_id + "'></td></tr>");
          staticPlayer.attach($('td.preview' + results[i].jingle_id).eq(0));
	    }
	}
}

var showMore = function() {
    ajax.search(query, sort, token, showResults);
}
