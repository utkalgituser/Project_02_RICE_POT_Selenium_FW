package utils;

import org.jspecify.annotations.NonNull;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Objects;
import java.util.Properties;

/**
 * Reads configuration key-value pairs from {@code config.properties}.
 * <p>
 * This class guarantees <strong>non-null</strong> return values.
 * If a required key is missing or blank, a descriptive
 * {@link RuntimeException} is thrown immediately — preventing
 * silent null propagation into downstream code.
 * </p>
 */
public class ConfigReader {

    private static final Properties properties;

    static {
        try {
            FileInputStream fileInputStream = new FileInputStream("src/test/resources/config.properties");
            properties = new Properties();
            properties.load(fileInputStream);
            fileInputStream.close();
        } catch (IOException e) {
            throw new RuntimeException("Could not load config.properties file.", e);
        }
    }

    /**
     * Returns the value for the given key from config.properties.
     * <p>
     * This method is null-safe — it throws immediately if the key
     * is not found, rather than returning null.
     * </p>
     *
     * @param key the property key to look up (must not be null)
     * @return the non-null, trimmed property value
     * @throws RuntimeException if the key is missing from config.properties
     */
    public static @NonNull String getProperty(@NonNull String key) {
        Objects.requireNonNull(key, "Config key must not be null.");
        String value = properties.getProperty(key);
        if (value == null) {
            throw new RuntimeException(
                    "Missing required config key: '" + key
                            + "'. Please add it to src/test/resources/config.properties");
        }
        return Objects.requireNonNull(value.trim());
    }

    /**
     * Returns the value for the given key, or a default if the key is missing.
     * <p>
     * Use this for <strong>optional</strong> configuration properties
     * where a sensible default exists (e.g., timeout overrides).
     * </p>
     *
     * @param key          the property key to look up
     * @param defaultValue the fallback value if the key is absent
     * @return the property value, or defaultValue if not found
     */
    public static @NonNull String getProperty(@NonNull String key, @NonNull String defaultValue) {
        Objects.requireNonNull(key, "Config key must not be null.");
        Objects.requireNonNull(defaultValue, "defaultValue must not be null.");
        String value = properties.getProperty(key);
        return (value != null) ? Objects.requireNonNull(value.trim()) : defaultValue;
    }
}
