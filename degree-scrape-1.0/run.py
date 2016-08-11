from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import time
import sys

_url = "http://www.abbreviations.com/acronyms/DEGREES/"
Url = _url
more = True
page_number = 1
country_isos = []
tail = ''
file = open('data-set.csv', "w")
file.write("degreeAccronym|degreeName \n")

def country_row_iso(abrv,name):
	a = abrv.encode(sys.stdout.encoding, errors='replace')
	fN = name.encode(sys.stdout.encoding, errors='replace')
	try:
		return str(a.decode("utf-8")) + "|" + str(fN.decode("utf-8"))
	except:
		return str(a) + "|" + str(fN)
while more:
	if(page_number > 1):
		Url = _url + str(page_number)

	url = urlopen(Url)
	content = url.read()
	soup = BeautifulSoup(content, "html.parser")
	tables = soup.findAll("table", class_="tdata")
	for table in tables:
		tableBody = table.findAll("tbody")
		for body in tableBody:
			rows = body.findAll("tr")
			for row in rows:
				abbreviation_col = row.find("td", class_="tm")
				abbreviation_link = abbreviation_col.find("a")
				abbreviation = abbreviation_link.contents[0]

				fullname_col = row.find("td", class_="dm")
				fullname = fullname_col.contents[0]

				country_isos.append(country_row_iso(abbreviation, fullname))

	more = (page_number != 61)
	page_number += 1
	
	for country_iso in country_isos:
		file.write(country_iso + "\n")
	print(str(Url) + " => [Scraped]")
	time.sleep(.5)
	pass
