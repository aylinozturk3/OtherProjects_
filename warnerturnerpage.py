from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from base import LoginPage  # Import base class
import time

class WarnerturnerPage(LoginPage):
    def __init__(self, driver):
        super().__init__(driver, (By.ID, 'edit-name'),
                         (By.ID, 'edit-pass'),
                         (By.XPATH, '//input[@name="op"]'))
        self.url = 'https://press.wbd.com/us/'
        self.video_locator = (By.CLASS_NAME, 'style-scope')


    def play_first_video(self, duration, email, password):
        self.open_url(self.url)
        self.click(By.XPATH, "//a[@href='/us/user/login' and contains(@class, 'button') and contains(@class, 'button--dark')]")
        time.sleep(3)

        self.login(email, password)
        try:
            self.click(By.XPATH, "//ul[@class='menu-navigation']//li[contains(@class, 'link-15')]")
            time.sleep(3)

            divs = self.driver.find_elements(By.CSS_SELECTOR, '.m-brands-icon-list__element.col')
            index = int(input("Enter the index of the div to click: "))
            if 0 <= index < len(divs):
                divs[index].click()
            else:
                print("Index out of range. Please enter a valid index.")

            self.click(By.CSS_SELECTOR, 'figure.m-item-content-row__thumbnail')
            time.sleep(5)

            link_elements = self.driver.find_elements(By.LINK_TEXT, "HERE")
            if link_elements:
                actions = ActionChains(self.driver)
                actions.move_to_element(link_elements[0]).perform()
                time.sleep(2)  # wait for a bit to ensure the element is in view
                link_elements[0].click()

                video_duration=self.driver.execute_script("return document.querySelector('video').duration;")
                print(f"video: {video_duration} sec.")
                if duration < video_duration:
                    starttime = time.time()
                    while True:
                        currenttime = time.time()
                        elapsedtime = currenttime - starttime
                        if elapsedtime >= duration:
                            break
                else:
                    time.sleep(video_duration)
            else:
                print("There is no video on that page")
        finally:
            self.driver.quit()

