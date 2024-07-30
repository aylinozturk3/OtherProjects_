from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        try:
            self.driver.get(url)
            self.driver.maximize_window()
        except WebDriverException as e:
            print(f"Error opening URL: {e}")

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


class ConfigManager:
    @staticmethod
    def get_config(*args):
        return {"path": "some_path"}


class Setup:
    def __init__(self, driver, master):
        self.driver = driver
        self.master = master


class ErrorHandling:
    @staticmethod
    def handle_exception(e):
        if isinstance(e, ValueError):
            logging.error(f"ValueError occurred: {e}")
        elif isinstance(e, TimeoutException):
            logging.error(f"TimeoutException occurred: {e}")
        elif isinstance(e, WebDriverException):
            logging.error(f"WebDriverException occurred: {e}")
        else:
            logging.error(f"Unexpected error occurred: {e}")
class YahooVideo(BasePage):
    def __init__(self, setup:Setup)->None:
        super().__init__(setup)
        self.hostemail="ozturkaylin@yahoo.com"
        self.hostpassword="aylinA102HaV:p6-hMk"
        configs= ConfigManager.get_config("yahoovideo","LoginPage","")

        self.host_wdc.path_dictionary= configs

    def prepare_options(self, headless:bool= False)-> Options:
        options=Options()
        options.headless=headless
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        return options
    def prepare_starttraffic(self, uicontroller=WebDriverController, headless:bool=False, **kwargs) -> bool: #**kwargs: to allow a function to accept an arbitrary number of keyword arguments
        #bool değer döndürür
        options=self.prepare_options(headless=headless)#metodunu çağırarak tarayıcı seçeneklerini hazırlar ve belirtilen URL'yi açar
        ui_controller.open(driver_options=options,browser="chrome")#belirtilen tarayıcı seçenekleri ve tarayıcı türü ile tarayıcıyı açar

    def starttraffic(self,headless:bool=False,  **kwargs)->bool:
        self.prepare_starttraffic(self.host_wdc,headless=headless)
        try:
            self.login_withoutlogin(self.host_wdc)
            self.login_(self.host_wdc,self.hostemail,self.hostpassword)
        except Exception:
            pass
        result=self.start_first_video(self.host_wdc)
        return result
    def stoptraffic(self, ui_controller: WebDriverController):#tarayıcıyı kapatır
        rp.debug("stopping video on yahoovideo")
        ui_controller.close()

    def start_first_video(self, ui_controller: WebDriverController)->bool:
        result=True
        if ui_controller.wait_until("video","select_video",timeout=10):
            result &=ui_controller.find_element("video","select_video").click()
            if ui_controller.wait_until("video","play_button",timeout=10):
                result&=ui_controller.find_element("video","play_button").click()
            else:
                result &=ui_controller.find_element("video","play_button2",timeout=10)

        else:
            result &=ui_controller.get("")
        if ui_controller.wait_until("video","close_btn",timeout=30):
            result &=ui_controller.find_element("video","close_btn").click()

        rp.debug(f"result is {result}")
        ui_controller.sleep(3)
        rp.debug("starting video...")
        ui_controller.sleep(5)
        return result

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

            return True
        except Exception as e:
            ErrorHandling.handle_exception(e)
            return False

