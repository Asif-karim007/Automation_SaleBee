import time
import re
import random
import sys
import select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException


class LoginInteraction:
    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
    
    def login(self, username, password):
        try:
            self.driver.get("https://qa.salebee.net/")
            self.driver.find_element(By.XPATH, "//*[@id='UserName']").send_keys(username)
            self.driver.find_element(By.XPATH, "//*[@id='Password']").send_keys(password)
            self.driver.find_element(By.XPATH, "//*[@id='myModal']/div/div/div[2]/form/div[3]/input").click()
            current_url = self.driver.current_url
            
            if current_url == "https://qa.salebee.net/Employee/MyProfile":
                print(f"User {username}: Login successful!")
            else:
                print(f"User {username}: Login failed.")
                
        except Exception as e:
            print(f"User {username}: Error occurred during login: {e}")
    
    def closeModal(self, username):
        try:
            modal = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='modal-header']"))
            )
            print("Modal is visible")

            close_button = modal.find_element(By.XPATH, "//*[@id='taskNotification']/div/div/div[1]/button/span/i")
            close_button.click()
            time.sleep(2)
            print("Closed the modal")

        except Exception as e:
            print(f"User {username}: Modal not found: {e}")
            
    def extract_number(self, text):
        match = re.search(r'\d+', text)
        if match:
            return int(match.group())
        return 0

    def openProspect(self, username):
        try:
            self.driver.find_element(By.XPATH, "//*[@id='sidebarmenu']/div[2]/div/ul/li[6]").click()
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='prospectGrid']"))
            )
            print(f"Prospect table has been loaded")
            
            try:
                current_prospect_element = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="prospectstagegroup"]/div[1]'))
                )
                current_prospect_text = current_prospect_element.text
                self.current_prospect_number = self.extract_number(current_prospect_text)
                print(f"Total prospect number: {self.current_prospect_number}")
                
            except Exception as e:
                print(f"Error occurred while extracting number: {e}")
                
        except Exception as e:
            print(f"Can not open prospect table: {e}")
            
    def retry_click(element, retries=3, delay=2):
        for _ in range(retries):
            try:
                element.click()
                return
            except ElementClickInterceptedException:
                time.sleep(delay)
        print("Failed to click element after retries.")

            

    def createProspect(self, username):    
        counter = 0
        print("Press Enter to stop the process...\n")
        while True: 
            if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                input()
                print(f"User {username}: Stopping the process...")
                break
            
            random_suffix = random.randint(10000, 99999)
            prospect_name = f"Automated Testing #{random_suffix}"
                
            try:
                # Wait until modal is not visible
                WebDriverWait(self.driver, 10).until(
                    EC.invisibility_of_element_located((By.XPATH, "//*[@id='myModal']"))
                )
                
                add_prospect_button = self.driver.find_element(By.XPATH, "//*[@id='ChildContainer']/div[1]/div[1]/div[1]/div[1]")
                
                # Wait until the element is clickable
                WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='ChildContainer']/div[1]/div[1]/div[1]/div[1]"))
                )
                
                # Scroll to the element and attempt the click with retry logic
                actions = ActionChains(self.driver)
                actions.move_to_element(add_prospect_button).perform()
                retry_click(add_prospect_button)  # Use retry_click here
                time.sleep(2)
                self.driver.find_element(By.XPATH, "//*[@id='org-Name']").send_keys(prospect_name)
                self.driver.find_element(By.XPATH, "//*[@id='myModal']/div/div/div[3]/div[1]/button").click()
                time.sleep(2)
                
                WebDriverWait(self.driver, 20).until(
                    EC.invisibility_of_element_located((By.XPATH, "/html/body/div[31]/div[4]"))
                )

                # Refresh the prospect table
                refresh_button = WebDriverWait(self.driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='ChildContainer']/div[1]/div[1]/div[1]/div[2]/a/i"))
                )
                retry_click(refresh_button)  # Use retry_click here
                time.sleep(2)

                WebDriverWait(self.driver, 40).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='prospectGrid']"))
                )

                # Get the new prospect number
                try:
                    new_prospect_element = WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="prospectstagegroup"]/div[1]'))
                    )
                    new_prospect_text = new_prospect_element.text
                    new_prospect_number = self.extract_number(new_prospect_text)
                    print(f"Total prospect number after creating a new prospect: {new_prospect_number}")
                    counter += 1
                    print(f"Prospect {counter} created: {prospect_name}")
                except Exception as e:
                    print(f"Error occurred while counting new prospect total: {e}")
                
                time.sleep(2)

                # Compare prospect numbers
                if new_prospect_number > self.current_prospect_number:
                    print(f"User {username}: Successfully created a new prospect!")
                else:
                    print(f"User {username}: Failed to create a new prospect.")
                
            except ElementClickInterceptedException as e:
                print(f"Element click intercepted: {e}. Trying again after waiting...")
                time.sleep(2)  
                
            except Exception as e:
                print(f"Error occurred while creating new prospect: {e}")

        print(f"Total number of prospects created automatically: {counter}")
