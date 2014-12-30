$( document ).ready(function() {
    $("#dashTitle h3 #userHeader").text(" " + currentUserEntity.username + "'s Dashboard");
	var ajax = new AjaxHandler();
	ajax.getUserSongs(ownedSongs);
	ajax.getUserCollabs(collabSongs);
    ajax.getUserInvites(invitedSongs);
});


var ownedSongs = function(response) {
    writeToTable(songTables.owned, response);
}

var collabSongs = function(response) {
    writeToTable(songTables.collab, response);
}

var invitedSongs = function(response) {
    writeToTable(songTables.invites, response);
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
    '#ownedTable': 'No songs found. Why not <a href="#" data-toggle="modal" data-target="#createJingleModal">create one?</a>',
    '#collabTable': 'No collaborations found. Start contributing!',
    '#inviteTable': 'No pending invitations'
}