from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from base import LoginPage  # Import your base class
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
class DiscordPage(LoginPage):
    def __init__(self, driver):
        super().__init__(driver, (By.XPATH, '//input[@name="email" and @type="text"]'),
                         (By.XPATH, "//input[@name='password' and @type='password']"),
                         (By.XPATH, "//button[@type='submit' and contains(@class, 'button_b83a05') and contains(@class, 'button_dd4f85') and contains(@class, 'lookFilled_dd4f85') and contains(@class, 'colorBrand_dd4f85') and contains(@class, 'sizeLarge_dd4f85') and contains(@class, 'fullWidth_dd4f85') and contains(@class, 'grow_dd4f85')]/div[text()='Giriş Yap']"))
        self.url = 'https://discord.com/'
        self.contact_locator = (By.XPATH, '//input[@class="input_f4e139" and @aria-label="Hızlı Geçiş"]')
        self.call_button = (By.XPATH, "//div[@class='iconWrapper_fc4f04 clickable_fc4f04' and @role='button' and @aria-label='Sesli Arama Başlat']")

    def video_call(self, duration, email, password):
        self.open_url(self.url)
        self.click(By.XPATH, '//a[@href="https://discord.com/login" and @data-track-nav="login"]')
        time.sleep(3)
        self.login(email, password)
        time.sleep(3)
        self.click(By.XPATH, '//button[contains(@class, "searchBarComponent_f0963d") and text()="Sohbet bul ya da başlat"]')
        time.sleep(3)

        kullanici_adi = str(input("Görüntülü konuşma yapmak istediğiniz hesap adını giriniz: "))
        search_box=self.find_element(By.XPATH, '//input[@class="input_f4e139"]')
        search_box.send_keys(kullanici_adi)
        time.sleep(3)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)

        self.start_call(duration, self.contact_locator, self.call_button)
