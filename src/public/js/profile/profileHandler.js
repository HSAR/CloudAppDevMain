$( document ).ready(function() {
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
        console.log("click");
    });
});

var userData = function(response) {
    var data = jQuery.parseJSON(response);
    if (!data) {
        data = {username: "testuserplsignore", user_id: "testuidplsignore", bio: "this shouldn't be here", tags: "pumping, lemma" }; //test case
    }
    
    $(".profile-username").text(data.username);
    $("#username-form").val(data.username);
    $("#bio").val(data.bio);
    $("#tags").val(data.tags);
}

var profileUpdated = function(response) {
    var data = jQuery.parseJSON(response);
    if (data.key) {
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