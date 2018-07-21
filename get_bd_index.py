from selenium import webdriver
import re
import time


def get_index_page(page_number):
    get_addr = "http://bi" + "gda" + "ve" + \
               "44" + ".com/page/" + str(page) + "/"
    print(get_addr)
    driver.get(get_addr)
    time.sleep(45)
    return driver.page_source


def save_index_page(page_number, page_source):
    with open("D:/projects/pycharm/bdpws/ind" + str(page_number) +
              ".html", encoding='utf-8', mode='w') as sp:
        sp.write(page_source)
        sp.close()


def get_dt_links(page_source):
    re_dt_links = re.compile(r'''
        http:\/\/bigdave44\.com        # base url
        \/                             # slash
        \d{4}                          # year
        \/                             # slash
        \d{2}                          # month
        \/                             # slash
        \d{2}                          # day
        \/                             # slash
        dt-\d{5,6}                     # page basename
        \/                             # slash
    ''', re.VERBOSE)
    links = re_dt_links.findall(page_source)
    return set(links)


def save_links(links):
    with open("D:/projects/pycharm/bdpws/save_links.txt",
              encoding='utf-8', mode='a') as sp:
        for link in links:
            print(link)
            sp.write(link + '\n')
        sp.close()


driver = webdriver.Firefox()

for page in range(5, 10):
    print("Getting page " + str(page))
    the_page_source = get_index_page(page)
    save_index_page(page, the_page_source)
    the_page_links = get_dt_links(the_page_source)
    save_links(the_page_links)

driver.close()
