package utils;

import org.jspecify.annotations.NonNull;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;
import java.util.Objects;

public class ElementUtil {
    private @NonNull WebDriver driver;
    private @NonNull WebDriverWait wait;

    public ElementUtil(@NonNull WebDriver driver) {
        this.driver = Objects.requireNonNull(driver, "WebDriver must not be null");
        this.wait = new WebDriverWait(driver, Objects.requireNonNull(Duration.ofSeconds(AppConstants.MEDIUM_DEFAULT_TIMEOUT)));
    }

    public @NonNull WebElement getElement(@NonNull By locator) {
        return Objects.requireNonNull(driver.findElement(locator));
    }

    public void doSendKeys(@NonNull By locator, @NonNull String value) {
        wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).clear();
        getElement(locator).sendKeys(value);
    }

    public void doClick(@NonNull By locator) {
        wait.until(ExpectedConditions.elementToBeClickable(locator)).click();
    }

    public @NonNull String doGetText(@NonNull By locator) {
        return Objects.requireNonNull(
                wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).getText());
    }

    public boolean isElementDisplayed(@NonNull By locator) {
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(locator)).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    public @NonNull String waitForTitleToBe(int timeOut, @NonNull String title) {
        WebDriverWait localWait = new WebDriverWait(driver, Objects.requireNonNull(Duration.ofSeconds(timeOut)));
        localWait.until(ExpectedConditions.titleIs(title));
        return Objects.requireNonNull(driver.getTitle());
    }
}
