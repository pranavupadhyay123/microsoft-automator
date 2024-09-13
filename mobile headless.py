import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# Function to generate a random string of given length
def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Path to msedgedriver.exe
edge_service = Service(executable_path="./msedgedriver.exe")  # Adjust the path if necessary

# Set up Edge WebDriver with headless and mobile emulation options
edge_options = Options()
edge_options.add_argument("--headless")  # Run in headless mode

# Set a user agent string for Android 14 on Redmi 12 5G
android_user_agent = (
    "Mozilla/5.0 (Linux; Android 14; Redmi 12 5G Build/ABCD1234) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/117.0.0.0 Mobile Safari/537.36"
)
edge_options.add_argument(f"user-agent={android_user_agent}")

# Initialize WebDriver for Edge using Selenium's native support
driver = webdriver.Edge(service=edge_service, options=edge_options)

# Set viewport size to simulate the Redmi 12 5G screen dimensions
driver.set_window_size(1080, 2400)  # Example dimensions for a Redmi 12 5G

# Open Bing search engine
driver.get("https://www.bing.com")

# Search random strings repeatedly
for _ in range(10):
    random_string = generate_random_string()

    # Open a new tab
    driver.execute_script("window.open('');")
    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])

    # Open Bing search engine in the new tab
    driver.get("https://www.bing.com")

    # Find the search box, type the random string, and hit Enter
    search_box = driver.find_element("name", "q")
    search_box.clear()  # Clear the search box before entering the next query
    search_box.send_keys(random_string)
    search_box.send_keys(Keys.RETURN)

    print(f"Searching for: {random_string}")

    # Wait for a few seconds before the next search (optional)
    time.sleep(20)

# Close all tabs and quit the browser
driver.quit()
