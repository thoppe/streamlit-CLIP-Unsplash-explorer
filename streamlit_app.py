import streamlit as st
import pandas as pd
import requests
import sys
import random
import start_api

app_formal_name = "Unsplash+CLIP image similarity"

# Start the app in wide-mode
st.set_page_config(
    layout="wide", page_title=app_formal_name,
)


# Starting random state
random_state = 78

# Number of results to return
top_k = 12


title_element = st.empty()
info_element = st.empty()

if st.button("💥 Randomize image"):
    m = sys.maxsize
    random_state = random.randint(0, 2 ** 32 - 1)


names = pd.read_csv("data/img_keys.csv")
random_sample = names.sample(n=1, random_state=random_state)["unsplashID"]

vector_idx = int(random_sample.index.values[0])
target_unsplash_id = random_sample.values[0]

url = f"https://unsplash.com/photos/{target_unsplash_id}"
title = f"CLIP+Unsplash image similarity [{target_unsplash_id}]({url})"
title_element.title(title)

url = "http://localhost:8000/top_match"
r = requests.get(url, params={"i": vector_idx, "top_k": top_k})
matching_ids = r.json()

# Try this!
# CSS Masonry
# https://w3bits.com/labs/css-masonry/

unsplash_links = [target_unsplash_id,] + matching_ids

divs = [
    f"""
    <div class="brick">
    <a href="https://unsplash.com/photos/{idx}">
    <img src="https://source.unsplash.com/{idx}">
    </a>
    </div>
    """
    for idx in unsplash_links
]
divs = "\n".join(divs)

with open("css/labs.css") as FIN:
    css0 = FIN.read()

with open("css/masonry.css") as FIN:
    css1 = FIN.read()


html = """
<html>
  <base target="_blank" />
  <head>
    <style> %s </style>
    <style> %s </style>
  </head>
  <body>
  <div class="masonry">
  %s
  </div>
  </body>
</html>
""" % (
    css0,
    css1,
    divs,
)

st.components.v1.html(html, height=1200, scrolling=True)
