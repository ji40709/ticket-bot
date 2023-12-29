from itertools import count
from tabnanny import check
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = ''
confirm_button_pressed = False
def run_webdriver(): # Main Selenium runner
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)  # Keep browser alive
    options.add_argument('--start-maximized') # Full window
    driver=webdriver.Chrome(options=options)
    driver.get('https://ticketplus.com.tw/order/27239b49272e4517a238cd3d3ffc0d72/523e9f9418f9b03352b847193a82fca9')
    #print("Before", confirm_button_pressed)
    #login_notice_enter()
    #print("After", confirm_button_pressed)
    #time.sleep(0.5)
    #if confirm_button_pressed:
    login()
    #else:
    #    print("Failed")
    #select_ticket()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    press_plus_button()


def login_notice_enter(): # Press confirm button
    global confirm_button_pressed
    confirm_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[4]/div/div/div[3]/div[2]/div[2]/button"))
    )
    confirm_button.click()
    confirm_button_pressed = WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located((By.XPATH, "/html/body/div/div[4]/div/div/div[3]/div[2]/div[2]/button"))
    )
    print("Click Login-notice button successfully.")

def login(): # Auto-input account & password, then login.
        print("Now")
        account = 'account' # Input ticket-plus account
        password = 'password' # Input ticket-plus password
        phone = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "MazPhoneNumberInput-20_phone_number"))
        )        
        phone.send_keys(account)
        pwd = driver.find_element(By.XPATH, "/html/body/div/div[3]/div/div[1]/div/div[2]/div[1]/form/div[3]/div/div[1]/div[1]/input")
        pwd.send_keys(password)
        login_button = driver.find_element(By.XPATH, "/html/body/div/div[3]/div/div[1]/div/div[2]/div[1]/form/button")
        login_button.click()
        print("Login successfully.")

def select_ticket(): # Press ticket panel with designated class(first, second, ...); Replace the XPATH with the area you want to buy.
    first_class = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[1]/div/div/main/div/div/div[2]/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/button"))
    )           
    first_class.click()
    if check_amount_clickable():
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4)") # If button is not displayed in the screen, selenium can't perform any action and throw error.
        print('Add 2')
    else:
        print('Keep')

def check_amount_clickable(): # Check whether the amount of ticket button is clickable which means buyable.
    amount_selector = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/main/div/div/div[2]/div[3]/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div[2]/span/div[1]")              
    amount_clickable = False
    if '2023' in amount_selector.text:
        print('Text: ', amount_selector.text)
        print('Ticket is buyable now.')
        amount_clickable = True
    else:
        print('Ticket is not buyable now.')
    return amount_clickable

def press_plus_button(): # Press button to add the amount of tickets you want to buy.
    ticket_to_buy = 2
    plus_button_invisible = WebDriverWait(driver, 5).until(
        EC.invisibility_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div/main/div/div/div[2]/div[3]/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/input"))
    )
    if plus_button_invisible:
        time.sleep(0.5) ## Need enhancement, sleep is not good
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        plus_button_selector = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "v-btn.v-btn--fab.v-btn--has-bg.v-btn--round.theme--light.v-size--x-small.light-primary-2"))
        )
        for i in range(0,ticket_to_buy):
            if plus_button_selector:
                plus_button_selector.click()
                print("Ticket + 1.")
            else:
                print("No ticket to buy.")
    else:
        print("Not show")
    
if __name__ == '__main__':
    before = datetime.datetime.now()
    run_webdriver()
    after = datetime.datetime.now()
    print("Elasped time: ", after - before)

