import requests
from bs4 import BeautifulSoup
import smtplib
import time


headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) ' \
                         'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 ' \
                         'Safari/537.36'}

# Gives information about the browser, Get it by searching "my user agent" on
# your browser



# This dictionary is used to store the hotel URLs and the trigger prices

hotels_prices = {

    'https://www.oyorooms.com/96616-oyo-rooms-oyo-70088-gurugram-residency'
    '-gurgaon/?checkin=17%2F09%2F2020&checkout=18%2F09%2F2020&rooms=1&guests' \
    '=2&rooms_config=1-2_0&selected_rcid=1': 800,

    "https://www.oyorooms.com/56085-spot-on-spot-on-37467-shivram-hotel" \
    "-jabalpur/?checkin=19%2F07%2F2020&checkout=20%2F07%2F2020&rooms=1" \
    "&guests=1&rooms_config=1-1_0&selected_rcid=272950": 500,


}


def start_scraping(hotels_prices=hotels_prices):
    while (True):
        for hotel_URL, price in hotels_prices.items():
            check_price(hotel_URL, price)
        time.sleep(36000)  # The default time loop is 10 hours


def check_price(URL, floor_price):
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')


    hotel_name = soup.find('h1', class_="c-1wj1luj").get_text()


    print(hotel_name)

    try:
        price_string = soup.find('span', class_="listingPrice__finalPrice " \
                                            "listingPrice__finalPrice--black").get_text()
    except:
        print("Please check your URL for " + hotel_name + ". The price should "
                                                          "be visible in the "
                                                          "link.")

    price = float(price_string[1:])

    print(price)

    body = " Price of " + hotel_name + " is now  " + price_string + " . "
    print(body)

    if price <= floor_price:
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

    server.sendmail(from_addr='Shivam Roy',
                    to_addrs=[], msg=msg)

    print('Mail sent.')
    print(msg)
    server.quit()


start_scraping(hotels_prices)  # Calls the main start function


# Caution: the loop runs indefintely unless stopped manually, because this is
# how it was supposed to be