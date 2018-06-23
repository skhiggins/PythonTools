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
import zipfile, io #for zip file 
from selenium import webdriver #use selenium for the dynamic content 





# FUNCTION TO SCRAPE FILES
def get_files(myurl,Type, folder = [], overwrite = True, contains = [], count = 0):
	# say hello
	# count is the variable to count how many urls we have urlopen yet
	# It is used to decide whether to use Selenium to scrape dynamic content or not 
	# if you want to use the selenium to scrape the content anyway, set count to -1
	helper_count = count
	if helper_count == -1:
		count = 0
	if count == 0:
		print ('-----')
		print ('Scraping from %s' % myurl)
		print ('-----')
		if folder == []:
			folder = os.getcwd()
		os.chdir(folder)
		resp = urlopen(myurl)
		
		# scrape 
		soup = bs(resp.read(), "html.parser")
		links = soup.find_all("a")
	else:
		# using the selenium to immitate a person manully open the website and click the js to get the html
		option = webdriver.ChromeOptions()
		option.add_argument("— incognito")
        # change this line to the place where you download your Chrome web driver
		browser = webdriver.Chrome(executable_path="/Applications/chromedriver", chrome_options=option)
		browser.get(myurl)
		html = browser.page_source

		# scrape
		soup = bs(html, "lxml")
		links = soup.find_all('a')

	Typecheck = []
	if type(Type) == type([]):
		Typecheck = Type
	elif isinstance(Type, str):	
		Typecheck.append(Type)
	else:
		print("Please input Type in a correct form (either as a string or a list of strings)")
		return
	for t in Typecheck:
			already = glob.glob('*.' + t + '*')	

	parsemyurl = urlparse(myurl)
	urlbase = parsemyurl.scheme + '://' + parsemyurl.netloc
	urlbase2 = myurl.rsplit('/', 1)[0] 

	urls = []
	longurls = []
	containlist = []
	originallist = []


	for link in links:
		longer_url = link.get('href')
		emptyOrNot = (longer_url == None)
		if emptyOrNot == True: continue #if longer_url is empty, prevent it from causing "'NoneType' is not iterable" Error
		for t in Typecheck:
			if longer_url.endswith(t):
				adj_url = longer_url
				if not (longer_url.startswith('http://') or longer_url.startswith('https://')):
					if longer_url.startswith('/'):
						adj = urllib.parse.quote(longer_url)
						adj_url = urlbase + adj
					elif longer_url.endswith('zip'):
						split_helper = re.search(r'\/', longer_url)
						adj_url = longer_url[split_helper.span()[0]:]
						adj_url = urlbase + adj_url
					else:
						adj_url = urlbase + '/' + longer_url
				if adj_url in longurls: continue # for duplicates
				skipornot = False;
				if contains != []: 
					if isinstance(contains, str):	
						containlist.append(contains)
					else :
						containlist = contains
					for c in containlist:
						checkname = re.compile(c)
						if checkname.search(adj_url) == None:
							skipornot = True
				if skipornot: continue
				url = re.sub(r'http://.*/', "", adj_url)
				url = re.sub(r'https://.*/', "", url)
				if url in already and overwrite == False: 
					print ("%s already downloaded" % url)
					continue # break out of loop if already downloaded
				longurls.append(adj_url)
				urls.append(url)
				originallist.append(longer_url)
	urls_longurls = zip(urls,longurls, originallist)

	for url, longurl, original in urls_longurls:
		try: 
			try:
				usefulfiles = urlopen(longurl)
				count += 100
			except:
				usefulfiles = urlopen(urlbase2 + "/" + original)
		except Exception as e: 
			print ("error downloading %s" % url)
			print(e)
			continue
		finalfile = usefulfiles.read()
		with open(url,'wb') as code:
			code.write(finalfile)
		print ("Successfully downloaded %s" % url)



#scrape from url hidden inside onclick
	urlson = []
	longurlon  = []
	for link in links:
		longer_urlonclick = link.get('onclick')
		emptyOrNot = (longer_urlonclick == None)
		if emptyOrNot == True: continue #if longer_url is empty, prevent it from causing "'NoneType' is not iterable" Error
		for t in Typecheck:
			if t in longer_urlonclick: 
				findstart = re.compile('http')
				findend = re.compile(t)
				startnum = findstart.search(longer_urlonclick).span()[0]
				endnumclass = findend.search(longer_urlonclick)
				endnum = endnumclass.span()[len(endnumclass.span()) - 1]
				adjurlon = longer_urlonclick[startnum:endnum]
				if adjurlon in longurlon: continue # for duplicates
				if contains != []: 
					if isinstance(contains, str):	
						containlist.append(contains)
					else :
						containlist = contains
					for c in containlist:
						checkname = re.compile(c)
						if checkname.search(adjurlon) == None:
							skipornot = True
				if skipornot: continue
				url_on = re.sub(r'http://.*/', "", adjurlon)
				if url_on in already and overwrite == False: 
					print ("%s already downloaded" % url)
					continue # break out of loop if already downloaded
				longurlon.append(adjurlon)
				urlson.append(url_on)
	urls_longurlson = zip(urlson,longurlon)

	for onclickurl, onclicklongurl in urls_longurlson:
		try: 
			count += 100
			onclickusefulfiles = urlopen(onclicklongurl)
		except: 
			print ("error downloading %s" % onclickurl)
			continue
		onclickfinalfile = onclickusefulfiles.read()
		with open(onclickurl,'wb') as code:
			code.write(onclickfinalfile)
		print ("Successfully downloaded %s" % onclickurl)
	
	# if the source page doesn't contains the specific file that we want, we use the selenium to 
	# scrpe the dynamic content of the website 
	if count == 0 or helper_count == -1:
		# increase the count in order to break out of the loop once we have tried to use selenium 
		# for one time
		count += 100
		get_files(myurl,Type, folder, overwrite, contains, count = count)
	else:
		# say goodbye
		print ('-----')
		print ('Finished sraping from %s' % myurl)
		print ('-----')




