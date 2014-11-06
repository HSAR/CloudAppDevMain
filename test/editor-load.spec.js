jQuery = require('jquery');
$ = jQuery;
var jsdom = require('jsdom').jsdom;

var jqueryJasmine = require('jasmine-jquery');


document = jsdom('<!doctype html><html><head></head><body></body></html>');
window = document.createWindow();





require('../src/public/js/editorHandler.js');

jasmine.getFixtures().fixturesPath = 'my/new/path';