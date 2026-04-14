package pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import utils.ElementUtil;
import utils.AppConstants;

public class OpenCartLoginPage {

    private WebDriver driver;
    private ElementUtil eleUtil;

    // 1. By locator - OR
    private By emailInput = By.xpath("//input[@id='input-email']");
    private By passwordInput = By.xpath("//input[@id='input-password']");
    private By loginButton = By.xpath("//input[@value='Login']");
    private By errorMessage = By.xpath("//div[contains(@class, 'alert-danger')]");

    // 2. Page constructor
    public OpenCartLoginPage(WebDriver driver) {
        this.driver = driver;
        this.eleUtil = new ElementUtil(driver);
    }

    // 3. Page actions
    public String getLoginPageTitle() {
        return eleUtil.waitForTitleToBe(AppConstants.SMALL_DEFAULT_TIMEOUT, AppConstants.LOGIN_PAGE_TITLE);
    }

    public void enterEmail(String email) {
        eleUtil.doSendKeys(emailInput, email);
    }

    public void enterPassword(String password) {
        eleUtil.doSendKeys(passwordInput, password);
    }

    public void clickLoginButton() {
        eleUtil.doClick(loginButton);
    }

    public String getErrorMessage() {
        return eleUtil.doGetText(errorMessage);
    }

    public OpenCartMyAccountPage doLogin(String email, String password) {
        eleUtil.doSendKeys(emailInput, email);
        eleUtil.doSendKeys(passwordInput, password);
        eleUtil.doClick(loginButton);
        return new OpenCartMyAccountPage(driver);
    }
}
