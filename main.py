from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from login_interaction import LoginInteraction
import threading
import time

def simulate_user(user_id):
    driver = webdriver.Chrome(service=Service())
    login_interaction = LoginInteraction(driver)

    username = "superadmin"
    password = "n123"

    login_interaction.login(username, password)
    time.sleep(2)
    login_interaction.closeModal(username)
    login_interaction.openProspect(username)
    login_interaction.createProspect(f"User{user_id}")

    driver.quit()
    print(f"Finished session and closed browser for user {user_id}.")

def simulate_concurrent_users(num_users):
    global total_prospects_created  
    threads = []
    for user_id in range(1, num_users + 1):
        thread = threading.Thread(target=simulate_user, args=(user_id,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        
    print(f"Total number of prospects created by all users: {total_prospects_created}")


# Main execution
if __name__ == "__main__":
    num_users = 5 
    simulate_concurrent_users(num_users)
