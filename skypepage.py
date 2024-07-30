from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from base import LoginPage  # Import your base class
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SkypePage(LoginPage):
    def __init__(self, driver):
        super().__init__(driver, (By.XPATH, "//input[@id='i0116']"),
                         (By.XPATH, "//input[@id='i0118']"),
                         (By.XPATH, "//button[@id='idSIButton9']"),
                         (By.XPATH, "//button[@id='idSIButton9']"))
        self.url = 'https://www.skype.com/tr/'
        self.call_button = (By.XPATH, "//button[@role='button' and @title='Sesli Arama']")

    def video_call(self, duration, email, password):
        self.open_url(self.url)
        time.sleep(3)
        self.click(By.XPATH, "//a[@aria-label='Open Skype in your browser']")
        time.sleep(3)
        self.login(email, password)
        time.sleep(10)  # evet hayır seç manuel
        # buraya kadar OKEY!
        kullanici_adi = str(input("Konuşmak istediğiniz kişinin kullanıcı adını giriniz: "))


        search_box1=WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Kişiler, gruplar, iletiler, web' and @role='button']")))
        search_box1.click()
        time.sleep(2)
        search_box2 = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="text" and @aria-label="Skype\'ta Ara"]')))
        search_box2.clear()
        search_box2.send_keys(kullanici_adi)
        time.sleep(2)
        for _ in range(2): # 2 kere enter girilir
            search_box2.send_keys(Keys.RETURN)
            time.sleep(1)

        self.click(*self.call_button)
        time.sleep(duration)



