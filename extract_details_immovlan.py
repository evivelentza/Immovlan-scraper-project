import requests
import csv
from bs4 import BeautifulSoup
from fake_headers import Headers
import time
import os


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}


def extract_property_data(url):
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, "lxml")

        data = {
            "url": url,
            "type": None,
            "price": None,
            "currency": "EUR",
            "surface": None,
            "rooms": None,
            "bathrooms": None,
            "yearBuilt": None,
            "city": None,
            "postalCode": None,
            "description": None,
            "terrace": None,
            "terrace_area": None,
            "garden": None,
            "garden_area": None,
            "equipped_kitchen": None,
            "furnished": None,
            "swimming_pool": None,
            "kitchen_surface": None,
        }

        # Info
        info_rows = soup.select('div.data-row-wrapper')
        for wrapper in info_rows:
            h4 = wrapper.find('h4')
            p = wrapper.find('p')
            if h4 and p:
                key = h4.text.strip().lower()
                val = p.text.strip().lower()

                if "bedroom" in key:
                    data["rooms"] = val
                elif "bathroom" in key:
                    data["bathrooms"] = val
                elif "livable surface" in key and "living" not in key:
                    data["surface"] = val.replace("m²", "").strip()
                elif "surface of living-room" in key:
                    data["living_room_surface"] = val.replace("m²", "").strip()
                elif "build year" in key:
                    data["yearBuilt"] = val
                elif "furnished" in key:
                    data["furnished"] = 1 if val == "yes" else 0
                elif "terrace" in key and "area" not in key:
                    data["terrace"] = 1 if val == "yes" else 0
                elif "garden" in key and "area" not in key:
                    data["garden"] = 1 if val == "yes" else 0
                elif "kitchen" in key:
                    data["equipped_kitchen"] = 1 if "equipped" in val else 0
                elif "swimming pool" in key:
                    data["swimming_pool"] = 1 if val == "yes" else 0
                elif "surface kitchen" in key:
                    data["kitchen_surface"] = val.replace("m²", "").strip()
                elif "terrace area" in key:
                    data["terrace_area"] = val.replace("m²", "").strip()
                elif "garden area" in key:
                    data["garden_area"] = val.replace("m²", "").strip()

        # Description
        description = soup.select_one("div.dynamic-description.active")
        if description:
            data["description"] = description.get_text(" ", strip=True)


        #Type from URL
        try:
            data["type"] = url.split("/")[5] 
        except IndexError:
            data["type"] = None

        # Price
        price_tag = soup.select_one('span.detail__header_price_data')
        if price_tag:
            data["price"] = price_tag.get_text(strip=True).replace("€", "").replace(" ", "").replace(".", "")
        else:
            li_tags = soup.select("div.financial.w-100 li")
            for li in li_tags:
                    if "price" in li.get_text().lower():
                        raw_price = li.get_text().split(":")[-1].strip()
                        data["price"] = raw_price.replace("€", "").replace(" ", "").replace(".", "")
                        break
       
        #Surface
        if not data.get("surface"):
            highlights = soup.select("li.property-highlight.margin-bottom-05.margin-right-05")
            for li in highlights:
                if "m²" in li.get_text():
                    data["surface"] = ''.join([c for c in li.get_text() if c.isdigit()])
                    break


        # Fallback for city and postal code from URL
        if not data.get("city") or not data.get("postalCode"):
            try:
                parts = url.split("/")
                data["postalCode"] = parts[7]
                data["city"] = parts[8]
            except:
                pass

        print(f"[DEBUG] Extracted: {data}")
        return data

    except Exception as e:
        print(f"[ERROR] Failed to scrape {url}: {e}")
        return None

#exporting to csv file
def save_row_to_csv(property_data, filename="immovlan_extracted.csv"):
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=property_data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(property_data)

def main():
    try:
        with open("property_links.csv") as f:
            urls = [line.strip() for line in f if line.strip()]
            
    except FileNotFoundError:
        print("[ERROR] property_links.csv not found.")
        return

    all_data = []

    for i, url in enumerate(urls):
        print(f"Scraping {i+1}/{len(urls)}: {url}")
        result = extract_property_data(url)
        if result:
            save_row_to_csv(result) 
        else:
            print(f"No data found for: {url}")
        time.sleep(1.5)


if __name__ == "__main__":
    main()


# #Yes No binary
# def yes_no_to_binary(value):
#     if value is None:
#         return None
#     value = value.strip().lower()
#     if value == "yes":
#         return 1
#     elif value == "no":
#         return 0
#     return None 