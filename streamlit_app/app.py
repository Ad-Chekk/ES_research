import streamlit as st
import pandas as pd
import os

# Paths to CSV files (Parallel to streamlit_app directory)
NET_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "net_data.csv")
SCRAPER_METADATA_PATH = os.path.join(os.path.dirname(__file__), "..", "scraper_metadata.csv")

# Load CSV files
@st.cache_data
def load_data():
    net_data = pd.read_csv(NET_DATA_PATH)
    scraper_metadata = pd.read_csv(SCRAPER_METADATA_PATH)
    return net_data, scraper_metadata

# Load data
net_data, scraper_metadata = load_data()

# Streamlit App UI
st.title("Web Scraping Metadata Visualization")

# Dataset selection
dataset_choice = st.radio("Select dataset:", ["Scrapy Metadata (net_data.csv)", "Requests Metadata (scraper_metadata.csv)"])

if dataset_choice == "Scrapy Metadata (net_data.csv)":
    st.subheader("Scrapy Metadata")
    st.dataframe(net_data)

    # Response Code Distribution
    if "Status Code" in net_data.columns:
        st.subheader("Response Code Distribution")
        st.bar_chart(net_data["Status Code"].value_counts())

    # Response Time Analysis
    if "Response Time (s)" in net_data.columns:
        st.subheader("Response Time Distribution")
        st.line_chart(net_data["Response Time (s)"])

elif dataset_choice == "Requests Metadata (scraper_metadata.csv)":
    st.subheader("Requests Metadata")
    st.dataframe(scraper_metadata)

    # Compare Response Times (if common column exists)
    if "Response Time (s)" in scraper_metadata.columns:
        st.subheader("Response Time Comparison")
        combined_data = pd.DataFrame({
            "Scrapy": net_data["Response Time (s)"] if "Response Time (s)" in net_data.columns else [],
            "Manual Requests": scraper_metadata["Response Time (s)"]
        })
        st.line_chart(combined_data)

# Filtering Option
st.subheader("Filter Data")
filter_url = st.text_input("Enter URL to filter:", "")
if filter_url:
    filtered_scrapy = net_data[net_data["URL"].str.contains(filter_url, na=False)]
    filtered_requests = scraper_metadata[scraper_metadata["URL"].str.contains(filter_url, na=False)]
    st.write("### Scrapy Data for URL:")
    st.dataframe(filtered_scrapy)
    st.write("### Requests Data for URL:")
    st.dataframe(filtered_requests)

st.write("### Summary Statistics")
st.write(net_data.describe())
st.write(scraper_metadata.describe())

st.success("Dashboard Loaded Successfully! 🎯")
