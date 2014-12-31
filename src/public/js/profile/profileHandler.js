$( document ).ready(function() {
    var path = window.location.pathname;
	var ajax = new AjaxHandler();

    ajax.getUser(path, userData);
	ajax.getUserSongs(path, ownedSongs);
	ajax.getUserCollabs(path, collabSongs);
    ajax.getUserInvites(path, invitedSongs);

    //if user is viewing own profile, allow editing
    if (currentUserEntity.user_id === path.split("/")[1]) {
        //display edit button
    }
});

var userData = function(response) {
    var data = jQuery.parseJSON(response);
    if (!data) {
        data = {username: "testuserplsignore", user_id: "testuidplsignore" }; //test case
    } 
    $("#profileTitle h3 #userHeader").text(" " + data.username + "'s Profile");
    //$("#bio").text(data.bio);
    //$("#tags").text(data.tags);
    
}
var ownedSongs = function(response) {
    writeToTable(songTables.owned, response);
}

var collabSongs = function(response) {
    writeToTable(songTables.collab, response);
}

var writeToTable = function(table, response) {
    var data = jQuery.parseJSON(response);
    if (!data) {
        $(table).append('<tr><td>'+ songTableEmptyMessage[table] +'</td><td></td><td></td><td></td></tr>');
    } else {
        for (var i = 0; i < data.length; i++) {
            $(table).append('<tr><td> <a href="http://jinglr-music.appspot.com/editor/' + data[i].id + '">' + data[i].title + '</a></td><td>' + data[i].owner + "</td><td>" + data[i].tags + "</td><td>" + data[i].genre + "</td></tr>");
        }
    }
}

var songTables = {
    owned: '#ownedTable',
    collab: '#collabTable',
    invites: '#inviteTable'
}

var songTableEmptyMessage = {
    '#ownedTable': 'User has not created any songs</a>',
    '#collabTable': 'User has not contributed to any songs',
}