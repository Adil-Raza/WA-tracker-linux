import os
from time import strftime, sleep
from notify_run import Notify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from pytz import timezone

# multiple status, containing key value=> key used to refer in code, value will be the value which will be saved in DB/logs
statusMap = {
    'ONLINE': 'online',
    'OFFLINE': 'offline'
}

#getting indian timezone
indian_timezone = timezone('Asia/Kolkata')

# getting notify for notification
notify = Notify()

# target_name that needs to be tracked
target_name = "Nazma"  

def getCurrentTime():
    return datetime.now(indian_timezone).strftime("%Y-%m-%d %I:%M:%S %p")  

def sendNotification(message):
    print(message)
    notify.send(message)

def handleStatusChange(status, time_stamp, target_name):
    message = '{} is {} : {}'.format(target_name, status, str(time_stamp[11:]))
    sendNotification(message)

def main(target_name):
    driver = webdriver.Chrome(executable_path="./chromedriver")
    driver.get("http://web.whatsapp.com")

    # check if user has logged to web.whatsapp
    while True:
        try:
            chat = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[2]/div")
            break
        except:
            print('Please log in to web.whatsapp')
            sleep(2)

    # proceding as user logged in
    while(True):
        try:
            print('userLogged in')
            print('finding chat element')
            # finding chat element
            chat = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[3]/div/header/div[2]/div/span/div[2]/div")
            chat.click()
            # print("Connected to Whatsapp Server")
            sleep(2)

            
            # finding search bar 
            print('finding search bar')
            search = driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[1]/div/label/div/div[2]')
            search.click()
            sleep(2)
            

            # searching for the target_name
            print('typing name in searchbar')
            search.send_keys(target_name)
            sleep(1)

            # opening the searched chat
            print('opening searched chat')
            open = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div[1]/div/div/div[2]/div/div")
            open.click()
            sleep(2)

            print('chat opened')
            print("Now tracking is live")

            t = getCurrentTime()

            sent_online_notification = False
            sent_offline_notification = False

            while True:
                try:
                    status = driver.find_element_by_class_name("_3-cMa").text
                    t = getCurrentTime()
                    # print("{1} :  {2} is {0}".format(status, t[11:],target_name))
                    
                    if status.startswith('typing'):
                        sleep(0.5)
                        continue

                    if status == "online" and (not sent_online_notification):
                        message = '{} is online. '.format(target_name) + str(t[11:])
                        handleStatusChange(statusMap['ONLINE'], t, target_name)
                        sent_online_notification = True
                        sent_offline_notification = False

                    if status != "online" and (not sent_offline_notification):
                        message = '{} is Offline. '.format(target_name) + str(t[11:])
                        handleStatusChange(statusMap['OFFLINE'], t, target_name)
                        sent_online_notification = False
                        sent_offline_notification = True
                    
                    sleep(0.5)
                except:
                    t = getCurrentTime()

                    if(not sent_offline_notification):
                        message = '{} is Offline. '.format(target_name) + str(t[11:])
                        handleStatusChange(statusMap['OFFLINE'], t, target_name)
                        sent_offline_notification = True
                        sent_online_notification = False
                    
                    sleep(0.5)
        except Exception as e:
            print("Main exception:", e)
            sendNotification('Exception')
            sleep(2)

            
    driver.close()

if __name__ == "__main__":
    main(target_name)
