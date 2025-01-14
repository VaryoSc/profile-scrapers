import os
import time
from typing import List

import typer
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import generate_file, use_driver

app = typer.Typer()


@app.command()
def get_profile(users: List[str], driver=None):
    if not driver:
        driver = webdriver.Chrome()

    bio_class = "xc3tme8 x18wylqe x1xdureb x1iom2gc x1vnunu7 x172qv1o xs5motx x69nqbv xywrmq2 x6ikm8r x10wlt62"
    picture_class = "xpdipgo x972fbf xcfux6l x1qhh985 xm0m39n xk390pu x5yr21d xdj266r x11i5rnm xat24cr x1mh8g0r xl1xv1r xexx8yu x4uap5 x18d9i69 xkhd6sd x11njtxf xh8yej3"
    file_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + ".csv"

    for user_id in users:
        profile_photo_elm = f"{user_id}'s profile picture"
        url = f'https://www.instagram.com/{user_id}/'

        # Navigate to the Instagram page
        driver.get(url)

        print("Waiting for page to load...")

        # try:
        # Wait until the profile image is loaded
        #     WebDriverWait(driver, 60).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, picture_class))
        #     )
        #     print("Page loaded successfully!")
        # except Exception as e:
        #     print(f"Error waiting for the page to load}")
        #     driver.quit()
        #     exit()
        time.sleep(5)

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
        bio = soup.find("section", {"class": f"{bio_class}"}).text

        # Build the profile dictionary with image and bio
        profile = {
            "url": url,
            "image": soup.find('img', alt=profile_photo_elm).get("src") if soup.find('img',
                                                                                     alt=profile_photo_elm) else "Image not found",
            "bio": bio,
        }

        generate_file(user_id, file_name, list(profile.values()))


@app.command()
def login(users: List[str]):
    load_dotenv()

    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("PASSWORD")

    driver = use_driver()
    url = "https://www.instagram.com/accounts/login/"

    print("Waiting for page to load...")

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


if __name__ == "__main__":
    app()
