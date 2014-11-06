module.exports = function(grunt) {
    // Project configuration.
    grunt.initConfig({
    	pkg: grunt.file.readJSON('package.json'),
        qunit: {
            all : ['test/qunit/*.hmtl']
        }
    });
    grunt.loadNpmTasks('grunt-contrib-qunit');
    // Task to run tests
    grunt.registerTask('default', ['qunit']);
};