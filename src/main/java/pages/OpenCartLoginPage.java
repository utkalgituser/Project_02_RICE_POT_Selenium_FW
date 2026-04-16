package pages;

import org.jspecify.annotations.NonNull;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import utils.ElementUtil;
import utils.AppConstants;
import java.util.Base64;
import java.util.Objects;

/**
 * Page object class representing the OpenCart Login Page.
 * Encapsulates the UI elements and actions associated with the login functionality.
 */
public class OpenCartLoginPage {

    private @NonNull WebDriver driver;
    private @NonNull ElementUtil eleUtil;

    // 1. By locator - OR
    private @NonNull By emailInput = By.xpath("//input[@id='input-email']");
    private @NonNull By passwordInput = By.xpath("//input[@id='input-password']");
    private @NonNull By loginButton = By.xpath("//input[@value='Login']");
    private @NonNull By errorMessage = By.xpath("//div[contains(@class, 'alert-danger')]");

    /**
     * Constructor for OpenCartLoginPage.
     * 
     * @param driver the WebDriver instance
     */
    public OpenCartLoginPage(@NonNull WebDriver driver) {
        this.driver = Objects.requireNonNull(driver, "WebDriver must not be null");
        this.eleUtil = new ElementUtil(driver);
    }

    /**
     * Gets the title of the login page.
     * 
     * @return the login page title as a String
     */
    public @NonNull String getLoginPageTitle() {
        return eleUtil.waitForTitleToBe(AppConstants.SMALL_DEFAULT_TIMEOUT, AppConstants.LOGIN_PAGE_TITLE);
    }

    /**
     * Enters the email address into the email input field.
     * If the email is Base64 encoded, it will be automatically decoded.
     * 
     * @param email the email address or its Base64 encoded representation
     */
    public void enterEmail(@NonNull String email) {
        eleUtil.doSendKeys(emailInput, decodeData(email));
    }

    /**
     * Enters the password into the password input field.
     * If the password is Base64 encoded, it will be automatically decoded.
     * 
     * @param password the password or its Base64 encoded representation
     */
    public void enterPassword(@NonNull String password) {
        eleUtil.doSendKeys(passwordInput, decodeData(password));
    }

    /**
     * Clicks on the login button.
     */
    public void clickLoginButton() {
        eleUtil.doClick(loginButton);
    }

    /**
     * Gets the error message displayed after an unsuccessful login attempt.
     * 
     * @return the error message as a String
     */
    public @NonNull String getErrorMessage() {
        return eleUtil.doGetText(errorMessage);
    }

    /**
     * Performs a complete login action and navigates to the My Account page.
     * 
     * @param email    the email address (raw or Base64 encoded)
     * @param password the password (raw or Base64 encoded)
     * @return the OpenCartMyAccountPage object upon successful login transition
     */
    public OpenCartMyAccountPage doLogin(@NonNull String email, @NonNull String password) {
        System.out.println("Logging in with email: " + maskEmail(decodeData(email)));
        enterEmail(email);
        enterPassword(password);
        clickLoginButton();
        return new OpenCartMyAccountPage(driver);
    }
    
    /**
     * Masks a sensitive email address for logging and reporting purposes.
     * 
     * @param email the raw email address
     * @return the partially masked email address
     */
    private String maskEmail(String email) {
        if (email == null || !email.contains("@")) return "******";
        String[] parts = email.split("@");
        if (parts[0].length() <= 2) return "**@" + parts[1];
        return parts[0].substring(0, 2) + "*****@" + parts[1];
    }
    
    /**
     * Decodes Base64 encoded data to prevent raw sensitive strings from being exposed in test data.
     * 
     * @param encodedData the potentially Base64 encoded data
     * @return the decoded string, or the original string if it is not valid Base64
     */
    private @NonNull String decodeData(@NonNull String encodedData) {
        try {
            return new String(Base64.getDecoder().decode(encodedData));
        } catch (IllegalArgumentException e) {
            // Fallback in case raw data was provided while transitioning
            return encodedData;
        }
    }
}
