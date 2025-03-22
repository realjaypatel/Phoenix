#temp code 1
# import requests
# response = requests.get('https://excel2api.vercel.app/api/1BSOoMb-j3ALwi56lgSW8x7q17iNGSbuq1gpi9vV_ZOQ')
# print('fetched data2 :',response)

# import requests

# # response = requests.get('https://api.example.com/data')
# # print(response.status_code)  # Print the status code of the response
# print(response.json())   

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def sanitize_filename(url):
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        filename = "index"
    if parsed_url.query:
        filename += "_" + parsed_url.query.replace("=", "_").replace("&", "_")
    return filename

def download_file(url, folder):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.join(folder, sanitize_filename(url))
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")
    else:
        print(f"Failed to download: {url}")

def download_assets(url, base_folder):
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Download CSS files
    css_folder = os.path.join(base_folder, 'css')
    if not os.path.exists(css_folder):
        os.makedirs(css_folder)
    for link in soup.find_all('link', rel='stylesheet'):
        css_url = urljoin(url, link['href'])
        download_file(css_url, css_folder)

    # Download JS files
    js_folder = os.path.join(base_folder, 'js')
    if not os.path.exists(js_folder):
        os.makedirs(js_folder)
    for script in soup.find_all('script', src=True):
        js_url = urljoin(url, script['src'])
        download_file(js_url, js_folder)

    # Download images
    # img_folder = os.path.join(base_folder, 'images')
    # if not os.path.exists(img_folder):
    #     os.makedirs(img_folder)
    # for img in soup.find_all('img', src=True):
    #     img_url = urljoin(url, img['src'])
    #     download_file(img_url, img_folder)

    # # Download other assets (e.g., videos, fonts)
    # other_assets_folder = os.path.join(base_folder, 'other_assets')
    # if not os.path.exists(other_assets_folder):
    #     os.makedirs(other_assets_folder)
    # for tag in soup.find_all(['video', 'source', 'link', 'audio']):
    #     if 'src' in tag.attrs:
    #         asset_url = urljoin(url, tag['src'])
    #         download_file(asset_url, other_assets_folder)
    #     elif 'href' in tag.attrs:
    #         asset_url = urljoin(url, tag['href'])
    #         download_file(asset_url, other_assets_folder)

if __name__ == "__main__":
    website_url = "https://prium.github.io/phoenix/v1.21.0/"  # Replace with the target website URL
    download_folder = "downloaded_assets"
    download_assets(website_url, download_folder)