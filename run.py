import json
import os
import re
import shutil

from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup


class Truck(BaseModel):
    id: int = 0
    href: str = ""
    title: str = ""
    price: int = 0
    mileage: int = 0
    color: str = ""
    power: int = 0
    description: str = ""


def write_data_to_json(filepath: str, data: dict):
    with open(filepath, mode="w") as output_file:
        json.dump(data, output_file)


cookies = {
    "ASP.NET_SessionId": "jgiupxaek0ntxaty3i1ypojs",
    "TS24consentID": "108330281.1674653626",
    "mGUID": "c38283b0-5baf-48ef-9a2f-9a8e5ffc84f8",
    "__RequestVerificationToken": "V4tiQgHopqBQ39xKRpw4CwKczpmgrwuoEr_wcvqYjLsIjqICOmBL1mKqtnLCJUAQWScKGJ-MkysCjRR8GSAYuorxv_I1",
    "_clck": "1ukegrl|1|f8k|0",
    "_clsk": "itqz55|1674653629111|1|1|i.clarity.ms/collect",
    "TS24consent": "essential:true|functional:true|analytics:true|marketing:true",
    "contact": "%7B%22na%22%3A%22%22%2C%22em%22%3A%22%22%2C%22ph%22%3A%22%22%7D",
    "_ga": "GA1.2.108330281.1674653626",
    "_gid": "GA1.2.1524380773.1674653637",
    "_gat_gtag_UA_33302270_1": "1",
    "_fbp": "fb.1.1674653638151.1524039092",
    "cto_bundle": "9eUDMl9zRmd3aTJLWVlZMUJEJTJGc0J2MnUlMkJlOVRscDBQU1ZRb1JWdzd0UCUyQnhsbEUlMkZhdUdRS3RwOTF6d0YyTExDaGlCZTc3dVk0ZGFEZ0RZRE1LRzZ0UXNxRWczY3dROHdQZUZtOFkyRDFONUJLaXJ5NExJZE9lc3lvNlhrZzVqR3hlREkxRkVpTSUyQiUyRlNYVjJrSnQySEVPa1hyZW5TU1ROWjJOV09pN3VHOURsdnhJUzY5eG92Mm41T1NZWEt2d216UFdLRG0",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    # 'Accept-Encoding': 'gzip, deflate, br',
    "Connection": "keep-alive",
    # 'Cookie': 'ASP.NET_SessionId=jgiupxaek0ntxaty3i1ypojs; TS24consentID=108330281.1674653626; mGUID=c38283b0-5baf-48ef-9a2f-9a8e5ffc84f8; __RequestVerificationToken=V4tiQgHopqBQ39xKRpw4CwKczpmgrwuoEr_wcvqYjLsIjqICOmBL1mKqtnLCJUAQWScKGJ-MkysCjRR8GSAYuorxv_I1; _clck=1ukegrl|1|f8k|0; _clsk=itqz55|1674653629111|1|1|i.clarity.ms/collect; TS24consent=essential:true|functional:true|analytics:true|marketing:true; contact=%7B%22na%22%3A%22%22%2C%22em%22%3A%22%22%2C%22ph%22%3A%22%22%7D; _ga=GA1.2.108330281.1674653626; _gid=GA1.2.1524380773.1674653637; _gat_gtag_UA_33302270_1=1; _fbp=fb.1.1674653638151.1524039092; cto_bundle=9eUDMl9zRmd3aTJLWVlZMUJEJTJGc0J2MnUlMkJlOVRscDBQU1ZRb1JWdzd0UCUyQnhsbEUlMkZhdUdRS3RwOTF6d0YyTExDaGlCZTc3dVk0ZGFEZ0RZRE1LRzZ0UXNxRWczY3dROHdQZUZtOFkyRDFONUJLaXJ5NExJZE9lc3lvNlhrZzVqR3hlREkxRkVpTSUyQiUyRlNYVjJrSnQySEVPa1hyZW5TU1ROWjJOV09pN3VHOURsdnhJUzY5eG92Mm41T1NZWEt2d216UFdLRG0',
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}
params = {"currentpage": "1"}

url = (
    f"https://www.truckscout24.de/transporter/gebraucht/kuehl-iso-frischdienst/renault"
)


def get_num_pages(response) -> int:
    soup = BeautifulSoup(response, "html.parser")
    total_cars = soup.find("div", class_="listItem").attrs.get("data-cnt")
    num_pages = round(int(total_cars) / 20)
    return num_pages


def get_page_soup(response):
    return BeautifulSoup(response, "html.parser")


def get_response_text(url: str, params: dict, cookies: dict, headers: dict):
    response = requests.get(url, params=params, cookies=cookies, headers=headers).text
    return response


def get_href(car) -> str:
    return "https://www.truckscout24.de" + car.find("div", class_="ls-titles").find(
        "a"
    ).attrs.get("href")


def get_id(car) -> int:
    car_id = car.find(
        "button", class_="sc-btn-block sc-btn-bob notransition reqPhotos"
    ).attrs.get("data-vid")
    return car_id


def get_title(car_soup) -> str:
    return car_soup.find("div", class_="header").find("h1").text


def get_price(car_soup) -> int:
    try:
        price = int(
            car_soup.find("div", class_="d-price sc-font-xl")
            .find("h2")
            .text.split(" ")[1]
            .replace(".", "")
            .replace(",-", "")
        )
    except ValueError:
        price = 0
    return price


def get_mileage(car_soup) -> int:
    try:
        mileage = int(
            car_soup.findAll("div", class_="itemval")[1]
            .text.replace(".", "")
            .split(" ")[0]
        )
    except ValueError:
        mileage = 0
    return mileage


def get_color_power_data_list(car_soup) -> list:
    return car_soup.find("ul", class_="columns").findAll("li")


def get_color(color_data_list: list) -> str:
    color_value = ""
    for data_element in color_data_list:
        color_info = re.findall(r"Farbe<\/div>([\w\W]+?)<\/li>", str(data_element))
        if color_info:
            color_value = re.findall(r'<div class="">([\w\W]+?)<\/div>', color_info[0])[
                0
            ]
    return color_value


def get_power(power_data_list: list) -> str:
    power_value = 0
    for data_element in power_data_list:
        power_info = re.findall(r"Leistung<\/div>([\w\W]+?)<\/li>", str(data_element))
        if power_info:
            power_value = re.findall('<div class="">([\w\W]+?)<\/div>', power_info[0])[
                0
            ].split(" ")[0]
    return power_value


def get_description(car_soup) -> str:
    return car_soup.find("div", class_="short-description").text


def download_photos(car_soup, car_id):
    photo_urls = car_soup.findAll("div", class_="gallery-picture")
    os.mkdir(os.path.join(os.getcwd(), str(car_id)))
    for photo in photo_urls[:3]:
        photo_path = photo.find("img").attrs.get("data-src")
        res = requests.get(photo_path, stream=True)
        file_name = photo_path.split("/")[-1]
        truck_directory_path = os.path.join(os.getcwd(), str(car_id), file_name)
        if res.status_code == 200:
            with open(truck_directory_path, "wb") as f:
                shutil.copyfileobj(res.raw, f)
            print("Image sucessfully Downloaded: ", file_name)
        else:
            print("Image Couldn't be retrieved")


response = get_response_text(url, params, cookies, headers)
num_pages = get_num_pages(response)
cars = []
for i in range(1, num_pages + 1):
    params = {"currentpage": f"{i}"}
    response = requests.get(
        url,
        params=params,
        cookies=cookies,
        headers=headers,
    ).text
    soup = get_page_soup(response)
    car = soup.findAll("div", class_="ls-top-cntnr")[0]
    car_id = get_id(car)
    href = get_href(car)
    car_info_page = get_response_text(href, params, cookies, headers)
    car_soup = get_page_soup(car_info_page)
    power_color_data_list = get_color_power_data_list(car_soup)
    truck = Truck(
        id=car_id,
        href=href,
        title=get_title(car_soup),
        price=get_price(car_soup),
        mileage=get_mileage(car_soup),
        color=get_color(power_color_data_list),
        power=get_power(power_color_data_list),
        description=get_description(car_soup),
    )
    cars.append(truck.dict())
    download_photos(car_soup, car_id)

data = {"ads": cars}
try:
    os.mkdir(os.path.join(os.getcwd(), "data"))
except FileExistsError:
    pass

data_file_path = os.path.join(os.getcwd(), "data", "data.json")
write_data_to_json(data_file_path, data)
