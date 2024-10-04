from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Set up Chrome options
chrome_options = Options()

# Disable JavaScript
chrome_options.add_experimental_option("prefs", {
    "profile.managed_default_content_settings.javascript": 2
})

# Disable cookies (block them completely)
chrome_options.add_argument("--disable-cookies")

# You can also launch Chrome in Incognito mode to prevent cookie storage
chrome_options.add_argument("--incognito")

# Initialize the WebDriver with the Chrome options
driver = webdriver.Chrome(options=chrome_options)

# Open the target URL (for testing)
driver.get("https://nypost.com")

# You can interact with the page (without JavaScript or cookies being enabled)
print("Page title is: ", driver.title)

# Close the browser after you're done
driver.quit()
