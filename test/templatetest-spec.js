var webdriver = require('selenium-webdriver');
 
var driver = new webdriver.Builder().
   withCapabilities(webdriver.Capabilities.firefox()).
   build();
 
describe('basic test', function () {

 it('should be on correct page', function (done) {
 
    driver.get('http://localhost:8080/template').then(function() {
            driver.findElement(webdriver.By.tagName("p")).getText().then(function(value) {
                    expect(value).toBe("Hello Generic User");
                    driver.quit();
                    done();
                }
            )
        });
    });
});