package pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;
import io.qameta.allure.Step;

public class OpenCartLoginPage {

    private WebDriver driver;
    private WebDriverWait wait;

    @FindBy(xpath = "//input[@id='input-email']")
    private WebElement emailInput;

    @FindBy(xpath = "//input[@id='input-password']")
    private WebElement passwordInput;

    @FindBy(xpath = "//input[@value='Login']")
    private WebElement loginButton;

    @FindBy(xpath = "//div[contains(@class, 'alert-danger')]")
    private WebElement errorMessage;

    public OpenCartLoginPage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        PageFactory.initElements(driver, this);
    }

    @Step("Enter email address: {email}")
    public void enterEmail(String email) {
        try {
            wait.until(ExpectedConditions.visibilityOf(emailInput)).clear();
            emailInput.sendKeys(email);
        } catch (Exception e) {
            throw new RuntimeException("Exception occurred while entering email: " + e.getMessage(), e);
        }
    }

    @Step("Enter password")
    public void enterPassword(String password) {
        try {
            wait.until(ExpectedConditions.visibilityOf(passwordInput)).clear();
            passwordInput.sendKeys(password);
        } catch (Exception e) {
            throw new RuntimeException("Exception occurred while entering password: " + e.getMessage(), e);
        }
    }

    @Step("Click on the login button")
    public void clickLoginButton() {
        try {
            wait.until(ExpectedConditions.elementToBeClickable(loginButton)).click();
        } catch (Exception e) {
            throw new RuntimeException("Exception occurred while clicking login button: " + e.getMessage(), e);
        }
    }

    @Step("Get login error message")
    public String getErrorMessage() {
        try {
            return wait.until(ExpectedConditions.visibilityOf(errorMessage)).getText();
        } catch (Exception e) {
            throw new RuntimeException("Exception occurred while fetching error message: " + e.getMessage(), e);
        }
    }

    @Step("Login with username: {email}")
    public OpenCartMyAccountPage doLogin(String email, String password) {
        enterEmail(email);
        enterPassword(password);
        clickLoginButton();
        return new OpenCartMyAccountPage(driver);
    }
}
