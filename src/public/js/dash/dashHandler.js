$( document ).ready(function() {
	//some auth stuff to get username
	var ajax = new AjaxHandler();
	ajax.setUserID('userID');
	ajax.getUserSongs(ownedSongs);
	ajax.getUserCollabs(collabSongs);
});

var ownedSongs = function(response) {
    var data = jQuery.parseJSON(response);
    if (!data) {
        $('#ownedTable').append('<tr><td>No songs found. Why not create one?</td><td></td><td></td><td></td></tr>');
    } else {
        for (var i = 0; i < data.length; i++) {
            $('#ownedTable').append("<tr><td>" + data.i.title + "</td><td>" + data.i.owner + "</td><td>" + data.i.tags + "</td><td>" + data.i.genre + "</td></tr>");
        }
    }
}

var collabSongs = function(response) {
    var data = jQuery.parseJSON(response);
    if (!data) {
        $('#collabTable').append('<tr><td>No songs found. Start contributing!</td><td></td><td></td><td></td></tr>');
    } else {
        for (var i = 0; i < data.length; i++) {
            $('#collabTable').append("<tr><td>" + data.i.title + "</td><td>" + data.i.owner + "</td><td>" + data.i.tags + "</td><td>" + data.i.genre + "</td></tr>");
        }
    }
}