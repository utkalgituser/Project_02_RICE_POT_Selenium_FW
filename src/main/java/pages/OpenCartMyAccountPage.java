package pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;
import io.qameta.allure.Step;

public class OpenCartMyAccountPage {

    private WebDriverWait wait;

    @FindBy(xpath = "//h2[text()='My Orders']")
    private WebElement myOrdersHeading;

    @FindBy(xpath = "//a[text()='View your order history']")
    private WebElement viewOrderHistoryLink;

    public OpenCartMyAccountPage(WebDriver driver) {
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(15));
        PageFactory.initElements(driver, this);
    }

    @Step("Verify if My Orders heading is displayed")
    public boolean isMyOrdersHeadingDisplayed() {
        try {
            return wait.until(ExpectedConditions.visibilityOf(myOrdersHeading)).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    @Step("Verify if View Order History link is displayed")
    public boolean isViewOrderHistoryLinkDisplayed() {
        try {
            return wait.until(ExpectedConditions.visibilityOf(viewOrderHistoryLink)).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }
}
