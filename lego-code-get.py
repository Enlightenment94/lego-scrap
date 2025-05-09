import os
import requests
from bs4 import BeautifulSoup

def get_product_codes_from_file(file_name):
    product_codes = []

    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()

        for line in lines:
            # Usuwamy białe znaki i dzielimy dane po '|' (odcinamy link od innych danych)
            parts = line.strip().split(" | ")
            if len(parts) >= 3:
                link = parts[-1]  # Link znajduje się na końcu po ' | '
                if link.startswith("http://") or link.startswith("https://"):
                    product_codes.append(link)

    return product_codes

"""
def get_product_code_from_link(link):
    response = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        product_code_tag = soup.find("span", class_="Markup__StyledMarkup-sc-nc8x20-0 dbPAWk")

        if product_code_tag:
            product_code = product_code_tag.text.strip()
            
            # Sprawdzamy, czy kod produktu jest cyfrą
            if product_code.isdigit():
                print(f"Link: {link} | Kod produktu: {product_code}")
                return product_code
            else:
                print(f"Link: {link} | Kod produktu nie jest liczbą, przechodzimy do kolejnego.")
                return None
        else:
            print(f"Link: {link} | Kod produktu nie znaleziony")
            return None
    else:
        print(f"Nie udało się pobrać strony: {link}")
        return None
"""



def get_product_code_from_link(link):
    response = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        product_code_tag = soup.find("p", class_="visually-hidden")

        if product_code_tag:
            product_code_text = product_code_tag.text.strip()
            
            product_code = product_code_text.split()[-1]  
            
            if product_code.isdigit():
                print(f"Link: {link} | Kod produktu: {product_code}")
                return product_code
            else:
                print(f"Link: {link} | Kod produktu nie jest liczbą, przechodzimy do kolejnego.")
                return None
        else:
            print(f"Link: {link} | Kod produktu nie znaleziony")
            return None
    else:
        print(f"Nie udało się pobrać strony: {link}")
        return None




def main():
    folder_name = "city"
    files = os.listdir(folder_name)
    
    page_files = [f for f in files if f.startswith("page_") and f.endswith(".txt")]
    page_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]), reverse=True)

    if page_files:
        latest_file = page_files[0]
        file_path = os.path.join(folder_name, latest_file)
        print(f"Przetwarzanie pliku: {latest_file}")

        links = get_product_codes_from_file(file_path)
        for link in links:
            product_code = get_product_code_from_link(link)
            print(f"Link: {link} | Kod produktu: {product_code}")
    else:
        print("Brak plików z danymi o produktach.")

if __name__ == "__main__":
    main()
