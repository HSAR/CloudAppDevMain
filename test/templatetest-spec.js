var webdriver = require('selenium-webdriver');

var driver = new webdriver.Builder().
    withCapabilities(webdriver.Capabilities.firefox()).
    build();

// This is a test suite, which groups together a bunch of tests.
describe('basic test', function () {

    // This is a test, a single self-contained unit that succeeds or fails. Ignored tests are xit('should be...')
    it('should be on correct page', function (done) {

        // Fetch page and execute callback when promise complete
        driver.get('http://localhost:8080/template').then(function () {

            // Find an element on the page and retrieve text within tag - callback, again
            driver.findElement(webdriver.By.tagName("p")).getText().then(function (value) {

                // Jasmine expect statement. Various other expectations are available.
                expect(value).toBe("Hello Generic User");

                // Close window - this doesn't matter on the VM, but is mostly for when you run manually
                driver.quit();

                // Complete test
                done();
            });
        });
    });
});
