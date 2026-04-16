package pages;

import org.jspecify.annotations.NonNull;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import utils.ElementUtil;
import java.util.Objects;

/**
 * Page object class representing the OpenCart My Account Page.
 * Provides methods to interact with elements on the My Account dashboard.
 */
public class OpenCartMyAccountPage {

    private @NonNull ElementUtil eleUtil;

    // 1. By locator - OR
    private @NonNull By myOrdersHeading = By.xpath("//h2[text()='My Orders']");
    private @NonNull By viewOrderHistoryLink = By.xpath("//a[text()='View your order history']");

    /**
     * Constructor for OpenCartMyAccountPage.
     * 
     * @param driver the WebDriver instance
     */
    public OpenCartMyAccountPage(@NonNull WebDriver driver) {
        Objects.requireNonNull(driver, "WebDriver must not be null");
        this.eleUtil = new ElementUtil(driver);
    }

    /**
     * Checks if the 'My Orders' heading is displayed on the page.
     * 
     * @return true if the heading is visible, false otherwise
     */
    public boolean isMyOrdersHeadingDisplayed() {
        return eleUtil.isElementDisplayed(myOrdersHeading);
    }

    /**
     * Checks if the 'View your order history' link is displayed.
     * 
     * @return true if the link is visible, false otherwise
     */
    public boolean isViewOrderHistoryLinkDisplayed() {
        return eleUtil.isElementDisplayed(viewOrderHistoryLink);
    }
}
