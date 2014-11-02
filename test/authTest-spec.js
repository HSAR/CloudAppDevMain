var webdriver = require('selenium-webdriver');

var driver = new webdriver.Builder().
    withCapabilities(webdriver.Capabilities.firefox()).
    build();

describe('Authentication Tests', function () {

    it('should serve the login page when accessing the editor and without being logged in', function (done) {

        driver.get('http://localhost:8080/editor/').then(function () {

            driver.findElement(webdriver.By.tagName("h3")).getText().then(function (loginH3) {

                // expect to not be on the editor page
                driver.getCurrentUrl().then(function (currURL) {
                    expect(currURL).toNotBe('http://localhost:8080/editor/');
                    console.log("FISH 1");
                });

                // expect to be on the login page
                expect(loginH3).toBe("Not logged in");
                    console.log("FISH 2");

                emailElement = driver.findElement(webdriver.By.name("action"));
                emailElement.click().then(function () {
                    driver.findElement(webdriver.By.css(".auth")).getText().then(function (authedUser) {
                        // expect to be correctly signed in
                        expect(authedUser).toContain("Signed in as test@example.com");
                    console.log("FISH 3");
                    });

                    // expect to have been redirected back onto the editor page
                    driver.getCurrentUrl().then(function (currURL) {
                        expect(currURL).toBe('http://localhost:8080/editor/');
                        console.log("FISH 4");
                        driver.quit();
                        done();
                    });
                });
            });
        });
    });
});
