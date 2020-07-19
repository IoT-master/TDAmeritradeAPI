#!./.env/bin/python3
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from selenium.webdriver import Firefox, FirefoxProfile
# from selenium.webdriver import PhantomJS
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import os
from time import sleep


def delay_before(delay):
    def wrap(f):
        def wrapped_f(*args):
            sleep(delay)
            f(*args)
        return wrapped_f
    return wrap

def delay_after(delay):
    def wrap(f):
        def wrapped_f(*args):
            f(*args)
            sleep(delay)
        return wrapped_f
    return wrap


class DelayBefore(object):
    def __init__(self, delay):
        self.delay = delay

    def __call__(self, func):
        def wrapper(*args):
            sleep(self.delay)
            func_return = func(*args)
            return func_return
        return wrapper


class LoginClass(object):

    def __init__(self, incognito=True, headless=False, brave=False):
        options = ChromeOptions()
        options.add_argument("disable-extensions")
        if incognito:
            options.add_argument("incognito")
        if headless:
            options.add_argument("headless")

        # options.add_argument("disable-gpu")
        # options.add_argument('window-size=1200x1200')
        # options.add_argument("remote-debugging-port=9222")
        # options.add_argument("kiosk")

        if os.name == 'nt':
            # path_to_chrome = str(Path('./chromedriver.exe').relative_to('.'))
            path_to_chrome = str(
                Path('./ChromeDrivers/Windows/chromedriver.exe').absolute())
        elif os.name == 'posix':
            path_to_chrome = str(
                Path('./ChromeDrivers/Mac/chromedriver').absolute())
        else:
            if brave:
                options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
            path_to_chrome = str(
                Path('./ChromeDrivers/Linux/chromedriver').absolute())
        self.browser = Chrome(path_to_chrome, options=options)

    def logging_in(self, url):
        self.browser.get(url)

    def wait_until_css_element_object_found(self, css_param, wait_time=10):
        wait = WebDriverWait(self.browser, wait_time)
        wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, css_param)))

    def scroll_down_one_page(self, lines_down):
        self.browser.execute_script(
            "window.scrollTo(0, " + str(lines_down) + ")")

    def drag_and_drop(self, source_element_object, destination_element_object):
        ActionChains(self.browser).drag_and_drop(
            source_element_object, destination_element_object).perform()

    def hover_over(self, element_object):
        ActionChains(self.browser).move_to_element(element_object).perform()

    def is_present(self, element_object):
        try:
            # browser.find_element_by_css_selector("div")
            if element_object.is_displayed():
                return True
        except:
            return False

    def update_browser(self):
        for handle in self.browser.window_handles:
            self.browser.switch_to.window(handle)

    def wait_until_name_element_object_found(self, name_param, wait_time=10):
        wait = WebDriverWait(self.browser, wait_time)
        wait.until(EC.visibility_of_element_located((By.NAME, name_param)))

    def wait_until_partial_link_text_element_object_found(self, partial_link_text, wait_time=10):
        wait = WebDriverWait(self.browser, wait_time)
        wait.until(EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, partial_link_text)))

    def wait_until_class_name_element_object_found(self, class_name, wait_time=10):
        wait = WebDriverWait(self.browser, wait_time)
        wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, class_name)))

    def wait_until_id_element_object_found(self, id_object, wait_time=10):
        wait = WebDriverWait(self.browser, wait_time)
        wait.until(EC.visibility_of_element_located((By.ID, id_object)))

    def wait_until_partial_link_text_object_found(self, id_object, wait_time=10):
        wait = WebDriverWait(self.browser, wait_time)
        wait.until(EC.visibility_of_element_located(
            (By.PARTIAL_LINK_TEXT, id_object)))

    def multi_select_in_list(self, element_objects, labels):
        for option in element_objects:
            if option.text in labels:
                option.click()

    def select_in_list(self, element_objects, labels):
        for option in element_objects:
            if option.text in labels:
                option.click()
                break


if __name__ == '__main__':
    fetching_token = LoginClass()
    fetching_token.logging_in('https://www.google.com')
