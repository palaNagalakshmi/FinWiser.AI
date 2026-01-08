import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "sec_filings.csv")
OUTPUT_DIR = os.path.join(DATA_DIR, "filings_text")

FORM_TYPES = ["10-K", "10-Q"]
MAX_COMPANIES = 3
MAX_FILINGS_PER_COMPANY = 2

HEADERS = {
    "User-Agent": "FINWISER.AI (academic project; contact: student@example.com)"
}
def extract_text_from_html(html_content: str) -> str:
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove scripts and styles
    for tag in soup(["script", "style"]):
        tag.decompose()

    text = soup.get_text(separator=" ")
    text = " ".join(text.split())  # normalize whitespace
    return text

def fetch_and_save_filings():
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV not found at {CSV_PATH}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(CSV_PATH)

    # Filter only 10-K / 10-Q
    df = df[df["Form Type"].isin(FORM_TYPES)]

    # Select limited companies
    selected_companies = df["Ticker"].dropna().unique()[:MAX_COMPANIES]
    df = df[df["Ticker"].isin(selected_companies)]

    print(f"Selected companies: {selected_companies}")

    for ticker in selected_companies:
        company_df = df[df["Ticker"] == ticker].head(MAX_FILINGS_PER_COMPANY)

        for _, row in company_df.iterrows():
            filing_url = row["Filing URL"]
            form_type = row["Form Type"]
            filed_at = row.get("Filed At", "unknown")

            filename = f"{ticker}_{form_type}_{filed_at}.txt"
            filepath = os.path.join(OUTPUT_DIR, filename)

            if os.path.exists(filepath):
                continue

            print(f"Downloading {filing_url}")

            try:
                response = requests.get(filing_url, headers=HEADERS, timeout=30)
                response.raise_for_status()

                text = extract_text_from_html(response.text)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(text)

                time.sleep(1)  # polite delay

            except Exception as e:
                print(f"Failed to fetch {filing_url}: {e}")
if __name__ == "__main__":
    fetch_and_save_filings()
