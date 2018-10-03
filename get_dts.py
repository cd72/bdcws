from selenium import webdriver
import re
import time
import random
import logging.config

def get_index_page():
    get_addr = "http://bi" + "gda" + "ve" + \
               "44" + ".com"
    logger.info(get_addr)
    driver.get(get_addr)
    time.sleep(15)
    return driver.page_source

def find_dt_link_elems():
    dt_elems=[]
    dt_links1 = driver.find_elements_by_partial_link_text("DT")
    for link in dt_links1:
        if re.match(r'''.+dt-\d{5}/$''', link.get_attribute('href')):
            logger.debug(link.text, link.get_attribute('href'))
            dt_elems.append(link)
    return dt_elems

def check_get_dts(dt_link_elems):
    for link in dt_link_elems:
        dt_url
        logger(f"Checking {link.get_attribute('href')")

dt_links1 = driver.find_elements_by_partial_link_text("DT")
for link in dt_links1:
    if re.match(r'''.+dt-\d{5}/$''', link.get_attribute('href')):
        print (link.text)
        print (link.get_attribute('href'))




def main():
    driver = webdriver.Firefox()

    index_page = get_index_page()
    dt_link_elems = find_dt_link_elems()
    check_get_dts(dt_link_elems)

    driver.close()


logging.config.fileConfig('logging.conf')
logger = logging.getLogger(__name__)
if __name__ == '__main__':
    main()