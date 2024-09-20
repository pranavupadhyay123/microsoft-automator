import os
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

os.system("taskkill /F /IM msedge.exe")

def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def create_driver(profile_directory):
    edge_options = Options()

    profile_path = "C:/Users/pranav/AppData/Local/Microsoft/Edge/User Data"
    edge_options.add_argument(f"user-data-dir={profile_path}")
    edge_options.add_argument(f"--profile-directory={profile_directory}")
    edge_options.add_argument("--headless")

    return webdriver.Edge(service=Service(executable_path=edge_service_path), options=edge_options)

def list_profile_directories(base_path):
    directories = []
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path) and (item.startswith('Profile ') or item == 'Default'):
            directories.append(item)
    return directories

def get_profile_range(profiles):
    print(f"Available profiles: {profiles}")
    start = int(input("Enter the starting profile number: "))
    end = int(input("Enter the ending profile number: "))
    
    if start >= 0 and end < len(profiles):
        return profiles[start:end + 1]
    else:
        print("Invalid range. Please try again.")
        return get_profile_range(profiles)

edge_service_path = "./msedgedriver.exe"
profile_base_path = "C:/Users/pranav/AppData/Local/Microsoft/Edge/User Data"
profile_directories = list_profile_directories(profile_base_path)

# Get the range of profiles
profile_range = get_profile_range(profile_directories)

for profile in profile_range:
    print(f"Using profile: {profile}")
    driver = create_driver(profile)

    try:
        driver.get("https://www.bing.com")

        for i in range(12):
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
