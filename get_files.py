# FUNCTION TO SCRAPE FILES ON WEBSITE
#  with 3 arguments: 
#   1) URL
#   2) folder to save files
#   3) list of filetypes to scrape
#  Sean Higgins and Angelyna Ye
#  created 2015
#  last revised 3mar2018

from bs4 import BeautifulSoup as bs # scraping
from urllib.parse import urlparse #parse urlbase
from urllib.request import urlopen
import requests
import os # for shell commands like change directory
import re # regular expressions
import glob # for list of files in a directory; see http://goo.gl/rVNp22
import urllib.parse # for modify broken url with whitespace
import zipfile, io

# FUNCTION TO SCRAPE FILES
def get_files(myurl, folder = [], overwrite = True, *Type):
	# say hello
	print ('-----')
	print ('Scraping from %s' % myurl)
	print ('-----')
	
	# urlbase = re.sub(r'http://.*/', "", myurl)
	# print(urlbase)
	if folder == []:
		folder = os.getcwd()
	os.chdir(folder)
	Typecheck = []
	if type(Type[0]) == str:
		for typ in Type:
			Typecheck.append(typ)	
	else:
		Typecheck = Type[0]
	for t in Typecheck:
		already = glob.glob('*.' + t + '*')
	resp = urlopen(myurl)
	
	# scrape 
	soup = bs(resp.read(), "html.parser")
	links = soup.find_all('a')

	parsemyurl = urlparse(myurl)
	urlbase = parsemyurl.scheme + '://' + parsemyurl.netloc + '/' 
	urlbase2 = parsemyurl.scheme + '://' + parsemyurl.netloc 


	urls = []
	longurls = []

	for link in links:
		longer_url = link.get('href')
		emptyOrNot = (longer_url == None)
		if emptyOrNot == True: continue #if longer_url is empty, prevent it from causing "'NoneType' is not iterable" Error
		for t in Typecheck:
			if longer_url.endswith(t): 
				if not longer_url.startswith('http://'):
					if longer_url.startswith('/'):
						adj = urllib.parse.quote(longer_url)
						adj_url = urlbase2 + adj
					else:
						adj_url = urlbase + longer_url
				if adj_url.endswith('zip'):
					try:
						r = requests.get(adj_url)
						z = zipfile.ZipFile(io.BytesIO(r.content))
						z.extractall()
					except Exception as e: 
						print("Error downloading:  " + adj_url)
						print(e)
						continue
				if adj_url in longurls: continue # for duplicates
				url = re.sub(r'http://.*/', "", adj_url)
				if url in already and overwrite == True: 
					print ("%s already downloaded" % url)
					continue # break out of loop if already downloaded
				longurls.append(adj_url)
				urls.append(url)
	urls_longurls = zip(urls,longurls)

	for url, longurl in urls_longurls:
		try: 
				usefulfiles = urlopen(longurl)
		except: 
			print ("error downloading %s" % url)
			continue
		finalfile = usefulfiles.read()
		with open(url,'wb') as code:
			code.write(finalfile)
		print ("Successfully downloaded %s" % url)

	# say goodbye
	print ('-----')
	print ('Finished sraping from %s' % myurl)
	print ('-----')	
