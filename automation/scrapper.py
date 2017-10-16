import urllib2
from bs4 import BeautifulSoup
wiki = "http://home.iitk.ac.in/~himnshu/studentsearch/index.php?query=14099&gender=all&batch=all&hall=all&degree=all&dept=all&blood=all"
page = urllib2.urlopen(wiki)
soup = BeautifulSoup(page,"html.parser")
all_links=soup.find_all("a")
for link in all_links:
	a= link.get("href")

b = a.split('=')
print b[1]

info = "http://home.iitk.ac.in/~himnshu/studentsearch/profile.php?username="+b[1]+""
page = urllib2.urlopen(info)
soup = BeautifulSoup(page,"html.parser")
all_p = soup.find_all("p")
c =  all_p[4].text.split(',')
print c[0]
