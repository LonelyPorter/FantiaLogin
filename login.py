import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://fantia.jp/sessions/signin")

# storing the current window handle to get back to dashbord
main_page = driver.current_window_handle

# load username and password
with open('config.json', 'r') as f:
    config = json.load(f)
user = config["username"]
pwd = config["password"]

element = driver.find_element_by_name("user[email]")
element.send_keys(user)
element = driver.find_element_by_name("user[password]")
element.send_keys(pwd)
element.submit()

creators = driver.find_elements_by_class_name("item-creator")
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
        driver.find_element_by_name("session[username_or_email]").send_keys("a")
        driver.find_element_by_name("session[password]").send_keys("a")
        driver.find_element_by_xpath("//*[@id=\"layers\"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]").click()
        driver.close()
    except:
        print("Already got the twitter bonus.")

    driver.switch_to.window(main_page);
    # single daily login bonus
    if (i == 6): # change the number for the one you want (n means the n+1th)
        try:
            driver.find_element_by_class_name("btn-yellow").click()
        except:
            print("Already done for single daily bouns")
    # go back the main menu
    driver.back()

# Mission complete
driver.quit()
