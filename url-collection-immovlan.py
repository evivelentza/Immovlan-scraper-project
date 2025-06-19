from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests



root_url = "https://immovlan.be/en/real-estate?transactiontypes=for-sale,in-public-sale&propertytypes=house,apartment&propertysubtypes=residence,villa,mixed-building,master-house,bungalow,cottage,chalet,mansion,apartment,ground-floor,penthouse,studio,duplex,loft,triplex&noindex=1"


response = requests.get(root_url)
print("ok")

options = Options()
#options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def wait_for_property_links(driver, timeout=20):
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/detail/']")))

        
    except Exception as e:
        print(" Timeout waiting for property results:", e)

def extract_links(driver):
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    links = []
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        if "/detail/" in href:
            full_url = "https://www.immovlan.be" + href if href.startswith("/") else href
            links.append(full_url)
    return list(set(links))

   

def extract_all_links(base_url, driver, pages=51):
    all_links = []
    for page_number in range(1, pages + 1):
        page_url = f"{base_url}&page={page_number}"
        print(f" Visiting: {page_url}")
        driver.get(page_url)
        wait_for_property_links(driver)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2.5)
        with open(f"debug_page_{page_number}.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        links = extract_links(driver)
        print(f" Found {len(links)} links")
        all_links.extend(links)

    return all_links

try:

    collected_links = extract_all_links(root_url, driver, pages=51)
    print(f"Total collected: {len(collected_links)} links")
    with open("property_links.csv", "w") as f:
        for link in collected_links:
            f.write(link + "\n")
finally:
    driver.quit()
