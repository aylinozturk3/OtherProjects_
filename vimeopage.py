from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from base import LoginPage2
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class VimeoPage(LoginPage2):
    def __init__(self, driver):
        super().__init__(driver, (By.XPATH, '@id=["email_login"]'),
                         (By.XPATH, '@id=["password_login"]'),
                         (By.XPATH, '//button[span[text()="Log in with an email"]]'))
        self.first_video_locator = (By.XPATH, "//span[@class='sc-hZSUBg eoTNMt' and .//span[contains(text(), 'Watch now')]]")
        self.url = 'https://vimeo.com/'

    def play_first_video(self,duration,email,password):
        try:
            self.open_url(self.url)
            sign_in_element= self.find_element(By.XPATH, "//button[contains(@class, 'box-border button') and contains(@class, 'bg-transparent')]")
            if sign_in_element:
                sign_in_element.click()
            else:
                print("Sign-in button is not found")
                return

            self.click(By.ID,'email_login')

            self.login(email,password)
            time.sleep(3)

            time.sleep(duration)

        except Exception as e:
            print(f"Error playing the first video: {e}")