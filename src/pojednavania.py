from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

url = "https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2005/300/"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

