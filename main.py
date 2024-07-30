from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from base import LoginPage  #import base classes
from amazonvideo import AmazonVideoPage
from discordpage import DiscordPage
from skypepage import SkypePage
from warnerturnerpage import WarnerturnerPage
from youtubekidspage import YoutubeKidsPage

class ErrorHandling:# handle diff. types of exceptions
    @staticmethod # class ın bir örneği olmadan çağırabilmek için staticmethod kullanılmıştır
    def handle_exception(e):
        if isinstance(e, ValueError):
            print(f"ValueError occurred: {e}")
        elif isinstance(e, TimeoutException):
            print(f"TimeoutException occurred: {e}")
        elif isinstance(e, WebDriverException):
            print(f"WebDriverException occurred: {e}")
        else:
            print(f"Unexpected error occurred: {e}")

if __name__ == '__main__':
    driver = webdriver.Chrome()

    sites = { #dict
        'AmazonVideo': AmazonVideoPage,
        'Discord': DiscordPage,
        'Skype':SkypePage,
        'WarnerTurner': WarnerturnerPage,
        'YoutubeKids': YoutubeKidsPage
    }

    try:
        site_name = input("please enter the site name: ( AmazonVideo, Discord, Skype, WarnerTurner, YoutubeKids): ")
        site_class = sites.get(site_name)

        if not site_class:
            print(f"site '{site_name}' is not listed above")
            driver.quit()
            exit()

        page = site_class(driver)  # create object page
        email = input("please enter your email address: ")
        password = input("please enter your password: ")
        duration = int(input("please enter the duration in sec. :"))
        if site_name in ('Discord', 'Skype'):
            page.video_call(duration, email, password)
        else:
            page.play_first_video(duration, email, password)# calling the method to play first video

    except Exception as e:
        ErrorHandling.handle_exception(e)
    finally:
        driver.quit()

class LoginPage(BasePage):
    def __init__(self, driver, email_locator, password_locator, login_button_locator, next_button_locator=None):
        super().__init__(driver)
        self.email_locator = email_locator
        self.password_locator = password_locator
        self.login_button_locator = login_button_locator
        self.next_button_locator = next_button_locator

    def login(self, email,password):
        self.send_keys(*self.email_locator, email)
        if self.next_button_locator: #next_button for two steps login
            self.click(*self.next_button_locator)
            time.sleep(3)
        self.send_keys(*self.password_locator, password)
        self.click(*self.login_button_locator)
