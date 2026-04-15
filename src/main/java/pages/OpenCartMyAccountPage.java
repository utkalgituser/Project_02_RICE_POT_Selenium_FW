package pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.Objects;

import utils.AppConstants;

// PageFactory initializes @FindBy fields at runtime via reflection;
// Eclipse's null analysis cannot verify this, so we suppress here.
@SuppressWarnings("null")
public class OpenCartMyAccountPage {

    private WebDriverWait wait;

    @FindBy(xpath = "//h2[text()='My Orders']")
    private WebElement myOrdersHeading;

    @FindBy(xpath = "//a[text()='View your order history']")
    private WebElement viewOrderHistoryLink;

    public OpenCartMyAccountPage(WebDriver driver) {
        Objects.requireNonNull(driver, "WebDriver must not be null");
        this.wait = new WebDriverWait(driver,
                Objects.requireNonNull(Duration.ofSeconds(AppConstants.EXPLICIT_WAIT_TIMEOUT)));
        PageFactory.initElements(driver, this);
    }

    public boolean isMyOrdersHeadingDisplayed() {
        try {
            return wait.until(ExpectedConditions.visibilityOf(myOrdersHeading)).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    public boolean isViewOrderHistoryLinkDisplayed() {
        try {
            return wait.until(ExpectedConditions.visibilityOf(viewOrderHistoryLink)).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }
}
