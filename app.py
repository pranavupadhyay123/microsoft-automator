import os
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def create_driver(profile_directory):
    edge_options = Options()

    # Path to your Edge profiles
    profile_path = "C:/Users/pranav/AppData/Local/Microsoft/Edge/User Data"

    # Use the profile that is already logged in
    edge_options.add_argument(f"user-data-dir={profile_path}")
    edge_options.add_argument(f"--profile-directory={profile_directory}")
    edge_options.add_argument("--headless")  # Remove if you want to see the browser

    # Create the WebDriver instance
    return webdriver.Edge(service=Service(executable_path=edge_service_path), options=edge_options)

def list_profile_directories(base_path):
    directories = []
    # Edge profiles are typically in subdirectories within 'User Data'
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path) and item.startswith('Profile ') or item == 'Default':
            directories.append(item)
    return directories

edge_service_path = "./msedgedriver.exe"  # Adjust the path if necessary

# Path to your Edge profiles
profile_base_path = "C:/Users/pranav/AppData/Local/Microsoft/Edge/User Data"

# Automatically detect profile directories
profile_directories = list_profile_directories(profile_base_path)

# Iterate over each profile and perform searches
for profile in profile_directories:
    print(f"Using profile: {profile}")
    driver = create_driver(profile)

    try:
        driver.get("https://www.bing.com")

        for i in range(20):  # Example loop to perform searches
            random_string = generate_random_string()
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get("https://www.bing.com")
            search_box = driver.find_element("name", "q")
            search_box.clear()
            search_box.send_keys(random_string)
            search_box.send_keys(Keys.RETURN)

            print(f"Profile: {profile}, Search {i + 1}: {random_string}")
            time.sleep(5)

    finally:
        driver.quit()
