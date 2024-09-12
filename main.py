import threading
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from login_interaction import LoginInteraction 

# def simulate_user(user_id):
#     driver = webdriver.Chrome(service=Service())
#     login_interaction = LoginInteraction(driver)

#     username = "superadmin"
#     password = "n123"

#     login_interaction.login(username, password)
#     time.sleep(2)
#     login_interaction.closeModal(username)
#     login_interaction.openProspect(username)
#     login_interaction.createProspect(f"User{user_id}")

#     driver.quit()
#     print(f"Finished session and closed browser for user {user_id}.")
def simulate_user(user_id):
    logging.getLogger("selenium").setLevel(logging.WARNING)
    service_obj = Service()

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--window-size=1200x800")  # Set a window size

    driver = webdriver.Chrome(service=service_obj, options=chrome_options)

    login_interaction = LoginInteraction(driver)

    username = "superadmin"
    password = "n123"  

    login_interaction.login(username, password)

    time.sleep(2)
    login_interaction.closeModal(username)

    login_interaction.openProspect(username)

    login_interaction.createProspect(username)

    driver.quit()
    print(f"Finished session and closed browser for User {user_id}.")
    
    
def simulate_concurrent_users(num_users): 
    threads = []
    for user_id in range(1, num_users + 1):
        thread = threading.Thread(target=simulate_user, args=(user_id,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        



# Main execution
if __name__ == "__main__":
    num_users = 30
    simulate_concurrent_users(num_users)
