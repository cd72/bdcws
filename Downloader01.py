from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# for firefox https://github.com/mozilla/geckodriver/releases
# https://foxmask.net/post/2016/02/17/pycharm-running-flake8/

# This is a change
print("starting...")

driver = webdriver.Firefox()
#driver.set_window_size(800,600)
#driver.set_window_size(3000,2100)
#driver.get("https://www.whatismybrowser.com/")
driver.get("http://bi" +"gda" + "ve" + "44" + ".com/2018/07/13/dt-28790/")

# note correct version of webdriver required
3# https://stackoverflow.com/questions/51160562/in-python3-6-selenium-module-connectionabortederror-winerror-10053-an-esta



#driver.get("http://www.google.co.uk")
#assert "Python" in driver.title
#elem = driver.find_element_by_name("q")
#elem.clear()
#elem.send_keys("pycon")
#elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source

# sleep now
time.sleep(20)
#print(driver.page_source)

print ("got here")
driver.get("http://bi" +"gda" + "ve" + "44" + ".com/2018/07/13/dt-28790/")
time.sleep(20)

#print (driver.find_element_by_name('body').text)
print (driver.page_source )

save_path = 'save1.txt'
save_file = open(save_path, encoding='utf-8', mode='w')
save_file.write(driver.page_source)
save_file.close()
driver.close()


x = 6
print(x)

y = 6
assert x == y
