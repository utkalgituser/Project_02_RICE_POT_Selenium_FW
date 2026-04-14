package utils;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class ElementUtil {
    private WebDriver driver;
    private WebDriverWait wait;

    public ElementUtil(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(AppConstants.MEDIUM_DEFAULT_TIMEOUT));
    }

    public WebElement getElement(By locator) {
        return driver.findElement(locator);
    }

    public void doSendKeys(By locator, String value) {
        wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).clear();
        getElement(locator).sendKeys(value);
    }

    public void doClick(By locator) {
        wait.until(ExpectedConditions.elementToBeClickable(locator)).click();
    }

    public String doGetText(By locator) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).getText();
    }

    public boolean isElementDisplayed(By locator) {
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    public String waitForTitleToBe(int timeOut, String title) {
        WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(timeOut));
        wait.until(ExpectedConditions.titleIs(title));
        return driver.getTitle();
    }
}
