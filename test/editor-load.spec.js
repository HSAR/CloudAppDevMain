jQuery = require('jquery');
$ = jQuery;

jqueryJasmine = require('/home/travis/.nvm/v0.10.32/lib/node_modules/jasmine-jquery');

require('../src/public/js/editorHandler.js');

jasmine.getFixtures().fixturesPath = 'my/new/path';