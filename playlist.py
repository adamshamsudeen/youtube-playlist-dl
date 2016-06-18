import urllib
import requests
from bs4 import BeautifulSoup
import re

def downloader(url,file_name):

	u = urllib.urlopen(url)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "Downloading: %s Bytes: %s" % (file_name, file_size)

	file_size_dl = 0
	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break

	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print status,
	f.close()

def video(url,quality):

	link_new="http://keepvid.com/?url="+url
	page = requests.get(link_new)
	source = page.text
	word=[]
	soup = BeautifulSoup(source, "html.parser")
	name=soup.find('a', {'class': 'n'}).text

	for links in soup.findAll('a', {'class': 'l'}):
	  word.append(links["href"])

	  


	if (len(word)>12 and quality==1):
		choice=1

	elif len(word)>2:
		choice=0

	name = str(name)+".mp4"
	downloader(word[choice], name)


def playlst(url,quality): 		#funtion to download playlist

	limit = raw_input("Enter \"yes\" to download entire playlist:")
	if limit=="yes":
		limit=1500
	else:
		limit = int(raw_input("Select the number of videos to download:"))
	
	page = requests.get(url)
	source = page.text
	i=0
	soup = BeautifulSoup(source, "html.parser")
	links =soup.findAll('a', {'class': 'pl-video-title-link yt-uix-tile-link yt-uix-sessionlink  spf-link '})

	for link in links:
	  link_new="http://keepvid.com/?url=https://www.youtube.com"+link.get('href')
	  if i>limit:
	    break
	  page = requests.get(link_new)
	  source = page.text
	  word=[]
	  soup = BeautifulSoup(source, "html.parser")
	  name=soup.find('a', {'class': 'n'}).text
	  
	  for links in soup.findAll('a', {'class': 'l'}):
	      word.append(links["href"])

	      
	  

	  if (len(word)>12 and quality==1):
	  	choice=1

	  elif len(word)>2:
	  	choice=0
	  else:
	  	continue

	  i=i+1
	  name = str(name)+".mp4"
	  downloader(word[choice], name)


def main() :
	url="https://www.youtube.com/watch?v=Yfr5ISTSIAM"
	#url="https://www.youtube.com/playlist?list=PLdJhb8qMrVC1mydazcLgJZ5X7txkkWYy_"
	quality =raw_input("Enter \"1\" for maximum qulity and \"2\" for 480p:")
	result = re.match('^.*playlist.*$',url)			#check if it is a playlist
	if result:
		playlst(url,quality)
	else:
		video(url,quality)


if __name__ == "__main__" :
  main()