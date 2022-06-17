import logging
import platform
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import options
from selenium.webdriver.support.ui import WebDriverWait


class SecureSelenium():
    def __init__(self, webdriver_path: str,
                 headless: bool,
                 user_agent: str = None,
                 window_width: int = 1200,
                 window_length: int = 800,
                 wait_sec_min: int = 3,
                 wait_sec_max: int = 5,
                 proxy: str = None):
        """Create webdriver and pass in browser settings.

        Args:
            webdriver_path: Full path to webdriver
            headless: Set True to run without monitor
            user_agent: Web user agent to look like
            window_width: Width of browser in pixels
            window_length: Length of browser in pixels
            wait_sec_min: Minimum seconds to wait between Selenium
                requests to websites
            wait_sec_max: Maximum seconds to wait between Selenium
                requests to websites
            proxy: Pass in proxy address and port. Must be http:// in prefix
                even if connection is https://
        """
        self.webdriver_path = webdriver_path
        self.headless = headless
        self.user_agent = self._get_user_agent(user_agent)
        self.window_width = window_width
        self.window_length = window_length
        self.wait_sec_min = wait_sec_min
        self.wait_sec_max = wait_sec_max
        self.proxy = proxy

        browser_options = options.Options()

        # Remove bot-like qualities
        # Other things to consider:
        #   Also make sure user agent matches platform.
        #   Search for "cdc_asdjflasutopfhvcZLmcfl_" in webdriver
        #   and replace with same length string.
        browser_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        browser_options.add_experimental_option(
            "useAutomationExtension", False)
        browser_options.add_argument(
            "--disable-blink-features=AutomationControlled")
        browser_options.add_argument(
            f"window-size={self.window_width},{self.window_length}")
        browser_options.add_argument("disable-infobars")  # disabling infobars
        # overcome limited resource problems
        browser_options.add_argument("--disable-dev-shm-usage")
        # Bypass OS security model
        browser_options.add_argument("--no-sandbox")
        browser_options.add_argument(f"user-agent={self.user_agent}")
        if self.proxy:
            browser_options.add_argument(f"--proxy-server={self.proxy}")
        browser_options.headless = self.headless

        self.webdriver = webdriver.Chrome(
            self.webdriver_path, options=browser_options)
        self.webdriver.implicitly_wait(self.wait_sec_min)

    def get(self, url):
        """Make request to target URL.

        Args:
            url: Endpoint to call
        """
        logging.info("Waiting between %s and %s seconds.",
                     self.wait_sec_min, self.wait_sec_max)
        time.sleep(random.randint(self.wait_sec_min, self.wait_sec_max))
        self.webdriver.get(url)

    def close(self):
        """Close webdriver."""
        self.webdriver.close()

    def _initial_cookies(self):
        """Visit some websites for the browser to pick up cookies.

        Websites can check if cookies are present.  Some websites may
        find it suspicious no cookies exist.
        """
        # Gather cookies to avoid bot qualities
        self.webdriver.get("https://google.com")
        time.sleep(random.randint(self.wait_sec_min, self.wait_sec_max))
        self.webdriver.get("https://google.com/search?q=cookies")

    def _get_user_agent(self, user_agent_param) -> str:
        """Build user agent to avoid security on websites.

        Args:
            user_agent_param: User defined parameter

        Returns: Create a user agent if one is not supplied.
        """
        logging.info("Looking for supplied user agent.")
        if user_agent_param:
            return user_agent_param

        logging.info("No user agent supplied, building one...")
        machine: str = f"{platform.machine()}" if platform.machine(
        ) is not None else ""

        user_agent: str = (f"Mozilla/5.0 (X11; {platform.system()}{machine}) "
                           + "AppleWebKit/537.36 (KHTML, like Gecko) "
                           + "Chrome/{self.chrome_version} Safari/537.36")
        logging.info(user_agent)
        return user_agent
