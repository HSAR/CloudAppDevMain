jQuery = require('jquery');
$ = jQuery;
var jsdom = require('jsdom').jsdom;

var jqueryJasmine = require('./jasmine-jquery.js');

jasmine.getFixtures().fixturesPath = '../src/templates';
// document = jsdom('<!doctype html><html><head></head><body></body></html>');
// window = document.createWindow();
loadFixtures('editor.html');




require('../src/public/js/editorHandler.js');

