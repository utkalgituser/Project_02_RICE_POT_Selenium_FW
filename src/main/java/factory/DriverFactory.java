package factory;

import org.jspecify.annotations.NonNull;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

import java.time.Duration;
import java.util.Objects;

import utils.AppConstants;

public class DriverFactory {

    private static ThreadLocal<WebDriver> driverProvider = new ThreadLocal<>();

    public static @NonNull WebDriver getDriver(String browser) {
        if (driverProvider.get() == null) {
            WebDriver driver;
            
            if (browser == null || browser.trim().isEmpty()) {
                browser = "chrome";
            }
            
            switch (browser.toLowerCase()) {
                case "firefox":
                    driver = new FirefoxDriver();
                    break;
                case "edge":
                    driver = new EdgeDriver();
                    break;
                case "chrome":
                default:
                    driver = new ChromeDriver();
                    break;
            }
            driver.manage().window().maximize();
            driver.manage().timeouts().pageLoadTimeout(Objects.requireNonNull(Duration.ofSeconds(AppConstants.PAGE_LOAD_TIMEOUT)));
            driverProvider.set(driver);
        }
        return Objects.requireNonNull(driverProvider.get(), "WebDriver was not initialised for this thread");
    }

    public static void quitDriver() {
        if (driverProvider.get() != null) {
            driverProvider.get().quit();
            driverProvider.remove();
        }
    }
}
