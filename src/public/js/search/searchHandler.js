//passed into the search ajax request
var token,
    query,
    sort,
    tag;

var init = function() {
	ajax = new AjaxHandler();
	sort = getUrlParam('sort');
	query = getUrlParam('query');
	tag = getUrlParam('tag');
	if (query) {
		$('#search-query').val(query);
	} else if (tag) {
		$('#search-query').val(tag);
	}
    $('#more-results').hide();
	$('a.sort-link').click(function() {
		var sortRule = $(this).attr('id').substring(5);//get what to sort by
		ajax.search(query, sortRule, null, tag, showResults, ajaxFailure);//update results to be sorted in specified way
	});
	ajax.search(query, sort, token, tag, showResults, ajaxFailure);
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

var showResults = function(response, token) {
    //don't clear the table if we're continuing a search
    if (!token) {
        $('#results tbody').empty();//clear existing results
    }
	var results = response.results;
		token = response.token;
		sort = response.sort;
		
	if (!results || results[0] == null) {
		$('#results tbody').append('<tr><td>No results found.</td><td></td><td></td><td></td></tr>');
		return;
	}
	if (response.more) {
		//enable next page link
		$('#more-results').click(function() {
            ajax.search(query, sort, token, tag, showResults, ajaxFailure);
        });
        $('#more-results').show();
	} else {
        //disable and hide link
		$('#more-results').unbind('click');
        $('#more-results').hide();
	}
	for (var i = 0; i < results.length; i++) {
		var staticPlayer = new StaticPlayer();
		staticPlayer.loadFile(window.location.protocol + '//' + window.location.host + '/api/songs/' + results[i].jingle_id + '/midi');
		var resultDate = new Date(results[i].date_created * 1000);
		var resultGenre = results[i].genre;
		if (resultGenre === null) {
			resultGenre = new String("");
		}
		$('#results tbody').append(
			'<tr><td>' + results[i].title + '</td>'
			+ '<td><a href="/web/users/' + results[i].author + '">' + results[i].username + '</a></td>'
			+ '<td>'+ results[i].tags + '</td>'
			+ '<td>' + resultGenre + '</td>'
			+ '<td>' + resultDate.toLocaleDateString() + '</td>'
			+ "<td class='preview" + results[i].jingle_id + "'></td></tr>"
		);
		staticPlayer.attach($('td.preview' + results[i].jingle_id).eq(0));
	}

}