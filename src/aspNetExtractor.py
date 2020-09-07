import requests
from   bs4 import BeautifulSoup
import urllib.parse as up
import re

import json

zakonyDictFile = open("trestnyZakon.json")
zakonyMap = json.loads(zakonyDictFile.read())

url = 'https://www.justice.gov.sk/Stranky/Sudy/Pojednavania/PojednavanieTrestZoznam.aspx'

requests.session().close()
with requests.session() as s:
    s.headers['user-agent'] = 'Mozilla/5.0'

    r    = s.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')

    target = (
        'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanie$ctl13$ctl00$cmbAGVCountOnPage'
    )

    # unsupported CSS Selector 'input[name^=ctl00][value]'
    data = { tag['name']: tag['value'] if tag.get("value") else ''
        for tag in soup.select('input') 
    }
    soup.select("input[name$=cmbAGVCountOnPage]")

    data.update({'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$cmbSud': 'OSPO', 
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanie$ctl13$ctl00$cmbAGVCountOnPage': '10',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanie$ctl13$ctl00$cmbAGVPager:': '1',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$btnHladaj.x': '13',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$btnHladaj.y': '10',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderSearchArea$ctl01$ctl04': '0'})
    
    #state = { tag['name']: tag['value'] if tag.get("value") else ''
    #    for tag in soup.select('input[name^=__]') 
    #}

    #data.update(state)
    

    # data['ctl00$FhMainContent$FhContent$ctl00$AnalysesCourse$CustomPager$total']
    
    last_page = len(soup.select('select[name$=Pager]')[0].find_all('option'))

    # for page in range(last_page + 1):
    data["__EVENTTARGET"] = 'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanie$ctl13$ctl00$cmbAGVCountOnPage'
    data["__EVENTARGUMENT"]=''
    data["__VIEWSTATEENCRYPTED"] =''
    
    r    = s.post(url, data=data)
    soup = BeautifulSoup(r.content, 'html5lib')
    data.clear()
    data = { tag['name']: tag['value'] if tag.get("value") else ''
            for tag in soup.select('input') 
    }
    data["__EVENTTARGET"] = ''
    data["__EVENTARGUMENT"]=''
    data["__VIEWSTATEENCRYPTED"] =''
    data.update({
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanie$ctl103$ctl00$cmbAGVCountOnPage': '100',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$gvPojednavanie$ctl103$ctl00$cmbAGVPager:': '1',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$btnHladaj.x': '13',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$btnHladaj.y': '10',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderSearchArea$ctl01$ctl04': '0',
                'InputKeywords': 'Hľadať na tejto lokalite...',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderSearchArea$ctl01$ctl00':'https://www.justice.gov.sk',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$cmbSud': 'OSPO', 
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$txtDatumPojednavania':'',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$txtDatumPojednavaniaOd':'',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$txtDatumPojednavaniaDo':'',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$txtSpisovaZnacka:':'',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$cmbFormaUkonu':'',
                'ctl00$ctl00$PlaceHolderMain$PlaceHolderMain$ctl01$txtObzalovani':'',
                })

    r    = s.post(url, data=data)
    soup = BeautifulSoup(r.content, 'html5lib')


    lineNum = 1
    paragrafNum=re.compile(r'§ (?P<par>\w+) *.')
    # unsupported CSS Selector 'tr:not(.tr_header)'
    for tr in soup.select('.GridTable tr'):
        if len(tr('td')) > 4:
            row = [ td.text.strip() for td in tr('td')[0:-1]]
            if row:

                num = paragrafNum.search(row[-2])
                
                print("{}\t{}\t{}\t{}\t{}".format( 
                            lineNum,
                            row[0], 
                            (zakonyMap.get(num.group("par"),num.group("par")) if num else row[-2]).ljust(50), 
                            row[-1].ljust(30),
                             '\t'.join(row[1::] )))
                lineNum+=1

        