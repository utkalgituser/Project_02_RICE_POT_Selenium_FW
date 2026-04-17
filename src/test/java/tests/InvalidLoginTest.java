package tests;

import org.jspecify.annotations.NonNull;
import org.openqa.selenium.WebDriver;
import org.testng.Assert;
import java.util.Objects;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Optional;
import org.testng.annotations.Parameters;
import org.testng.annotations.Test;

import factory.DriverFactory;
import pages.OpenCartLoginPage;
import utils.ConfigReader;
import io.qameta.allure.Description;
import io.qameta.allure.Epic;
import io.qameta.allure.Feature;
import io.qameta.allure.Severity;
import io.qameta.allure.SeverityLevel;
import io.qameta.allure.Story;
@Epic("OpenCart Automation")
@Feature("Login functionality")
public class InvalidLoginTest {

    private OpenCartLoginPage loginPage;

    @Parameters({ "browser" })
    @BeforeMethod
    public void setUp(@Optional("chrome") String browser) {
        WebDriver driver = DriverFactory.getDriver(browser);
        driver.get(Objects.requireNonNull(ConfigReader.getProperty("url")));
        loginPage = new OpenCartLoginPage(driver);
    }

    private static final @NonNull String EXPECTED_INVALID_MSG =
            "Warning: No match for E-Mail Address and/or Password.";
    private static final @NonNull String LOCKOUT_MSG =
            "Your account has exceeded allowed number of login attempts. Please try again in 1 hour.";

    @Test(dataProvider = "invalidLoginData", dataProviderClass = utils.TestDataUtils.class)
    @Story("Invalid Login Story")
    @Severity(SeverityLevel.NORMAL)
    @Description("Verify that appropriate error message is displayed when invalid credentials are provided")
    public void testInvalidCredentials(@NonNull String username, @NonNull String password) {
        loginPage.doLogin(username, password);

        @NonNull String actualErrorMsg = Objects.requireNonNull(loginPage.getErrorMessage(),
                "Error message element returned null for user: " + username);

        boolean isInvalidCredentials = actualErrorMsg.contains(EXPECTED_INVALID_MSG);
        boolean isAccountLocked     = actualErrorMsg.contains(LOCKOUT_MSG);

        Assert.assertTrue(
                isInvalidCredentials || isAccountLocked,
                "Unexpected error message on invalid login attempt."
                + "\n  Expected (invalid-credentials): [" + EXPECTED_INVALID_MSG + "]"
                + "\n  Expected (account-locked)     : [" + LOCKOUT_MSG + "]"
                + "\n  Actual UI message             : [" + actualErrorMsg + "]");
    }

    @AfterMethod
    public void tearDown() {
        DriverFactory.quitDriver();
    }
}
