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
    if (!response) {
        $(table).append('<tr><td>'+ songTableEmptyMessage[table] +'</td><td></td><td></td><td></td></tr>');
    } else {
        for (var i = 0; i < response.length; i++) {
            $(table).append('<tr><td> <a href="http://jinglr-music.appspot.com/editor/' + response[i].id + '">' + response[i].title + '</a></td><td>' + response[i].owner + "</td><td>" + response[i].tags + "</td><td>" + response[i].genre + "</td></tr>");
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