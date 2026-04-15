package utils;

/**
 * Centralized application-wide constants.
 * <p>
 * Timeout values are loaded from {@code config.properties} at startup.
 * If a key is missing or invalid, defaults are applied automatically.
 * This ensures no hardcoded timeout values exist anywhere in the project.
 * </p>
 *
 * <h3>Configuration keys:</h3>
 * <ul>
 *   <li>{@code timeout.page.load} — page load timeout in seconds (default: 30)</li>
 *   <li>{@code timeout.explicit.wait} — explicit wait timeout in seconds (default: 15)</li>
 *   <li>{@code timeout.implicit.wait} — implicit wait timeout in seconds (default: 10)</li>
 * </ul>
 */
public class AppConstants {

    // ─── Timeout Defaults ───────────────────────────────────
    private static final int DEFAULT_PAGE_LOAD_TIMEOUT = 30;
    private static final int DEFAULT_EXPLICIT_WAIT = 15;
    private static final int DEFAULT_IMPLICIT_WAIT = 10;

    // ─── Configurable Timeout Values (loaded from config.properties) ──
    public static final int PAGE_LOAD_TIMEOUT = loadInt("timeout.page.load", DEFAULT_PAGE_LOAD_TIMEOUT);
    public static final int EXPLICIT_WAIT_TIMEOUT = loadInt("timeout.explicit.wait", DEFAULT_EXPLICIT_WAIT);
    public static final int IMPLICIT_WAIT_TIMEOUT = loadInt("timeout.implicit.wait", DEFAULT_IMPLICIT_WAIT);

    // ─── Page Titles ────────────────────────────────────────
    public static final String LOGIN_PAGE_TITLE = "Account Login";

    /**
     * Loads an integer value from config.properties.
     * Returns the provided default if the key is missing, blank, or not a valid integer.
     *
     * @param key          the property key
     * @param defaultValue fallback value
     * @return the parsed integer or the default
     */
    private static int loadInt(String key, int defaultValue) {
        try {
            String value = ConfigReader.getProperty(key, String.valueOf(defaultValue));
            return Integer.parseInt(value.trim());
        } catch (NumberFormatException e) {
            System.err.println("Invalid integer for config key '" + key
                    + "'. Using default: " + defaultValue);
            return defaultValue;
        }
    }
}
