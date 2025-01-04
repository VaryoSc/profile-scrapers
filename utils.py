import csv

from selenium import webdriver


def use_driver():
    """placeholder code to generate the webdriver

    May upgrade later
    """
    options = webdriver.EdgeOptions()
    options.unhandled_prompt_behavior = 'dismiss'
    options.add_argument("--disable-notifications")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.popups": 0,
    })
    driver = webdriver.Edge(options=options)
    return driver


def generate_file(user_id, file_name, content):
    with open(file_name, 'a', encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        content.append(user_id)
        writer.writerow(content)
        print("Added profile!")
