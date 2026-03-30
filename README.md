# TCGPlayer Collection to Google Sheets Scraper

This Python-based tool automates the process of scraping your TCGPlayer collection data and syncing it directly to a Google Sheet. It parses the HTML table from a public collection URL, preserves hyperlinks, and formats the spreadsheet for better readability.

---

## 🚀 Features

- **Automated Scraping:** Uses `BeautifulSoup` to target specific table selectors on TCGPlayer.
- **Hyperlink Preservation:** Automatically converts card links into clickable `=HYPERLINK` formulas.
- **Custom Formatting:** Utilizes `gspread-formatting` to automatically adjust column widths for a cleaner UI.
- **Secure Configuration:** Manages sensitive URLs and API keys using a `.env` file.

## 🛠️ Prerequisites

Before running the script, ensure you have:

1.  **Python 3.x** installed.
2.  A **Google Cloud Project** with the Google Sheets API enabled.
3.  A **Service Account Key** (JSON file) downloaded from the Google Cloud Console.
4.  A **Public TCGPlayer Collection URL** (Account Icon -> Your Collection -> Settings).

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/tcgplayer-to-sheets.git](https://github.com/your-username/tcgplayer-to-sheets.git)
   cd tcgplayer-to-sheets
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your credentials:
   ```
   collection_url='YOUR_PUBLIC_TCGPLAYER_URL'
   path_to_service_account_key='path/to/your/service-account.json'
   google_sheet_id='YOUR_GOOGLE_SHEET_ID_FROM_URL'
   ```

## 📋 Usage

1. **Share the Sheet:** Open your Google Sheet and share it with the `client_email` found in your Service Account JSON file (give it **Editor** permissions).

2. **Run the Script:**
   ```bash
   python main.py
   ```
3. The script will clear the existing sheet, scrape the latest data, and insert the updated rows with functional hyperlinks.

## 🧪 Technical Overview

- **Scraping Logic:** The script targets the `#collectionContainer table` selector to extract HTML table element holding the relevant data.
- **Data Transformation:** It iterates through `<td>` elements, specifically targeting the 'name' column to extract `<a>` tags and build Google Sheets formulas to preserve the same hyperlink format.
- **API Interaction:** Uses `value_input_option='USER_ENTERED'` to ensure Google Sheets parses the hyperlink strings as functional formulas rather than plain text.

## 🙏 Credits & Resources

[LearnDataSci: Ultimate Guide to Web Scraping](https://www.learndatasci.com/tutorials/ultimate-guide-web-scraping-w-python-requests-and-beautifulsoup/)

[Web Scraping with Python - Video Guide](https://www.youtube.com/watch?v=bEEzKvkj0nI)

[Python.org: Scraping to Google Sheets Discussion](https://discuss.python.org/t/webscraping-and-copying-data-into-google-sheets/62021)

[gspread API Documentation](https://docs.gspread.org/en/v3.7.0/api.html)
