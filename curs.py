from pprint import pprint
import requests
from bs4 import BeautifulSoup
from datetime import date
import urllib.request
import xml.dom.minidom as minidom


def get_data(xml_url):
    web_file = urllib.request.urlopen(url)
    return web_file.read()


def get_currencies_dictionary(xml_content):
    dom = minidom.parseString(xml_content)
    elements = dom.getElementsByTagName("Valute")
    currency_dict = {}

    for node in elements:
        for child in node.childNodes:
            if child.nodeType == 1:
                if child.tagName == 'Value':
                    if child.firstChild.nodeType == 3:
                        value = float(child.firstChild.data.replace(',', '.'))
                if child.tagName == 'CharCode':
                    if child.firstChild.nodeType == 3:
                        char_code = child.firstChild.data
        currency_dict[char_code] = value
    return currency_dict


today = date.today().strftime("%d/%m/%Y")
url = f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={today}"
currency_dict = get_currencies_dictionary(get_data(url))['USD']
# print(currency_dict)
