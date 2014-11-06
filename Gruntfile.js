module.exports = function(grunt) {
    // Project configuration.
    grunt.initConfig({
        qunit: {
            files: ['test/qunitExample.html']
        }
    });

    // Task to run tests
    grunt.registerTask('test', 'qunit');
};