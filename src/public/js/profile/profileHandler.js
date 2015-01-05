var oldData = {
    username: null,
    bio: null,
    tags: null
};

var pageData = {
    tags : []
};
var path;

var init = function() {
    path = window.location.pathname;
    path = path.split("/")[3];
	ajax = new AjaxHandler();

    ajax.getUser(path, userData, ajaxFailure);
	ajax.getUserSongs(path, ownedSongs, ajaxFailure);
	ajax.getUserCollabs(path, collabSongs, ajaxFailure);

    //if user is viewing own profile, allow editing
    if (currentUserEntity.user_id === path) {
        $('button.edit-button').removeClass('no-display').click(function() {
            $('.profile-edit').removeClass('no-display');//display the profle editor
        });

        $('textarea').attr('readonly',false);
        $('#profile-update-submit').show();
    }

    $('#tags-form').keyup(function() {
        if($(this).val().slice(-1) === ',') {//if tag ended
            createTag($(this).val().slice(0,-1));
        }
    });
}

var createTag = function(name) {
    if(!name || name === '') {//validate name
        return;
    }
    $('#tags-form').val('');//reset form
    if(pageData.tags.indexOf(name) === -1) {
        pageData.tags.push(name);//store that tag
        $('.tags-area').append('<button class="btn tag-button new-tag">' + name + 
                '<i class="glyphicon glyphicon-remove"></i></button>');
        $('.new-tag').click(function() {
            console.log("reached click event");
            var index = pageData.tags.indexOf(name);
            console.log(index);
            pageData.tags.splice(index, 1);
            $(this).remove();
        }).removeClass('new-tag');
    }
}

var isFormUpdated = function() {
    var newData = {};

    if ($("#username-form").val() === "") {
        $('#page-content').prepend(
            '<div id="ajax-alert" role="alert" class="alert alert-danger alert-dismissible fade in">'
            + '<button aria-label="Close" data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span></button>'
            + "<p>Your username cannot be empty</p>"
            + '</div>'
        );
        $('.profile-edit').addClass("no-display");
        return;
    }
    if ($("#username-form").val() !== oldData.username && $("#username-form").val() !== "") {

    createTag($('#tags-form').val());//add any remaining stuff in form
    if ($("#username-form").val() !== oldData.username && $("#username-form").val() != null) {

        newData.username = $("#username-form").val();
    }
    if ($("#bio-form").val() !== oldData.bio) {
        newData.bio = $("#bio-form").val();
    }
    if (pageData.tags !== oldData.tags) {
        newData.tags = pageData.tags.join();
    }
    if (!jQuery.isEmptyObject(newData)) {
        ajax.updateProfile(path, newData, profileUpdated, ajaxFailure);
    } else {
        $('#page-content').prepend(
            '<div id="ajax-alert" role="alert" class="alert alert-danger alert-dismissible fade in">'
            + '<button aria-label="Close" data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span></button>'
            + "<p>You didn't make any changes!</p>"
            + '</div>'
        );
        $('.profile-edit').addClass("no-display");//hide profile editor
    }
}

var profileUpdated = function() {
    ajax.getUser(path, userData, ajaxFailure); //update profile page
    getCurrentUser(setUser, ajaxFailure); //update currentUserEntity and related fields
    $('.profile-edit').addClass("no-display");//hide profile editor
    $('.alert').alert("close");
    $('#page-content').prepend(
        '<div id="ajax-alert" role="alert" class="alert alert-success alert-dismissible fade in">'
        + '<button aria-label="Close" data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span></button>'
        + "<p>Profile updated</p>"
        + '</div>'
    );
}

var userData = function(response) {
    $(".profile-username").text(response.username);
    $("#username-form").val(response.username);
    $("#bio-form").val(response.bio);
    var tagsList = response.tags;
    for(var i = 0; i < tagsList.length; i++) {
        createTag(tagsList[i]);
    }
    oldData.username = $("#username-form").val();
    oldData.bio = $("#bio-form").val()
    oldData.tags = response.tags;

    if(!response.bio || response.bio === '') {//if undefined or empty
         $('#bio-read-content').html('This Jinglr member has no biography');
    } else {
        $('#bio-read-content').html(response.bio);
    }
    
    $('#tags-area').html("");
    if(!response.tags || response.tags === '') {//if undefined or empty
         $('#tags-area').append('<p>This Jinglr member has no favourite tags</p>');
    } else {
        var tmp = new String(response.tags);
        tags = tmp.split(',');
        for(var i = 0; i < tags.length; i++) {
            $('#tags-area').append('<button class="label label-primary tag-label">' + tags[i] + '</button>');
        }
    }
}

var ownedSongs = function(response) {
    writeToTable('#ownedTable', response);
}

var collabSongs = function(response) {
    writeToTable('#collabTable', response);
}

var writeToTable = function(table, response) {
    var songTableEmptyMessage = {
        '#ownedTable': 'User has not created any songs',
        '#collabTable': 'User has not contributed to any songs',
    }

    if (!response || response[0] == null) {
        $(table).append('<tr><td>'+ songTableEmptyMessage[table] +'</td><td></td><td></td><td></td></tr>');
    } else {
        for (var i = 0; i < response.length; i++) {
            var resultDate = new Date(response[i].date_created * 1000);
            var resultGenre = response[i].genre;
          	if (resultGenre === null) {
          		resultGenre = new String("");
         	 }
            var staticPlayer = new StaticPlayer();
            staticPlayer.loadFile(window.location.protocol + '//' + window.location.host + '/api/songs/' + response[i].jingle_id + '/midi');
            $(table).append('<tr><td>' +  response[i].title + '</td>' 
                + '<td><a href="/web/users/' + response[i].author + '">' + response[i].username + '</a></td>' 
                + '<td>' + response[i].tags + '</td>'
                + '<td>' + resultGenre + '</td>'
                + '<td>' + resultDate.toLocaleDateString() + '</td>'
                + "<td class='preview" + response[i].jingle_id + "'></td></tr>"
            );
            staticPlayer.attach($(table + ' td.preview' + response[i].jingle_id).eq(0));
        }
    }
}


