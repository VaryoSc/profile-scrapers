import csv

from selenium import webdriver


def use_driver():
    """placeholder code to generate the webdriver

    May upgrade later
    """
    driver = webdriver.Edge()
    return driver

def generate_file(user_id, file_name, content):
    with open(file_name, 'a', encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow([content['bio'], f'{user_id}'])
        print("Added profile!")