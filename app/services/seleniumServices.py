import datetime
import random
import time
import json
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from app.config import Config
import os

class Twitter_Trend_Scraper:
    def __init__(self, manual_verify_timeout=300):
        self.manual_verify_timeout = manual_verify_timeout
        self.setup_driver()

    def setup_driver(self):
        options = webdriver.ChromeOptions()

        # options.add_argument("--disable-gpu")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # SEtting up proxymesh things
        PROXY_USERNAME = Config.PROXY_USERNAME
        PROXY_PASSWORD = Config.PROXY_PASSWORD
        PROXY_HOST = Config.PROXY_HOST
        PROXY_PORT = Config.PROXY_PORT

        # options.add_argument(f'--proxy-server=http://{PROXY_HOST}:{PROXY_PORT}')
        # options.add_argument(f'--proxy-auth={PROXY_USERNAME}:{PROXY_PASSWORD}')
        # options.add_argument(f'--proxy-bypass-list=<-loopback>')

        self.driver = webdriver.Chrome(options=options)

    #simulating human like typing to avoid the detection
    def simulate_human_typing(self, element, text):
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

    # If any captcha code or otp is needed to enter then the app will wait for the input to be entered
    def wait_for_manual_verification(self):
        print("\n=== MANUAL VERIFICATION REQUIRED ===")
        print("Please complete the verification in the browser.")
        print(f"You have {self.manual_verify_timeout} seconds to complete it.")
        print("The script will continue automatically once verification is completed.")
        print("===================================\n")

        # storing the initial verification url
        initial_url = self.driver.current_url
        start_time = time.time()

        while time.time() - start_time < self.manual_verify_timeout:
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            # print(f'PRINTING THE PAGE SOURCE: \n{page_source}')
            if current_url != initial_url and not any([
                "verify" in current_url,
                "verification" in current_url,
                "confirm" in current_url,
                "challenge" in current_url,
                "authenticate" in current_url
            ]):
                print("\nVerification completed successfully! Redirected to:", current_url)
                time.sleep(2)  # Give a moment for any redirects to complete
                return True

            # List of indicators that we're still on a verification page
            verification_indicators = [
                "verification" in page_source,
                "verify" in page_source,
                "confirmation" in page_source,
                "confirm your identity" in page_source,
                "enter the code" in page_source,
                "verify your phone" in page_source,
                "verify your email" in page_source
            ]

            if not any(verification_indicators):
                print(f'\nVerification Completed Successfully!')
                time.sleep(2)
                return True

            # Waiting before checking again
            time.sleep(1)

        print("\nVerification timeout reached, Please try again")
        return False

    # In case verification code is required Then we will have to manually enter the
    def check_for_verification(self):
        try:
            verification_elements = self.driver.find_elements(By.XPATH,
                                                              "//*[contains(text(),'verification') or contains(text(), 'Verify') or \
                                                              contains(text(),'confirm') or contains(text(),'Confirm') or \
                                                              contains(text(),'Enter the code')]"
                                                              )
            if verification_elements:
                # Wait for manual verification to complete
                if self.wait_for_manual_verification():
                    return True
                else:
                    raise Exception("Verification timeout - please try again")

        except NoSuchElementException:
            pass
        return True

    # wait for the element to render
    def wait_for_element(self, by, value, timeout=10):
        try:
            # explicit wait
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except TimeoutException:
            return None

    def is_home_page(self):
        try:
            home_indicators = [
                'home' in self.driver.current_url.lower(),
            ]

            return any(home_indicators)

        except Exception:
            return False

    def check_for_input_type(self):
        page_source = self.driver.page_source

        if 'Enter your password' in page_source:
            return 'password'
        elif 'Enter your phone number or email address' in page_source:
            return 'email_or_phone'
        elif 'Enter your phone number or username' in page_source:
            return 'phone_or_username'
        elif 'Sign in to X' in page_source:
            return 'username'
        elif any(text in page_source.lower() for text in ['verification code', 'confirm your identity']):
            return 'verification'
        return None

    def handle_input_type(self, input_type, value):
        input_selectors = {
            'password': 'input[name="password"]',
            'email_or_phone': 'input[data-testid="ocfEnterTextTextInput"]',
            'phone_or_username': 'input[data-testid="ocfEnterTextTextInput"]',
            'username': 'input[autocomplete="username"]'
        }

        selector = input_selectors.get(input_type)
        if not selector:
            return False

        try:
            input_field = self.wait_for_element(By.CSS_SELECTOR, selector)

            if input_field:
                if input_type == 'email_or_phone' and '@' in value:
                    self.simulate_human_typing(input_field, value)
                elif input_type == 'phone_or_username' and not value.startswith('+'):
                    self.simulate_human_typing(input_field, value)
                else:
                    self.simulate_human_typing(input_field, value)

                time.sleep(random.uniform(0.5, 1.5))

                input_field.send_keys(Keys.ENTER)

                time.sleep(3)
                return True

        except Exception as e:
            print(f"Error Handling {input_type} input: {e}")
        return False

    def login(self, username: str, password: str, email: str):
        try:

            self.driver.get("https://x.com/i/flow/login")
            # time.sleep(30)
            # self.driver.implicitly_wait(30)
            max_steps = 5
            step_count = 0
            # we will only try 5 times

            while step_count < max_steps:
                time.sleep(3)

                if self.is_home_page():
                    return True

                current_input = self.check_for_input_type()
                # print(f'Current Input type: {current_input}')

                if current_input == 'username':
                    self.handle_input_type('username', username)
                elif current_input == 'password':
                    self.handle_input_type('password', password)
                elif current_input == 'email_or_phone':
                    self.handle_input_type('email_or_phone', email)
                elif current_input == 'phone_or_username':
                    self.handle_input_type('username', username)
                elif current_input == 'verification':
                    if not self.wait_for_manual_verification():
                        return False
                else:
                    time.sleep(300)
                    print(f"Unknown input field {current_input}")
                    return False

                step_count += 1
                time.sleep(2)

            return self.is_home_page()

        except Exception as e:
            print(f"error logging in : {e}")

        return False

    def get_ip_address(self):
        try:
            time.sleep(5)
            self.driver.get("http://httpbin.org/ip")
            response = self.driver.find_element(By.TAG_NAME, "body").text
            data = json.loads(response)
            return data['origin']
        except Exception as e:
            print(f"Error fetching IP address: {e}")
            return None

    def fetch_trends(self):
        try:
            # to get it from the explore tabs for you page
            self.driver.get("https://x.com/explore/tabs/for-you")
            time.sleep(5)

            try:
                no_button = self.driver.find_element(By.XPATH, "//button[@aria-label='Close']")

                no_button.click()
            except:
                print(f'No Two factor button')

            # to get it from the home page whats happening

            trending_data = []
            # home_page_data = self.driver.find_element(By.XPATH,"//div[@class='css-146c3p1 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1xuzw63']")
            fetched_data = self.driver.find_elements(By.XPATH,
                                                     "//div[@class='css-146c3p1 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-b88u0q r-1bymd8e']")

            for data in fetched_data:
                # print(f'Printing trending topic: {data.text}')
                trending_data.append(data.text)

            return trending_data


        except Exception as e:
            print(f'Error Fetching the trends {e}')
            return None

    def close(self):
        self.driver.quit()


def login_and_fetch_x_trends():
    scrapper = Twitter_Trend_Scraper()
    TWITTER_USERNAME = Config.TWITTER_USERNAME
    TWITTER_PASSWORD = Config.TWITTER_PASSWORD
    TWITTER_EMAIL = Config.TWITTER_EMAIL

    try:
        if scrapper.login(TWITTER_USERNAME, TWITTER_PASSWORD, TWITTER_EMAIL):
            trends = scrapper.fetch_trends()
            ip_address = scrapper.get_ip_address()
            timestamp = datetime.datetime.now()
            return (ip_address, trends,timestamp)

    finally:
        scrapper.close()


# login_and_fetch_x_trends()
