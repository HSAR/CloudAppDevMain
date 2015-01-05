var ajax;
var pageData = { owned : {}, tags : []};

var init = function() {
	ajax = new AjaxHandler();
	ajax.getUserSongs(ownedSongs, ajaxFailure);
	ajax.getUserCollabs(collabSongs, ajaxFailure);
    ajax.getUserInvites(invitedSongs, ajaxFailure);
    ajax.getLatestSongs(latestSongs, ajaxFailure);

    $('#title-form').val('');//clear cached values on page load
    $('#genre-form').val('');
    $('#tags-form').val('');
    
    $("#createJingleButton").click(function() {
        createTag($("#tags-form").val(),$('.tags-area').eq(0),$('#tags-form'));
        ajax.createJingle($("#title-form").val(), $("#genre-form").val(), pageData.tags.join(), songCreated, ajaxFailure);
        $('#createJingleModal').modal('hide');
    });

    $("#editJingleButton").click(function() {
        createTag($("#edit-tags-form").val(),$('.tags-area').eq(1),$('#edit-tags-form'));
        ajax.updateJingle(pageData.currentlyEdited,$("#edit-title-form").val(), $("#edit-genre-form").val(), pageData.tags.join(), songCreated, ajaxFailure);
        $('#editJingleModal').modal('hide');
    });

    $('#create-jingle').click(function() {
        $('.tags-area').empty();
        pageData.tags = [];//reset tags
    });

    $('.tags-form').keyup(function() {
        if($(this).val().indexOf(',') !== -1) {//if tag ended
            var $target;
            var $input;
            if($(this).attr('id') === 'tags-form') {
                $target = $('.tags-area').eq(0);
                $input = $('#tags-form');
            } else {
                $target = $('.tags-area').eq(1);
                $input = $('#edit-tags-form'); 
            }
            var parts = $(this).val().split(',');
            createTag(parts[0],$target,$input); 
            
            
        }
    });

    if(currentUserEntity) {
        var tags = currentUserEntity.tags;
        for(var i = 0; i < tags.length; i++) {
            var htmlToAppend = '<li><i class="glyphicon glyphicon-flash"></i><a href="'
            + window.location.protocol + '//' + window.location.host + '/search?tag=' + tags[i].trim()
            + '">' + tags[i].trim() +  '</a></li>';
            $('ul.tag-list').append(htmlToAppend);
        }
    }
};

var ownedSongs = function(response) {
    writeToTable('#ownedTable', response);
};

var collabSongs = function(response) {
    writeToTable('#collabTable', response);
};

var invitedSongs = function(response) {
    if (!response || response[0] === null) {
        $('#inviteTable').append('<tr><td>'+ 'No pending invitations' +'</td></tr>');
    } else {
        for (var i = 0; i < response.length; i++) {
            var resultDate = new Date(response[i].date_created * 1000);
            var resultGenre = response[i].genre;
            if (resultGenre === null) {
          		resultGenre = new String();
         	}
            $('#inviteTable').append(
                '<tr><td>' + response[i].title +'</td>'
                + '<td><a href="/web/users/' + response[i].author + '">' + response[i].username + '</a></td>'
                + '<td>' + response[i].tags + '</td>'
                + '<td>' + resultGenre + '</td>'
                + '<td>' + resultDate.toLocaleDateString() + '</td>'
                + '<td><button class="accept-button invite-response-button btn btn-sm btn-success" type="button" value="'+ response[i].jingle_id +'">Accept</button>'
                + '<button class="reject-button invite-response-button btn btn-sm btn-danger" type="button" value="'+ response[i].jingle_id +'">Reject</button></td></tr>'
            );
        }

        $(".accept-button").click(function() {
            ajax.respondToInvite($(this).val(), true, acceptedInvite);
        });

        $(".reject-button").click(function() {
            ajax.respondToInvite($(this).val(), false, rejectedInvite);
        });
    }
};

var latestSongs = function(response) {
    var result = response.results;
    for (var i = 0; i < result.length && i<5; i++) {
            var staticPlayer = new StaticPlayer();
            staticPlayer.loadFile(window.location.protocol + '//' + window.location.host + '/api/songs/' + result[i].jingle_id + '/midi');
            $('#latest-table tbody').append(
            	'<tr><td>' + result[i].title + '</td>'
                + "<td class='preview" + result[i].jingle_id + "'></td></tr>");
            staticPlayer.attach($('#latest-table td.preview' + result[i].jingle_id).eq(0));
    }
};

var songCreated = function() {
    $('#title-form').val('');
    $('#genre-form').val('');
    $('#tags-form').val('');

    $('#ownedTable > tbody').html("");
    ajax.getUserSongs(ownedSongs, ajaxFailure);
    $('.alert').alert("close");
    $('#page-content').prepend(
        '<div id="ajax-alert" role="alert" class="alert alert-success alert-dismissible fade in">'
        + '<button aria-label="Close" data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span></button>'
        + "<p>Jingle saved</p>"
        + '</div>'
    );
};

var acceptedInvite = function() {
    $('#collabTable > tbody').html("");
    $('#inviteTable > tbody').html("");
    ajax.getUserCollabs(collabSongs, ajaxFailure);
    ajax.getUserInvites(invitedSongs, ajaxFailure);
    $('.alert').alert("close");

    $('#page-content').prepend(
        '<div id="ajax-alert" role="alert" class="alert alert-success alert-dismissible fade in">'
        + '<button aria-label="Close" data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span></button>'
        + "<p>Invite accepted</p>"
        + '</div>'
    );
    alertUser('alert-success', 'Invite accepted');
};



var rejectedInvite = function() {
    $('#inviteTable > tbody').html("");
    ajax.getUserInvites(invitedSongs, ajaxFailure);
    $('.alert').alert("close");

    $('#page-content').prepend(
        '<div id="ajax-alert" role="alert" class="alert alert-success alert-dismissible fade in">'
        + '<button aria-label="Close" data-dismiss="alert" class="close" type="button"><span aria-hidden="true">×</span></button>'
        + "<p>Invite declined</p>"
        + '</div>'
    );
    alertUser('alert-success', 'Invite rejected');
};



var createTag = function(name,$target,$inputArea) {
    if(!name || name === '') {//validate name
        return;
    }
    $inputArea.val('');//reset form
    if(pageData.tags.indexOf(name) === -1) {
        pageData.tags.push(name);//store that tag
        $target.append('<button class="btn tag-button new-tag">' + name + 
                '<span class="glyphicon glyphicon-remove"></span></button>');
        $('.new-tag').click(function() {
            var index = pageData.tags.indexOf(name);
            pageData.tags.splice(index, 1);
            $(this).remove();
        }).removeClass('new-tag');
    }
};

var writeToTable = function(table, response) {
    var songTableEmptyMessage = {
        '#ownedTable': 'No songs found. Why not <a href="#" data-toggle="modal" data-target="#createJingleModal">create one?</a>',
        '#collabTable': 'No collaborations found. Start contributing!',
    };
    if (response[0] === undefined) {
        $(table).append('<tr><td>'+ songTableEmptyMessage[table] +'</td></tr>');
    } else {
        for (var i = 0; i < response.length; i++) {
            var resultDate = new Date(response[i].date_created * 1000);
            var resultGenre = response[i].genre;
         	if (resultGenre === null) {
          		resultGenre = new String();
         	}
            var staticPlayer = new StaticPlayer();
            var editHTML = '';
            if(table === '#ownedTable') {
                editHTML = '<td><button class="btn btn-primary new-edit-button" id="edit-jingle-' 
                + response[i].jingle_id + '" data-toggle="modal" data-target="#editJingleModal">Edit</button></td>';
                pageData.owned[response[i].jingle_id] = response[i];
            }
            staticPlayer.loadFile(window.location.protocol + '//' + window.location.host + '/api/songs/' + response[i].jingle_id + '/midi');
            $(table).append('<tr><td> <a href="/web/songs/' + response[i].jingle_id + '">' + response[i].title + '</a></td>' 
                + '<td><a href="/web/users/' + response[i].author + '">' + response[i].username + '</a></td>' 
                + '<td>' + response[i].tags + '</td>'
                + '<td>' + resultGenre + '</td>'
                + '<td>' + resultDate.toLocaleDateString() + '</td>'
                + "<td class='preview" + response[i].jingle_id + "'></td>"
                + editHTML + '</tr>');
            staticPlayer.attach($(table + ' td.preview' + response[i].jingle_id).eq(0));
           
            $('.new-edit-button').click(function() {
                var id = $(this).attr('id').substring(12);
                var res = pageData.owned[id];

                pageData.tags = [];
                $('.tags-area').empty();

                for(var i = 0; i < res.tags.length; i++) {
                    createTag(res.tags[i],$('.tags-area').eq(1),$('#edit-tags-form'));
                }
                
                $('#edit-title-form').val(res.title);
                $('#edit-genre-form').val(res.genre);
                $('#edit-tags-form').val('');
                pageData.currentlyEdited = res.jingle_id;
            });
            $('.new-edit-button').removeClass('new-edit-button');
        }
    }
};


