import requests
from bs4 import BeautifulSoup
import smtplib
import time


URL = "https://www.oyorooms.com/56085-spot-on-spot-on-37467-shivram-hotel" \
      "-jabalpur/?checkin=19%2F06%2F2020&checkout=20%2F06%2F2020&rooms=1" \
      "&guests=1&rooms_config=1-1_0&selected_rcid=272950"

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) ' \
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 ' \
                         'Safari/537.36'}

# Gives infor about the browser, Get by seraching "my user agent" on your browser

def check_price():
    page = requests.get(URL, headers = headers)

    soup = BeautifulSoup(page.text, 'html.parser')


                    #print(soup.prettify())

    hotel_name = soup.find('h1', class_ = "c-1wj1luj").get_text()

    print(hotel_name)

    price_string = soup.find('div', class_ =  "c-gnxvp8").get_text()

    price = float(price_string[1:])

    print(price)

    body = " Price of " + hotel_name + " is now  " + price_string + " . "
    print(body)


    if price >= 500:
        send_mail(hotel_name, price_string, URL)


def send_mail(hotel_name, price_string, URL):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    # Enter your email and password here, for security reasons placeholders
    # have been left in its place.
    # A good secure practise would be to use an app specific passwords

    server.login('email', 'password')



    subject = " Price of " + hotel_name + " is down !!"
    subject = subject.encode('ascii', 'ignore').decode('ascii')

    body = " Price of " + hotel_name + " is now  " + price_string + " . \n " \
            "You can book it at: " + URL


    body = body.encode('ascii', 'ignore').decode('ascii')



    msg = f"Subject: {subject}\n\n{body}"


    # Enter list of recipeints here

    server.sendmail(from_addr= 'Shivam Roy',
                    to_addrs= [], msg = msg)

    print('Mail sent.')
    server.quit()

while(True):
    check_price()
    time.sleep(60 * 60 * 10)

# The default time loop is 10 hours

