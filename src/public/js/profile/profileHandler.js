var init = function() {
    var path = window.location.pathname;
    path = path.split("/")[3];
	var ajax = new AjaxHandler();

    ajax.getUser(path, userData);
	ajax.getUserSongs(path, ownedSongs);
	ajax.getUserCollabs(path, collabSongs);

    //if user is viewing own profile, allow editing
    if (currentUserEntity.user_id === path || true) {
        $('textarea').attr('readonly',false);
        $('#profile-update-submit').show();
    } else {
        $('#profile-update-submit').hide();
    }

    $('#profile-update-submit').click(function(e) {
        ajax.updateProfile(path, $("#username-form").val(), $("#bio-form").val(), $("#tags-form").val(), profileUpdated());
    });
}

var userData = function(response) {
    if (!response) {
        response = {username: "testuserplsignore", user_id: "testuidplsignore", bio: "this shouldn't be here", tags: "pumping, lemma" }; //test case
    }
    
    $(".profile-username").text(response.username);
    $("#username-form").val(response.username);
    $("#bio").val(response.bio);
    $("#tags").val(response.tags);
}

var profileUpdated = function(response) {
    if (response.key) {
        //successful
    }
}

var ownedSongs = function(response) {
    writeToTable(songTables.owned, response);
}

var collabSongs = function(response) {
    writeToTable(songTables.collab, response);
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
    '#ownedTable': 'User has not created any songs',
    '#collabTable': 'User has not contributed to any songs',
}