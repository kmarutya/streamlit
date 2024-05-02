import re
import ssl
import streamlit as st
import pandas as pd
import numpy as np

from dataclasses import dataclass


def convert_google_sheet_url(url):
    # Regular expression to match and capture the necessary part of the URL
    pattern = r'https://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)(/edit#gid=(\d+)|/edit.*)?'

    # Replace function to construct the new URL for CSV export
    # If gid is present in the URL, it includes it in the export URL, otherwise, it's omitted
    replacement = lambda m: f'https://docs.google.com/spreadsheets/d/{m.group(1)}/export?' + (f'gid={m.group(3)}&' if m.group(3) else '') + 'format=csv'

    # Replace using regex
    new_url = re.sub(pattern, replacement, url)
    return new_url


def get_last_n_kuzigames(last_n: int = 10) -> pd.DataFrame:
    # Define the URL of the Google Sheets document
    url = 'https://docs.google.com/spreadsheets/d/1EXUs6D5yiRrVIuuZ4lYJzoLaxy3DcmAr0v_j9OQ7xyc/edit#gid=587406342'
    new_url = convert_google_sheet_url(url)

    # Disable SSL certificate verification
    ssl._create_default_https_context = ssl._create_unverified_context
    df = pd.read_csv(new_url, header=0)

    # Filter the DataFrame if more than two columns have the value "играли" (case-insensitive)
    df = df[df.apply(lambda row: row.str.lower().eq('играли').sum() <= 2, axis=1)]

    # Get tail and trim columns
    tail = df.tail(last_n).iloc[:, :8].fillna('')

    return tail

st.write("Кузинтара")

# Approximate coordinates (latitude, longitude)
cities = {
    "San Francisco": (37.7749, -122.4194),
    "San Diego": (32.7157, -117.1611),
    "Seattle": (47.6062, -122.3321),
    "New York City": (40.7128, -74.0060),
    "Boston": (42.3601, -71.0589)
}

# Create a NumPy array
coordinates_array = np.array(list(cities.values()))

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))


chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)

# plot map
map_data = pd.DataFrame(
    coordinates_array,
    columns=['lat', 'lon']
)

st.map(map_data)

# widgets
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# From the command line, run
#  streamlit run stremalit.py

df_games = get_last_n_kuzigames(10)
st.write(df_games)