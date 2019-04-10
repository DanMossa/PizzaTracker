# python 2#

from selenium import webdriver
import smtplib
from termcolor import colored
import time

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("EMAILADDRESS", "PASSWORD")

emailMessage = """From: EMAILADDRESS
To: EMAILADDRESS
MIME-Version: 1.0
Content-type: text/html
Subject: Someone's eating pizza!!

"""


chromeBrowser = webdriver.PhantomJS(service_args=["--webdriver-loglevel=ERROR"])

print "Running...\n"
# phoneNumbers to try
phoneNumbers = []
# phoneNumbers already sent in 24 hours
orderNumbers = []
while True:
    i = 0
    for n in phoneNumbers:
        try:
            chromeBrowser.get('http://www.dominos.com/en/pages/tracker/#/track/order/')
            phoneNumbersInput = chromeBrowser.find_element_by_id("Phone")
            phoneNumbersInput.send_keys(phoneNumbers[i])

            submitButton = chromeBrowser.find_element_by_class_name("js-formSubmit")
            submitButton.click()
            # If Pizza is Found
            chromeBrowser.find_element_by_id("shoutoutSend")
            print colored(phoneNumbers[n] + " did order pizza.", "green")
            orderNumbers.append(phoneNumbers[i])
            try:
				server.sendmail("EMAILADDRESS", "dEMAILADDRESS", emailMessage + phoneNumbers[0])
				print "Successfully sent email"
            except Exception as e:
				print str(e)
        except Exception as e:
            print colored(phoneNumbers[i] + " did not order pizza.\n", "red")
            if "Unable to find element with id" not in str(e):
                print str(e)
        finally:
            i += 1
            time.sleep(10)
    print "Finished"
    chromeBrowser.quit()
    time.sleep(10800)

server.quit()