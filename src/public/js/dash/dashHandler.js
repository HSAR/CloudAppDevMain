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
            var staticPlayer = new StaticPlayer();
            staticPlayer.loadFile(window.location.protocol + '//' + window.location.host + '/api/songs/' + response[i].jingle_id + '/midi');
            $(table).append('<tr><td> <a href="/web/songs/' + response[i].jingle_id + '">' + response[i].title + '</a></td><td><a href="/web/users/' + response[i].author + '">' + response[i].username + '</a></td><td>'+ response[i].tags + "</td><td>" + response[i].genre + "</td><td class='preview" + response[i].jingle_id + "'></td></tr>");
            staticPlayer.attach($('td.preview' + response[i].jingle_id));
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
