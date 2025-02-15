import requests
import time
import socket
import pandas as pd
import os

urls = [
    "http://example.com",
    "http://quotes.toscrape.com",
    "http://httpbin.org/get"
]

def fetch_metadata(url):
    try:
        session = requests.Session()
        start_time = time.time()
        response = session.get(url, headers={"User-Agent": "Mozilla/5.0"})
        end_time = time.time()

        metadata = {
            "URL": response.url,
            "Status Code": response.status_code,
            "Response Time (s)": round(end_time - start_time, 4),
            "Content Length": len(response.content),
            "Depth": 1,  # Direct request
            "IP Address": socket.gethostbyname(url.split("//")[1].split("/")[0]),
            "Request Headers": str(response.request.headers),
            "Response Headers": str(response.headers),
            "User Agent": response.request.headers.get("User-Agent", "N/A"),
            "Redirected URLs": " → ".join([r.url for r in response.history]) if response.history else "None",
            "Encoding": response.encoding,
            "Cookies": str(response.cookies.get_dict())
        }

        return metadata

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Fetch data
data = [fetch_metadata(url) for url in urls if fetch_metadata(url) is not None]

# Convert to DataFrame
df = pd.DataFrame(data)

# Append to CSV if file exists, else create new one
csv_file = "scraper_metadata.csv"
if os.path.exists(csv_file):
    df.to_csv(csv_file, mode='a', header=False, index=False)  # Append without rewriting header
else:
    df.to_csv(csv_file, index=False)  # Create file with headers

print("Data appended to scraper_metadata.csv")
