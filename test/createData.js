var webdriver = require('selenium-webdriver');

var driver = new webdriver.Builder().
    withCapabilities(webdriver.Capabilities.firefox()).
    build();

var createData = function(thenFunc) {
  driver.get('http://localhost:8080/admin/initialdata').then(function () {
    emailElement = driver.findElement(webdriver.By.name("action"));
    checkElement = driver.findElement(webdriver.By.name("admin"));
    checkElement.click().then(function () {
      emailElement.click().then(function () {
        thenFunc();
      });
    });
  });
};

module.exports.createData = createData;
