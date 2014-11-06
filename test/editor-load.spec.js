jQuery = require('jquery');
$ = jQuery;
var jsdom = require('jsdom').jsdom;
document = jsdom('<!doctype html><html><body></body></html>');
window = document.createWindow();


var jqueryJasmine = require('jasmine-jquery');


require('../src/public/js/editorHandler.js');

jasmine.getFixtures().fixturesPath = 'my/new/path';