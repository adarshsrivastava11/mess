import socket
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup
REMOTE_SERVER = "www.google.com"
def is_connected():
  try:
    
    host = socket.gethostbyname(REMOTE_SERVER)
    
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

if is_connected() == True:
  wiki = "http://127.0.0.1:8000/backup/"
  page = urllib2.urlopen(wiki)
  soup = BeautifulSoup(page,"html.parser")
  # print soup

  now = datetime.now().strftime('%H')
  fo = open(str(now)+".html", "a+")
  if now == '03':
    fo.write(str(soup))

