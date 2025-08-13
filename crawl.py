from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys

showLoginXPath = "/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/section[2]/div/ion-grid/ion-row[1]/ion-col[2]/ion-button"
APKeyInputXPath = "/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/section[2]/div/ion-grid/ion-row[2]/ion-col[1]/form/div/div/div[1]/ion-input/input"
passwordInputXPath = "/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/section[2]/div/ion-grid/ion-row[2]/ion-col[1]/form/div/div/div[2]/div/ion-input/input"
loginBtnXPath = "/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/section[2]/div/ion-grid/ion-row[2]/ion-col[1]/form/div/div/div[3]/ion-button"
signAttendanceXPath = "/html/body/app-root/ion-app/ion-router-outlet/app-tabs/ion-content/ion-tabs/div/ion-router-outlet/app-dashboard/ion-content/div/ion-row/ion-col/ion-card[1]/ion-card-content/ion-row/ion-col[1]"
otpNum1XPath = "/html/body/app-root/ion-app/ion-router-outlet/app-student/ion-content/ion-row/ion-col/div/input[1]"
otpNum2XPath = "/html/body/app-root/ion-app/ion-router-outlet/app-student/ion-content/ion-row/ion-col/div/input[2]"
otpNum3XPath = "/html/body/app-root/ion-app/ion-router-outlet/app-student/ion-content/ion-row/ion-col/div/input[3]"



class interact:
    def  __init__(self, XPath):
        self.xpath = XPath

    def get_xpath(self):
        return self.xpath

    def find(self, id)->bool:
        indicator1 = driver.find_elements(By.XPATH, self.xpath)
        indicator2 = driver.find_elements(By.ID, id)
        if (len(indicator1) >= 1 | len(indicator2) >= 1):
            return True
        
        return False

class button(interact):
    def __init__(self, XPath, time:int=10):
        super().__init__(XPath)
        self.xpath = XPath
        self.time = time
        self.drive = self.prep()

    def prep(self):
        return WebDriverWait(driver, self.time).until(
            EC.element_to_be_clickable((By.XPATH, self.xpath))
            )

    def push(self):
        self.drive.click()

class fillin(interact):
    def __init__(self, XPath, time:int=5):
        super().__init__(XPath)
        self.xpath = XPath
        self.time = time
        self.drive = self.prep()

    def prep(self):
        return WebDriverWait(driver, self.time).until(
              EC.visibility_of_element_located((By.XPATH, self.xpath))
              )  

    def send(self, fillings):
        self.drive.send_keys(fillings)


def login_apspace(APkey:str, Password:str):
    button(showLoginXPath).push()
    fillin(APKeyInputXPath).send(APkey)
    fillin(passwordInputXPath).send(Password)
    button(loginBtnXPath).push()
    

def sign_attendace(otp:list[str]):
    button(signAttendanceXPath).push()
    fillin(otpNum1XPath).send(otp[0])
    fillin(otpNum2XPath).send(otp[1])
    fillin(otpNum3XPath).send(otp[2])
    fillin(otpNum3XPath).send(Keys.ENTER)


def main(attendance_code:str, apkey:str, password:str):
    global driver
    
    if (len(attendance_code) == 0):
        print("Missing Code!")
        return
    
    otp = list(attendance_code)
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://apspace.apu.edu.my/login")

    login_apspace(apkey, password)
    sign_attendace(otp)

    time.sleep(5)
    alert = "/html/body/app-root/ion-app/ion-alert/div[2]/div[1]"
    alert_id = "alert-1-msg"

    if (interact(alert).find(alert_id)):
        print(f"ALERT FAIL TO SIGN {apkey}")
        return
    else:
        print(f"{apkey} has signed.")
        
    driver.quit()
    
if __name__ == "__main__":
    if (len(sys.argv) < 2 ):
        print("Missing OTP!")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

#inspiration:
#https://github.com/yuenci/APU-automatic-take-attendance/blob/master/script/seleniumWD.py#L16


# <div id="alert-1-msg" class="alert-message sc-ion-alert-md">Failed to update attendance. Incorrect OTP</div>