from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import re
import os.path
import time
import random

def get_dt_page(dt_url):
    print(dt_url)
    try:
        driver.get(dt_url)
    except TimeoutException as te:
            print ("Exception" + str(te))
    print ("got it")
    time.sleep(45)
    return driver.page_source


def get_save_file_name(dt_url):
    re_dt_page_name = re.compile(r"(dt-\d{5})")
    m = re_dt_page_name.search(dt_url)
    if m:
        file_base_name=m.group()
    else:
        raise(ValueError, 'Invalid dt url', dt_url)

    print(file_base_name)
    full_file_name="dts/" + file_base_name + ".html"
    print(full_file_name)
    return full_file_name


def save_dt_page(full_file_name, page_source):
    with open(full_file_name, encoding='utf-8', mode='w') as sp:
        sp.write(page_source)
        sp.close()


driver = webdriver.Firefox()
driver.set_page_load_timeout(30)

with open("save_links.txt", encoding='utf-8') as url_file:
    for dt_url in url_file:
        save_name = get_save_file_name(dt_url)
        if os.path.isfile(save_name):
            print(f"File {save_name} already exists")
        else:
            the_page_source=get_dt_page(dt_url)
            save_dt_page(save_name, the_page_source)
            print("saved")
            time.sleep(random.randint(40,50))
            print("sleep done")

driver.close()

