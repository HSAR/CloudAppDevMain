var ajax;
var pageData = { owned : []};

var init = function() {
	ajax = new AjaxHandler();
	ajax.getUserSongs(ownedSongs, ajaxFailure);
	ajax.getUserCollabs(collabSongs, ajaxFailure);
    ajax.getUserInvites(invitedSongs, ajaxFailure);
    ajax.getLatestSongs(latestSongs, ajaxFailure);
    
    $("#createJingleButton").click(function() {
        ajax.createJingle($("#title-form").val(), $("#genre-form").val(), $("#tags-form").val(), songCreated, ajaxFailure);
        $('#createJingleModal').modal('hide');
    });

    $("#editJingleButton").click(function() {
        if ($("#edit-title-form").val() !== "") {
            ajax.updateJingle(pageData.currentlyEdited,$("#edit-title-form").val(), $("#edit-genre-form").val(), $("#edit-tags-form").val(), songCreated, ajaxFailure);
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
}

var ownedSongs = function(response) {
    writeToTable('#ownedTable', response);
}

var collabSongs = function(response) {
    writeToTable('#collabTable', response);
}

var invitedSongs = function(response) {
    if (!response || response[0] == null) {
        $('#inviteTable').append('<tr><td>'+ 'No pending invitations' +'</td><td></td><td></td><td></td><td></td></tr>');
    } else {
        for (var i = 0; i < response.length; i++) {
            var resultDate = new Date(response[i].date_created * 1000);
            var resultGenre = response[i].genre;
            if (resultGenre === null) {
          		resultGenre = new String("");
         	}
            $('#inviteTable').append(
                '<tr><td>' + response[i].title +'</td>'
                + '<td><a href="/web/users/' + response[i].author + '">' + response[i].username + '</a></td>'
                + '<td>' + response[i].tags + '</td>'
                + '<td>' + resultGenre + '</td>'
                + '<td>' + resultDate.toLocaleDateString() + '<td>'
                + '<td><button class="accept-button btn btn-success" type="button" value="'+ response[i].jingle_id +'">Accept</button>'
                + '<button class="reject-button btn btn-danger" type="button" value="'+ response[i].jingle_id +'">Reject</button></td></tr>'
            );
        }

        $(".accept-button").click(function() {
            ajax.respondToInvite($(this).val(), true, acceptedInvite);
        });

        $(".reject-button").click(function() {
            ajax.respondToInvite($(this).val(), false, rejectedInvite);
        });
    }
}

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
}

var songCreated = function() {

    $('#createJingleModal').modal('hide');
    $('#editJingleModal').modal('hide');

    $('#ownedTable > tbody').html("");
    ajax.getUserSongs(ownedSongs, ajaxFailure);
}

var acceptedInvite = function() {
    $('#collabTable > tbody').html("");
    $('#inviteTable > tbody').html("");
    ajax.getUserCollabs(collabSongs, ajaxFailure);
    ajax.getUserInvites(invitedSongs, ajaxFailure);
}

var rejectedInvite = function() {
    $('#inviteTable > tbody').html("");
    ajax.getUserInvites(invitedSongs, ajaxFailure);
}

var writeToTable = function(table, response) {
    var songTableEmptyMessage = {
        '#ownedTable': 'No songs found. Why not <a href="#" data-toggle="modal" data-target="#createJingleModal">create one?</a>',
        '#collabTable': 'No collaborations found. Start contributing!',
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
            var editHTML = '';
            if(table === '#ownedTable') {
                editHTML = '<td><button class="btn btn-primary new-edit-button" id="edit-jingle-' + i + '" data-toggle="modal" data-target="#editJingleModal">Edit</button></td>';
                pageData.owned.push(response[i]);
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
                $('#edit-title-form').val(res.title);
                $('#edit-genre-form').val(resultGenre);
                $('#edit-tags-form').val(res.tags);
                pageData.currentlyEdited = res.jingle_id;
            });
            $('.new-edit-button').removeClass('new-edit-button');
        }
    }
}


