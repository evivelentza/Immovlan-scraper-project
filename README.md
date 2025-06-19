# **Immovlan Property Scraper**
This project is a HTML-based web scraper for immovlan.be, designed to extract property listing details across Belgium.

## 🚀 **Project Goal**
The goal is to **scrape and structure real estate data** from Immovlan for:

- Market analysis  
- Visualization and exploration  
- Real estate research  
- Dataset building for future tools or products

Currently, the scraper extracts the following:

-Property type

-Price and currency

-Surface area

-Number of rooms

-Bathrooms (if available)

-Equipped kitchen

-City and postal code

🛠️ **Technologies Used**
```bash
Python 3.10+
requests
BeautifulSoup (bs4)
csv
time, os, re (standard libs)
   ```

**How It Works**

The script reads property URLs from property_links.csv.
It fetches and parses each page using BeautifulSoup.
Relevant property data is extracted via HTML parsing.
The results are saved into immovlan_extracted.csv.

1. **Clone the repository**
   ```bash
   git clone https://github.com/evivelentza/Immovlan-scraper-project.git
   cd immovlan-scraper project
   ```

2. **(Optional) Create and activate a virtual environment**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install requests beautifulsoup4
   ```

4. **Add your list of property URLs**
   ```bash
   - Place them (one per line) in a file named `property_links.csv`
    ```
    
5. **Run the scraper**
   ```bash
   python extract_details_immovlan.py
   ```

6. **Output**
   - All extracted data is saved into:
     ```text
     immovlan_data_extracted.csv
     ```

---

### 🧠 Files

| Filename                     | Purpose                                          |
|-----------------------------|--------------------------------------------------|
| `property_links.csv`         | Input: list of property URLs                     |
| `extract_details_immovlan.py`| Main scraping logic                              |
| `immovlan_data_extracted.csv`| Output: final scraped dataset                    |
| `requirements.txt`           | Required Python packages (`pip install -r`)     |
| `url-collection-immovlan.py` | Optional: script to collect URLs from Immovlan  |

---



**Notes**
-The scraper is designed for educational and research purposes.
-Be mindful of Immovlan’s terms of service.
-Includes time.sleep() to avoid overloading the server (politeness delay).
