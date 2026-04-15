package tests;

import org.openqa.selenium.WebDriver;
import org.testng.Assert;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Optional;
import org.testng.annotations.Parameters;
import org.testng.annotations.Test;

import factory.DriverFactory;
import pages.OpenCartLoginPage;
import pages.OpenCartMyAccountPage;
import utils.ConfigReader;

import java.util.Objects;

public class ValidLoginTest {

    private OpenCartLoginPage loginPage;

    @Parameters({ "browser" })
    @BeforeMethod
    public void setUp(@Optional("chrome") String browser) {
        WebDriver driver = DriverFactory.getDriver(browser);
        driver.get(Objects.requireNonNull(ConfigReader.getProperty("url")));
        loginPage = new OpenCartLoginPage(driver);
    }

    @Test(dataProvider = "validLoginData", dataProviderClass = utils.TestDataUtils.class)
    public void testValidCredentials(String username, String password) {
        OpenCartMyAccountPage myAccountPage = loginPage.doLogin(username, password);

        Assert.assertTrue(myAccountPage.isMyOrdersHeadingDisplayed(),
                "'My Orders' heading is not displayed.");
        Assert.assertTrue(myAccountPage.isViewOrderHistoryLinkDisplayed(),
                "'View your order history' link is not displayed.");
    }

    @AfterMethod
    public void tearDown() {
        DriverFactory.quitDriver();
    }
}
