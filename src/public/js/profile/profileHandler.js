var init = function() {
    var path = window.location.pathname;
    path = path.split("/")[3];
	var ajax = new AjaxHandler();

    ajax.getUser(path, userData, unknownUser);
	ajax.getUserSongs(path, ownedSongs);
	ajax.getUserCollabs(path, collabSongs);

    //if user is viewing own profile, allow editing
    if (currentUserEntity.user_id === path) {
        $('.profile-edit').removeClass('no-display');
        $('textarea').attr('readonly',false);
        $('#profile-update-submit').show();
        $('#profile-update-submit').click(function() {
            var newData = {};
            if ($("#username-form").val() !== oldData.username && $("#username-form").val() != null) {
                newData.username = $("#username-form").val();
            }
            if ($("#bio-form").val() !== oldData.bio) {
                newData.bio = $("#bio-form").val();
            }
            if ($("#tags-form").val() !== oldData.tags) {
                newData.tags = $("#tags-form").val();
            }

            if (newData) {
                ajax.updateProfile(path, newData, profileUpdated);
            }        
        });
    } else {
        $('#profile-update-submit').hide();
        $('.profile-read').removeClass('no-display');
    }
}

var oldData = {
    username: null,
    bio: null,
    tags: null
}

var userData = function(response) {
    $(".profile-username").text(response.username);
    $("#username-form").val(response.username);
    $("#bio-form").val(response.bio);
    $("#tags-form").val(response.tags);
    oldData.username = $("#username-form").val();
    oldData.bio = $("#bio-form").val()
    oldData.tags = $("#tags-form").val();

    $('#bio-read-content').html(response.bio);
    var tmp = new String(response.tags);
    tags = tmp.split(',');
    for(var i = 0; i < tags.length; i++) {
        $('div#tags-area').append('<span class="label label-primary">' + tags[i] + '</span>');
    }
}

var unknownUser = function() {
    $('#unknown-profile-modal').modal('show');
    $('#unknown-profile-button').click(function() {
        location.href=window.location.protocol + '//' + window.location.host + '/dashboard';
    })
}
var profileUpdated = function(response) {
    console.log(response);
}

var ownedSongs = function(response) {
    writeToTable(songTables.owned, response);
}

var collabSongs = function(response) {
    writeToTable(songTables.collab, response);
}

var writeToTable = function(table, response) {
    if (!response || response[0] == null) {
        $(table).append('<tr><td>'+ songTableEmptyMessage[table] +'</td><td></td><td></td><td></td></tr>');
    } else {
        for (var i = 0; i < response.length; i++) {
            var staticPlayer = new StaticPlayer();
            staticPlayer.loadFile(window.location.protocol + '//' + window.location.host + '/api/songs/' + response[i].jingle_id + '/midi');
            $(table).append('<tr><td>' +  response[i].title + '</td>' 
                + '<td><a href="/web/users/' + response[i].author + '">' + response[i].username + '</a></td>' 
                + '<td>' + response[i].tags + '</td>'
                + '<td>' + response[i].genre + '</td>'
                + "<td class='preview" + response[i].jingle_id + "'></td></tr>");
            staticPlayer.attach($('td.preview' + response[i].jingle_id).eq(0));
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
