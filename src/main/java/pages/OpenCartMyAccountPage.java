package pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import utils.ElementUtil;

public class OpenCartMyAccountPage {

    private ElementUtil eleUtil;

    // 1. By locator - OR
    private By myOrdersHeading = By.xpath("//h2[text()='My Orders']");
    private By viewOrderHistoryLink = By.xpath("//a[text()='View your order history']");

    // 2. Page constructor
    public OpenCartMyAccountPage(WebDriver driver) {
        this.eleUtil = new ElementUtil(driver);
    }

    // 3. Page actions
    public boolean isMyOrdersHeadingDisplayed() {
        return eleUtil.isElementDisplayed(myOrdersHeading);
    }

    public boolean isViewOrderHistoryLinkDisplayed() {
        return eleUtil.isElementDisplayed(viewOrderHistoryLink);
    }
}
