jQuery = require('jquery');
$ = jQuery;
window = require('jsdom').jsdom().createWindow();
document = window.document;

var jqueryJasmine = require('jasmine-jquery');


require('../src/public/js/editorHandler.js');

jasmine.getFixtures().fixturesPath = 'my/new/path';