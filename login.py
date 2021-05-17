import json
import time
import os.path
from os import path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

# check if there is existing cookies for the section
if path.exists("cookies.json") and path.getsize("cookies.json") != 0:
    driver.get("https://fantia.jp")

    with open('cookies.json', 'r') as cf:
        cookies = json.load(cf)
    # delete the old cookies and load in the new
    driver.delete_all_cookies()
    # load cookies
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
else:
    driver.get("https://fantia.jp/sessions/signin")
    # load username and password
    with open('config.json', 'r') as f:
        config = json.load(f)
    user = config["username"]
    pwd = config["password"]

    element = driver.find_element_by_name("user[email]")
    element.send_keys(user)
    element = driver.find_element_by_name("user[password]")
    element.send_keys(pwd)
    element = driver.find_element_by_xpath("/html/body/div[1]/main/div/div/div[1]/div/div/form/div[3]/button")
    element.click()

# storing the current window handle to get back to dashbord
main_page = driver.current_window_handle

time.sleep(1)
# store cookie
if not path.exists("cookies.json"):
    with open('cookies.json', 'w') as cf:
        json.dump(driver.get_cookies(), cf, indent = 6)

creators = driver.find_elements_by_class_name("item-creator")
# print(len(creators))
for i in range (len(creators)):
    creators = driver.find_elements_by_class_name("item-creator")  # reload because they got removed from the DOM (?)
    c = creators[i]
    c.click()
    time.sleep(1) # wait for the button to show up on the right bottom corner
    # Login started
    driver.find_element_by_class_name("fan-fixed-nav").click() # right bottom
    time.sleep(2)
    # do the login for twitter
    try:
        driver.find_element_by_xpath("//*[@id=\"fanclub-support-status-modal\"]/div/div[2]/div[2]/a").click()
        # switch to login twitter
        twitter_page = None
        for handle in driver.window_handles:
            if handle != main_page:
                twitter_page = handle
        driver.switch_to.window(str(twitter_page))
        # twitter login
        time.sleep(1)
        driver.find_element_by_name("session[username_or_email]").send_keys("a")
        driver.find_element_by_name("session[password]").send_keys("a")
        driver.find_element_by_xpath("//*[@id=\"layers\"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]").click()
        driver.close()
    except:
        print("Already got the twitter bonus.")

    driver.switch_to.window(main_page);
    # single daily login bonus
    if (i == len(creators)-1): # change the number for the one you want (n means the n+1th)
        try:
            driver.find_element_by_class_name("btn-yellow").click()
        except:
            print("Already done for single daily bouns")
    # go back the main menu
    driver.back()

# Mission complete
driver.quit()
