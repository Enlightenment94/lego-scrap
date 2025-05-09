import os
import requests
from bs4 import BeautifulSoup


def scrap_lego_products(page_num=1, max=1, folder_name="city"):
    base_url = "https://www.lego.com/pl-pl/themes/" + folder_name + "?page="
    products = []

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    while True:
        url = f"{base_url}{page_num}&offset=0"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        items = soup.find_all("a", class_="ProductLeaf_title__1UhfJ")

        for item in items:
            title = item.find("span", class_="markup").text.strip()
            link = "https://www.lego.com" + item["href"]
            price_tag = item.find_next("span", class_="ds-label-md-bold", attrs={"data-test": "product-leaf-price"})
            price = price_tag.text.strip() if price_tag else "Brak ceny"
            products.append((title, price, link))

        filename = os.path.join(folder_name, f"page_{page_num}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            for title, price, link in products:
                f.write(f"{title} | {price} | {link}\n")

        page_num += 1
        if page_num >= max:
            break

    return products

lego_data = scrap_lego_products( max = 7, folder_name = "city")

for title, price, link in lego_data:
    print(f"{title} | {price} | {link}")
