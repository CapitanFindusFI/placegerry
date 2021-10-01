import requests
import re
import json
import time
import logging
import os.path
import mimetypes
from slugify import slugify

logging.basicConfig(level=logging.DEBUG);
logger = logging.getLogger(__name__)

def search(keywords, max_results=None):
    url = 'https://duckduckgo.com/';
    params = {
    	'q': keywords
    };

    logger.debug("Hitting DuckDuckGo for Token");

    #   First make a request to above URL, and parse out the 'vqd'
    #   This is a special token, which should be used in the subsequent request
    res = requests.post(url, data=params)
    searchObj = re.search(r'vqd=([\d-]+)\&', res.text, re.M|re.I);

    if not searchObj:
        logger.error("Token Parsing Failed !");
        return -1;

    logger.debug("Obtained Token");

    headers = {
        'authority': 'duckduckgo.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-fetch-dest': 'empty',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': 'https://duckduckgo.com/',
        'accept-language': 'en-US,en;q=0.9',
    }

    params = (
        ('l', 'us-en'),
        ('o', 'json'),
        ('q', keywords),
        ('vqd', searchObj.group(1)),
        ('f', ',,,'),
        ('p', '1'),
        ('v7exp', 'a'),
    )

    requestUrl = url + "i.js";

    logger.debug("Hitting Url : %s", requestUrl);

    while True:
        while True:
            try:
                res = requests.get(requestUrl, headers=headers, params=params);
                data = json.loads(res.text);
                break;
            except ValueError as e:
                logger.debug("Hitting Url Failure - Sleep and Retry: %s", requestUrl);
                time.sleep(5);
                continue;

        logger.debug("Hitting Url Success : %s", requestUrl);
        filtered_data=collect_results(data["results"])
        download_images(filtered_data)

        if "next" not in data:
            logger.debug("No Next Page - Exiting");
            exit(0);

        requestUrl = url + data["next"];

def collect_results(results):
    filtered_results=[]
    for result in results:
        obj={}
        obj["width"] = result["width"]
        obj["height"] = result["height"]
        obj["url"] = result["image"]
        obj["title"] = result["title"]
        filtered_results.append(obj)
    return filtered_results

def download_images(objs):
    for obj in objs:
        download_image(obj["title"], obj["width"], obj["height"], obj["url"])


def download_image(title, width, height, url):
    filename="{0}-{1}-{2}".format(width, height, slugify(title))
    response=requests.get(url, allow_redirects=True)
    content_type = response.headers['content-type']
    extension = mimetypes.guess_extension(content_type)
    if extension == ".png" or extension == ".jpg":
        filepath="{0}/{1}{2}".format("downloaded/", filename, extension)
        open(filepath, "wb").write(response.content)
        print("{0} downloaded".format(filepath))

search("gerry scotti")