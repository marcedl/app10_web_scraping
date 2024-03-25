import requests
import selectorlib
import smtplib
import os

data = r"C:\Users\leona\OneDrive\Escritorio\Python Mega Course Build 20 Apps\app10_web_scraping\data.txt"

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    #Scrape the page source from the URL
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    user_name = "marcedl88@gmail.com"
    password = os.getenv("PASSWORD")

    receiver = "marcedl88@gmail.com"

    message = f"""\
    Subject: New event was found!

    New event found: {extracted}
    """
    with smtplib.SMTP_SSL(host, port) as server:
        server.login(user_name, password)
        server.sendmail(user_name, receiver, message)
    print("Email was sent")


def store(extracted):
    with open(data, "a") as file:
        file.write(extracted + "\n")


def read(extracted):
    with open(data, "r") as file:
        return file.read()


if __name__ == "__main__":
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)
    content = read(extracted)
    if extracted != "No upcoming tours":
        if extracted not in content:
            store(extracted)
            send_email(message="New event was found!")