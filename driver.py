import threading

from functools import wraps

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains, Command
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select


class Driver:
    def __init__(self):
        driver_path = 'f:\\PyProjects\\fraud_downloader\\chromedriver.exe'

        # Class variables
        self.web_driver = None
        self.browser_lock = False
        self.headless = True
        self.notifications = False
        self.tabs = []

        options = Options()
        if self.notifications is False:
            options.add_argument('--disable-notifications')
            options.add_experimental_option("detach", True)
            #options.set_preference("dom.webnotifications.enabled", False)
        options.headless = self.headless

        # Assign proxy servers here
        proxy_list = []

        # Prob create selenium instance here
        if proxy_list is None or len(proxy_list) < 1:
            self.web_driver = webdriver.Chrome(executable_path=driver_path, options=options)
            print('[*] Browser driver has been initialized')
        else:
            # Set up proxy if 'proxy' variables' value is True
            proxy_server = Proxy()
            proxy_server.proxy_type = ProxyType.MANUAL
            proxy_server.http_proxy = proxy_list[0]

            capabilities = webdriver.DesiredCapabilities.CHROME
            proxy_server.add_to_capabilities(capabilities)
            print('[*] Browser driver has been initialized')
        print('[*] Opening Chrome browser..')
        print("[*] Notifications have been disabled for this session.")

        #self.tabs.append(self.web_driver.window_handles[-1])

    def browser_action(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                import time

                while True:
                    # Wait until browser is free
                    if self.browser_lock is True:
                        time.sleep(0.8)
                    else:
                        self.browser_lock = True
                        return func(self, *args, **kwargs)
            finally:
                self.browser_lock = False
        return wrapper

    def create_new_tab(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            self.web_driver.execute_script('window.open()')
            self.tabs.append(self.web_driver.window_handles[-1])

            return func(self, *args, **kwargs)
        return wrapper

    @browser_action
    @create_new_tab
    def open_url(self, url):
        try:
            self.web_driver.switch_to.window(self.tabs[-1])
            self.web_driver.get(url)
            self.wait()
        except Exception as ex:
            print("[*] Error -- " + str(ex))

    def wait(self, timeout=5):
        self.web_driver.implicitly_wait(timeout)

    def close(self):
        self.web_driver.quit()