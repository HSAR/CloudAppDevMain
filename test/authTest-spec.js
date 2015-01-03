var createData = require('./createData.js');
var webdriver = require('selenium-webdriver');

var driver = new webdriver.Builder().
    withCapabilities(webdriver.Capabilities.firefox()).
    build();

driver.manage().timeouts().pageLoadTimeout(50000);

describe('Authentication Tests', function () {

    it('should serve the login page when accessing the editor and without being logged in', function (done) {
        createData.createData(function () {
            driver.get('http://localhost:8080/web/songs/0').then(function () {
    
                driver.findElement(webdriver.By.tagName("h3")).getText().then(function (loginH3) {
    
                    // expect to not be on the editor page
                    driver.getCurrentUrl().then(function (currURL) {
                        expect(currURL).toNotBe('http://localhost:8080/web/songs/0');
                    });
    
                    // expect to be on the login page
                    expect(loginH3).toBe("Not logged in");
    
                    emailElement = driver.findElement(webdriver.By.name("action"));
                    emailElement.click().then(function () {
                        // expect to have been redirected back onto the editor page
                        driver.getCurrentUrl().then(function (currURL) {
                            expect(currURL).toBe('http://localhost:8080/web/songs/0');
                            driver.quit();
                            done();
                        });
                    });
                });
            });
        });
    }, 50000 /*timeout*/);
});
