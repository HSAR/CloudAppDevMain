$( document ).ready(function() {
	//some auth stuff to get username
	var ajax = new AjaxHandler();
	ajax.setUserID('userID');
	ajax.getUserSongs(ownedSongs);
	ajax.getUserCollabs(collabSongs);
    ajax.getUserInvites(invitedSongs);
});

//Yeah, there's a lot of code repetition here, I'll get round to fixing that
var ownedSongs = function(response) {
    var data = jQuery.parseJSON(response);
    if (!data) {
        $('#ownedTable').append('<tr><td>No songs found. Why not create one?</td><td></td><td></td><td></td></tr>');

        //checking the code below is working
        data = [
            {title: "lol", 
            owner: "me", 
            tags: "rofl", 
            genre: "punk"
            id: "1234lemma"}];
    } 
    //uncomment else when done for real
    //else {
        for (var i = 0; i < data.length; i++) {
            //the parameter for unique ids might change
            $('#ownedTable').append('<tr><td> <a href="http://http://jinglr-music.appspot.com/editor/' + data[i].id + '">' + data[i].title + '</a></td><td>' + data[i].owner + "</td><td>" + data[i].tags + "</td><td>" + data[i].genre + "</td></tr>");
        }
    //}
}

var collabSongs = function(response) {
    var data = jQuery.parseJSON(response);
    if (!data) {
        $('#collabTable').append('<tr><td>No songs found. Start contributing!</td><td></td><td></td><td></td></tr>');
    } else {
        for (var i = 0; i < data.length; i++) {
            $('#collabTable').append('<tr><td> <a href="http://http://jinglr-music.appspot.com/editor/' + data[i].id + '">' + data[i].title + '</a></td><td>' + data[i].owner + "</td><td>" + data[i].tags + "</td><td>" + data[i].genre + "</td></tr>");
        }
    }
}

var invitedSongs = function(response) {
    var data = jQuery.parseJSON(response);
    if (!data) {
        $('#inviteTable').append('<tr><td>No invitiations.</td><td></td><td></td><td></td></tr>');
    } else {
        for (var i = 0; i < data.length; i++) {
            $('#inviteTable').append('<tr><td> <a href="http://http://jinglr-music.appspot.com/editor/' + data[i].id + '">' + data[i].title + '</a></td><td>' + data[i].owner + "</td><td>" + data[i].tags + "</td><td>" + data[i].genre + "</td></tr>");
        }
    }
}