var webdriver = require('selenium-webdriver');

var driver = new webdriver.Builder().
    withCapabilities(webdriver.Capabilities.firefox()).
    build();

var createData = function() {
  driver.get('http://localhost:8080/admin/createinitialdata').then(function () {
    emailElement = driver.findElement(webdriver.By.name("action"));
    checkElement = driver.findElement(webdriver.By.name("admin"));
    checkElement.click().then(function () {
      emailElement.click().then(function () {
        return driver;
      });
    });
  });
};
