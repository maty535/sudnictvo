from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

url = "https://www.slov-lex.sk/pravne-predpisy/SK/ZZ/2005/300/"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")


pNum=re.compile(r'paragraf-(?P<par>\w+)\.nadpis')
#print(soup.get_text())
#paragrafy = soup.find_all("div", class_="paragrafOznacenie")
pNadpisy  = soup.find_all( class_="paragrafNadpis NADPIS")
print(pNadpisy)

parMap = {}

for nadpis in pNadpisy:
    #print(nadpis.attrs)
    num = pNum.search(nadpis.get("id"))
    #print("{}:{}".format( num.group("par"), nadpis.string))
    parMap[num.group("par")] = nadpis.string

import pprint
import json

pp = pprint.PrettyPrinter(sort_dicts=False)
pp.pprint(parMap)
f = open("trestnyZakon.json", mode ="w",encoding='utf-8')
f.write(json.dumps(parMap, sort_keys = False, indent = 2,ensure_ascii=False))
