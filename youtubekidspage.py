import json
import logging
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class WebDriverController:
    def __init__(self,driver):
        self.driver=driver
    def open(self, driver_options, browser):
        try:
            if browser=="chrome":
                self.driver=webdriver.Chrome(options=driver_options)
        except WebDriverException as e:
            print(f"Error opening URL: {e}")

    def close(self):
        try:
            self.driver.quit()
        except WebDriverException as e:
            print(f"Error closing browser: {e}")

    def get(self, url):
        try:
            self.driver.get(url)
        except WebDriverException as e:
            print(f"Error navigating to URL: {e}")




class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        try:
            self.driver.get(url)
            self.driver.maximize_window()
        except WebDriverException as e:
            print(f"Error opening URL: {e}")

class YoutubeKidsPage(BasePage):
        def __init__(self, driver, config):
            super().__init__(driver)
            self.config = config
            self.url = config.get('url', 'https://www.youtubekids.com')
            self.first_video_locator = (
            config['video']['select_video']['path'], config['video']['select_video']['type'])

        def load_config(self, filepath):
            with open(filepath, 'r') as file:
                return json.load(file)

        def select_account(self, account_num):
            try:
                accounts = self.driver.find_elements(By.CLASS_NAME, 'profile')
                accounts[account_num].click()
                time.sleep(5)
            except IndexError:
                logging.error(f"No account found at index {account_num}.")
                self.driver.quit()

        def enter_parent_details(self, year_input):
            self.click(By.ID, 'parent-button')
            time.sleep(5)
            self.click(By.ID, 'next-button')
            time.sleep(5)

            current_year = datetime.now().year
            numbers = [int(num) for num in str(year_input)]

            for i in range(1, 5):
                digit_input_id = f'//input[@id="onboarding-age-gate-digit-{i}"]'
                digit_input = self.driver.find_element(By.XPATH, digit_input_id)
                digit_input.send_keys(numbers[i - 1])
                time.sleep(2)

            if (current_year - year_input) < 18:
                logging.error("You are not old enough to be a parent.")
                self.driver.quit()
                exit()

            time.sleep(2)
            self.click(By.XPATH,
                       '//button[@id="submit-button" and @class="style-scope ytk-kids-onboarding-age-gate-renderer"]')
            time.sleep(5)

        def play_first_video(self, email, password, duration):
            self.open_url(self.url)
            try:
                user_type = input('Select: child or parent: ')
                if user_type == 'parent':
                    year_input = int(input('Please enter the year you were born in: '))
                    self.enter_parent_details(year_input)
                    self.play_video_flow(email, password, duration)
                else:
                    logging.error('Please ask a parent to set up YouTube Kids.')
                    self.driver.quit()
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                self.driver.quit()

        def play_video_flow(self, email, password, duration):
            try:
                self.driver.find_element(By.CLASS_NAME, 'video-stream')
                time.sleep(duration)

                self.click(By.XPATH,
                           '//button[@id="sign-in-info-next-button" and @class="style-scope ytk-kids-sign-in-info-renderer"]')
                time.sleep(5)

                self.click(By.ID, 'account-info-container')
                time.sleep(40)

                original_window = self.driver.current_window_handle
                for handle in self.driver.window_handles:
                    if handle != original_window:
                        self.driver.switch_to.window(handle)
                        break

                self.login(email, password)
                time.sleep(3)
                self.driver.switch_to.window(original_window)

                account_num = int(input("Enter the account number (starting from 0): "))
                self.select_account(account_num)
                time.sleep(3)

                self.click(By.XPATH, self.first_video_locator[0])
            except NoSuchElementException as e:
                logging.error(f"Element not found: {e}")
            except TimeoutException as e:
                logging.error(f"Timeout occurred: {e}")

        def prepare_options(self, headless: bool = False):
            options = Options()
            options.headless = headless
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-extensions")
            options.add_argument("--display=:99")
            return options

        def prepare_start_traffic(self, headless: bool = False):
            options = self.prepare_options(headless=headless)
            self.driver.open(driver_options=options, browser="chrome")

        def start_traffic(self, email, password, duration, headless: bool = False):
            self.prepare_start_traffic(headless=headless)
            self.play_first_video(email, password, duration)
        def login_withoutlogin(self,ui_controller:WebDriverController)->bool:#Navigates to the login page without performing login
              ui_controller.get("https://www.yahoo.com/entertainment/") #URL'yi açar
              ui_controller.wait_until("login","email",timeout=60)

        def login_(self, ui_controller: WebDriverController, email:str, password:str)->  bool: #Performs the login process using provided email and password
          try:
              email_field=ui_controller.find_element("login","email")
              email_field.send_keys(email)

              if ui_controller.wait_until("login","continue_button",timeout=10):
                  continue_btn=ui_controller.find_element("login","continue_button")
                  continue_btn.click()

                  ui_controller.sleep(5)

                  password_field=ui_controller.find_element("login","password")
                  password_field.send_keys(password)

                  login_btn=ui_controller.find_element("login","login_button")
                  login_btn.click()
              else:
                  password_field=ui_controller.find_element("login","password")
                  password_field.send_keys(password)

                  login_btn=ui_controller.find_element("login","login_button")
                  login_btn.click()

          except Exception as e:
              pass

# Config loading
config_path = 'youtubekids.json'
with open(config_path, 'r') as file:
    config = json.load(file)

# Driver initialization
driver = webdriver.Chrome()

# YoutubeKidsPage instantiation
youtube_kids_page = YoutubeKidsPage(driver, config)

# User credentials and video duration
email = 'ozturkaylin18@example.com'
password = 'aylinA102'
duration = 30  # Duration in seconds

# Start traffic
youtube_kids_page.start_traffic(email, password, duration)
