import time
import random
import string
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

def generate_random_string(length=10):
    letters = string.ascii_lowercasey
    return ''.join(random.choice(letters) for i in range(length))

edge_service_path = "./msedgedriver.exe"  # Adjust the path if necessary

def create_driver(profile_path):
    edge_options = Options()
    edge_options.add_argument(f"user-data-dir={profile_path}")
    edge_options.add_argument("--headless")
    edge_options.add_argument("--disable-gpu")
    return webdriver.Edge(service=Service(executable_path=edge_service_path), options=edge_options)

def get_all_profile_paths(include_default=False):
    base_path = os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data")
    profile_paths = []
    for item in os.listdir(base_path):
        if item.startswith("Profile ") or (include_default and item == "Default"):
            full_path = os.path.join(base_path, item)
            profile_paths.append((item, full_path))
    return profile_paths

searches_per_account = 20

# Get all profiles and display them
all_profiles = get_all_profile_paths(include_default=True)
print("Detected profiles:")
for i, (profile_name, profile_path) in enumerate(all_profiles, 1):
    print(f"{i}. {profile_name}: {profile_path}")

# Ask user if they want to include the default profile
include_default = input("Include default profile? (y/n): ").lower() == 'y'

# Filter profiles based on user choice
profile_paths = [path for name, path in all_profiles if include_default or name != "Default"]

print(f"\nWill process {len(profile_paths)} profiles.")

for profile_path in profile_paths:
    print(f"\nStarting searches for profile: {profile_path}")

    driver = create_driver(profile_path)

    try:
        driver.get("https://www.bing.com")

        for i in range(searches_per_account):
            random_string = generate_random_string()

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])

            driver.get("https://www.bing.com")

            search_box = driver.find_element("name", "q")
            search_box.clear()
            search_box.send_keys(random_string)
            search_box.send_keys(Keys.RETURN)

            print(f"Search {i+1}/{searches_per_account}: {random_string}")

            time.sleep(5)

        print(f"Completed searches for profile: {profile_path}")

    finally:
        driver.quit()
        time.sleep(5)

print("All profiles processed.")