import csv
import os
import time
from typing import List

import typer
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def get_profile(users: List[str], driver = webdriver.Chrome()):


    bio_class = "x7a106z x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x78zum5 xdt5ytf x2lah0s xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x11njtxf xskmkbu x1pjya6o x14cbv0q x7wvtww x9v3v6d x17eookw x1q548z6"
    picture_class = "xpdipgo x972fbf xcfux6l x1qhh985 xm0m39n xk390pu x5yr21d xdj266r x11i5rnm xat24cr x1mh8g0r xl1xv1r xexx8yu x4uap5 x18d9i69 xkhd6sd x11njtxf xh8yej3"
    file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".csv"

    for user_id in users:
        profile_photo_elm = f"{user_id}'s profile picture"
        url = f'https://www.instagram.com/{user_id}/'

        # Navigate to the Instagram page
        driver.get(url)

        print("Waiting for page to load...")

        try:
           # Wait until the profile image is loaded
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.CLASS_NAME, picture_class))
            )
            print("Page loaded successfully!")
        except Exception as e:
            print(f"Error waiting for the page to load: {e}")
            driver.quit()
            exit()


        # Get the page source after everything is loaded
        page_source = driver.page_source

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')


        # Set up headers to mimic a real browser request (optional, not used in this code snippet)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'csrftoken': 'zEDgus4QRkDOEhMYrt2KUKuFDV5Hj1i1',
            'datr': '3t1GZ_WyJLonsBiTIFX9ZXKv',
            'ds_user_id': '53397735863'
        }

        # Find the profile picture element (update the selector if necessary)
        # Extract bio section (adjust the class or selector)
        bio = soup.find("div", {"class": f"{bio_class}"}).text

        # Build the profile dictionary with image and bio
        profile = {
            "url": url,
            "image": soup.find('img', alt=profile_photo_elm).get("src") if soup.find('img', alt=profile_photo_elm) else "Image not found",
            "bio": bio,
        }

        with open(file_name, 'a', encoding="utf-8-sig") as products_file:
            writer = csv.writer(products_file)
            writer.writerow(list(profile.values()))
            print("Added profile!")

    # Quit the driver after scraping
    driver.quit()

users = ["mobinpiri9902"]
load_dotenv()

username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("PASSWORD")

print(username)
driver = webdriver.Chrome()
url = "https://www.instagram.com/accounts/login/"

print("Waiting for page to load...")

try:
    # Open the webpage
    driver.get(url)

    # Wait for the username field to be present
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))  # Adjust selector as needed
    )
    username_field.send_keys(username)

    # Wait for the password field to be present
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))  # Adjust selector as needed
    )
    password_field.send_keys(password)

    # Wait for the login button to be clickable
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))  # Adjust selector as needed
    )
    login_button.click()

    WebDriverWait(driver, 10).until(EC.url_changes(url))

    # Check if the URL contains the specific text
    current_url = driver.current_url
    if "https://www.instagram.com/auth_platform/codeentry" in current_url:
        print("On the verification page, waiting longer...")
        WebDriverWait(driver, 120).until(EC.url_changes(current_url))

    print("Getting user's profile...")
    get_profile(users, driver)
except Exception as e:
    print(f"Error waiting for the page to load: {e}")
    driver.quit()
    exit()
