$( document ).ready(function() {
	//some auth stuff to get username
	var ajax = new AjaxHandler();
	ajax.setUserID('userID');
	ajax.getUserSongs(ownedSongs);
	ajax.getCollabSongs(collabSongs);
});

var ownedSongs = function(data) {
            for (var i = 0; i < data.length; i++) {
                $('<tr>').html(
                    $('td').text(data.i.title),
                    $('td').text(data.i.owner),
                    $('td').text(data.i.tags),
                    $('td').text(data.i.genre)
                ).appendTo('#ownedTable');

            });
}
var collabSongs = function(data) {
            for (var i = 0; i < data.length; i++) {
                $('<tr>').html(
                    $('td').text(data.i.title),
                    $('td').text(data.i.owner),
                    $('td').text(data.i.tags),
                    $('td').text(data.i.genre)
                ).appendTo('#collabTable');

            });
}