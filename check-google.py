import requests
from bs4 import BeautifulSoup
import re

def search_google_and_filter_by_price(query, price_threshold):
    google_url = f"https://www.google.com/search?q={query}"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    response = requests.get(google_url, headers=headers)
    
    if response.status_code != 200:
        print("Błąd przy wysyłaniu zapytania do Google")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    links = []
    for a_tag in soup.find_all("a", href=True):
        link = a_tag["href"]
        
        if "product" in link or "store" in link: 
            links.append(link)
    
    filtered_links = []
    for link in links:
        product_price = get_product_price(link)
        if product_price and product_price <= price_threshold / 2:
            filtered_links.append(link)
    
    return filtered_links

def get_product_price(link):
    try:
        response = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
    except Exception as e:
        print(f"Błąd przy pobieraniu strony {link}: {e}")
        return None
    
    if response.status_code != 200:
        print(f"Błąd przy pobieraniu strony: {link}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    price_tag = soup.find("span", class_="price") 
    if not price_tag:
        print(f"Nie znaleziono ceny dla: {link}")
        return None
    
    price_text = price_tag.get_text(strip=True)
    
    price_text = re.sub(r'[^\d,]', '', price_text)  
    price_text = price_text.replace(",", ".") 
    
    try:
        price = float(price_text)
        return price
    except ValueError:
        print(f"Nie udało się przekonwertować ceny: {price_text}")
        return None

query = "Lego 60441"
price_threshold = 10
links = search_google_and_filter_by_price(query, price_threshold)

if links:
    for link in links:
        print(link)
else:
    print("Brak wyników spełniających warunki.")
