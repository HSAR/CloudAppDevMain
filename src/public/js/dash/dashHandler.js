var init = function() {
	var ajax = new AjaxHandler();
	ajax.getUserSongs(ownedSongs, connectionFailure);
	ajax.getUserCollabs(collabSongs, connectionFailure);
    ajax.getUserInvites(invitedSongs, connectionFailure);
    
    $("#createJingleButton").click(function() {
        ajax.createJingle($("#title-form").val(), $("#genre-form").val(), $("#tags-form").val(), songCreated, connectionFailure);
    });
}

var songCreated = function() {
    location.reload();
}

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
    if (!response || response[0] == null) {
        $(table).append('<tr><td>'+ songTableEmptyMessage[table] +'</td><td></td><td></td><td></td></tr>');
    } else {
        for (var i = 0; i < response.length; i++) {
            $(table).append('<tr><td> <a href="http://jinglr-music.appspot.com/web/songs/' + results[i].jingle_id + '">' + response[i].title + '</a></td><td>' + response[i].author + "</td><td>" + response[i].tags + "</td><td>" + response[i].genre + "</td></tr>");
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