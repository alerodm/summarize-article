import os
import sys
import unicodedata

import requests


def get_cleaned_content(page_url):
    txtify_url = f"https://txtify.it/{page_url}"  # for real usage switch to txtify api
    headers = {
        "Accept": "text/plain",
        "User-Agent": "PostmanRuntime/7.28.4"
    }
    req = requests.get(txtify_url, headers=headers)
    req.raise_for_status()
    text = unicodedata.normalize("NFKD", req.text)
    text = text.translate(str.maketrans({"\n": " ", "\t": " "}))
    return text


def summarize_text(text):
    textapi_url = "https://app.thetextapi.com/text/summarize"
    headers = {
        "Content-Type": "application/json",
        "apikey": os.environ.get('TEXT_API_KEY')
    }

    body = {
        "text": text
    }

    response = requests.post(textapi_url, headers=headers, json=body)
    response.raise_for_status()
    return response.json().get('summary')


if __name__ == "__main__":
    page_url = sys.argv[1]
    text = get_cleaned_content(page_url)
    text_summary = summarize_text(text)
    print(text_summary)
