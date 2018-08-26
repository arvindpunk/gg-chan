import requests
import re
from bs4 import BeautifulSoup

async def getRating(handle):
    r = requests.get("https://www.codechef.com/users/" + handle)
    a = r.content
    soup = BeautifulSoup(a, 'html.parser')
    rating = soup.find("div", "rating-number")
    if rating == None:
    	return -1
    else:
    	return int(rating.text)

def getRoleFromRating(rating):
    rating = int(rating)
    if(rating<1400):
        s='1'
    elif(rating<1600):
        s='2'
    elif(rating<1800):
        s='3'
    elif(rating<2000):
        s='4'
    elif(rating<2200):
        s='5'
    elif(rating<2500):
        s='6'
    else:
        s='7'
    return s+"star"

async def getSubmissions(handle=''):
	r = requests.get("https://www.codechef.com/status/FLOW006")
	a = r.content
	soup = BeautifulSoup(a, 'html.parser')
	data = soup.find_all("tr", class_=re.compile("kol"))
	l=[]
	for row in data:
		strRow = str(row)
		if handle in strRow:
			l.append(strRow[83:91])
	return l