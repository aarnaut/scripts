import requests
import base64
import json 
import io

from tqdm import tqdm

def get_serial_id(part):
    url = f"https://linkvertise.net/api/v1/redirect/link/static/13243/sp2002p{part}md?origin=https://smokelinks.blogspot.com/p/sp20.html"
    data = requests.get(url = url).json()
    return data["data"]["link"]["id"]

def build_download_url(part, serialId): 
    serial = {'timestamp': 1580577074449, 'random': '375123', 'link_id': serialId}
    serialBase64Endcoded = str(base64.b64encode(json.dumps(serial).encode()), "utf-8")
    return f"https://linkvertise.net/api/v1/redirect/link/13243/sp2002p{part}md/target?serial={serialBase64Endcoded}"

def get_download_link(part):
    serialId = get_serial_id(part)
    url = build_download_url(part, serialId)
    data = requests.get(url = url).json()
    return data["data"]["target"]

urls = []
urls.append(get_download_link("1"))
urls.append(get_download_link("2"))
urls.append(get_download_link("3"))
urls.append(get_download_link("4"))

print(urls)