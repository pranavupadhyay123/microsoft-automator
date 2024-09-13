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
edge_service_path = "./msedgedriver.exe"  # Adjust the path if necessary


# Function to create a new WebDriver instance with a specific user data directory
def create_driver(profile_path):
    edge_options = Options()
    edge_options.add_argument(f"user-data-dir={profile_path}")  # Specify the user data directory
    edge_options.add_argument("--profile-directory=Profile 1")  # Ensure we're using the correct profile
    edge_options.add_argument("--headless")  # Run in headless mode
    edge_options.add_argument("--disable-gpu")  # Disable GPU acceleration (might be needed for headless mode)
    return webdriver.Edge(service=Service(executable_path=edge_service_path), options=edge_options)


# List of profile paths for different accounts
profile_paths = [
    "C:/Users/Pranav/AppData/Local/Microsoft/Edge/User Data/Profile 2",
    "C:/Users/Pranav/AppData/Local/Microsoft/Edge/User Data/Profile 3",
    "C:/Users/Pranav/AppData/Local/Microsoft/Edge/User Data/Profile 4",
    "C:/Users/Pranav/AppData/Local/Microsoft/Edge/User Data/Profile 5",
    "C:/Users/Pranav/AppData/Local/Microsoft/Edge/User Data/Profile 6",
]

# Number of searches per account
searches_per_account = 20

# Iterate through each profile
for profile_path in profile_paths:
    print(f"Starting searches for profile: {profile_path}")

    # Initialize WebDriver for Edge using a specific user profile
    driver = create_driver(profile_path)

    try:
        # Open Bing search engine
        driver.get("https://www.bing.com")

        # Search random strings repeatedly
        for _ in range(searches_per_account):
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
            time.sleep(5)

        print(f"Completed searches for profile: {profile_path}")

    finally:
        # Close all tabs and quit the browser
        driver.quit()
        time.sleep(5)  # Ensure the WebDriver is properly closed before moving to the next profile

print("All profiles processed.")
