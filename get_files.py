# Notice:
# The following script uses Selenium to scrape dynamic contents of the website, and requires
# the user to download the following packages and drivers
# 1. Selenium package — used to automate web browser interaction from Python
# 	 Please download the package from the following link: "https://pypi.org/project/selenium/"
# 2. ChromeDriver — provides a platform to launch and perform tasks in specified browser.
#    Please download the package from the following link: "https://sites.google.com/a/chromium.org/chromedriver/home"

# FUNCTION TO SCRAPE FILES ON WEBSITE
#  with 7 arguments: 
#   1) myurl: URL to scrape 
#   2) Type: list of file types to scrape
#   3) folder: folder to save files
#   4) ovewirte: set to False if the user doesn't want to download 
#                the files that the user have already downloaded in the folder
#				 the default value is set to True
#   5) contains: files' names to skip. use to skip files with specific names
#   6) count: if the user wants to use the selenium to scrape the dynamic content regardless of 
#             how many pdf have already been downloaded, please set count to -1
#             count is the variable to count how many URLs we have urlopen yet
#             It is used to decide whether to use Selenium to scrape dynamic content or not 
#   7) filepath: folder to locate ChromeDriver
#  Sean Higgins and Angelyna Ye
#  created 2015
#  last revised 30 June 2018

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
def get_files(myurl,Type, folder = [], overwrite = True, 
	contains = [], count = 0, filepath = []):
	# Use helper_count to store the original value of count
	helper_count = count
	# if helper_count equals 1, Selenium must be ran
	# but we first need to reset count to 0, to start the first routine of web scraping
	if helper_count == -1:
		count = 0
	# if it's the first time, get_files is called
	if count == 0:
		# say hello
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

	# use the selenium to imitate a person manully open the website and click the Javascrip
	# to get the html
	# Please don't close the pop-up Chrome window while scraping!	
	else:
		try: 
			option = webdriver.ChromeOptions()
			option.add_argument("--incognito")
			if filepath == []:
				browser = webdriver.Chrome(executable_path="/Applications/chromedriver", chrome_options=option)
			else:
				browser = webdriver.Chrome(executable_path=filepath, chrome_options=option)
			browser.get(myurl)
			html = browser.page_source
		except Exception as e:
			print(e)
			Chrome_driver_url = "https://sites.google.com/a/chromium.org/chromedriver/home"
			Selenium_url = "https://pypi.org/project/selenium/"
			print("Please don't close the pop-up Chrome window while scraping")
			print("Please download the ChromeDriver from the following link: \n%s"  %Chrome_driver_url)
			print("Please download the Selenium Package from the following link: \n%s "  %Selenium_url)
			return;
		# scrape
		soup = bs(html, "lxml")
		links = soup.find_all('a')

	# Modify the Type input to a standard type
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

	# adjust the url
	parsemyurl = urlparse(myurl)
	urlbase = parsemyurl.scheme + '://' + parsemyurl.netloc
	urlbase2 = myurl.rsplit('/', 1)[0] 

	urls = []
	longurls = []
	containlist = []
	originallist = []
	skipornot = False;

	# start to scrape
	for link in links:
		longer_url = link.get('href')
		emptyOrNot = (longer_url == None)
		#if longer_url is empty, prevent it from causing "'NoneType' is not iterable" Error
		if emptyOrNot == True: continue 
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
				# for duplicates
				if adj_url in longurls: continue 
				# if the user want to skip files with specific names
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
			except:
				usefulfiles = urlopen(urlbase2 + "/" + original)
		except Exception as e: 
			print ("error downloading %s" % url)
			print(e)
			continue
		finalfile = usefulfiles.read()
		with open(url,'wb') as code:
			code.write(finalfile)
		count += 100
		print ("Successfully downloaded %s" % url)



# scrape from url hidden inside onclick
	urlson = []
	longurlon  = []
	for link in links:
		longer_urlonclick = link.get('onclick')
		emptyOrNot = (longer_urlonclick == None)
		#if longer_url is empty, prevent it from causing "'NoneType' is not iterable" Error
		if emptyOrNot == True: continue 
		for t in Typecheck:
			if t in longer_urlonclick: 
				findstart = re.compile('http')
				findend = re.compile(t)
				startnum = findstart.search(longer_urlonclick).span()[0]
				endnumclass = findend.search(longer_urlonclick)
				endnum = endnumclass.span()[len(endnumclass.span()) - 1]
				adjurlon = longer_urlonclick[startnum:endnum]
				# for duplicates
				if adjurlon in longurlon: continue 
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
				# break out of loop if already downloaded
				if url_on in already and overwrite == False: 
					print ("%s already downloaded" % url_on)
					continue 
				longurlon.append(adjurlon)
				urlson.append(url_on)
	urls_longurlson = zip(urlson,longurlon)

	# Dowload the files
	for onclickurl, onclicklongurl in urls_longurlson:
		try: 
			onclickusefulfiles = urlopen(onclicklongurl)
		except: 
			print ("error downloading %s" % onclickurl)
			continue
		onclickfinalfile = onclickusefulfiles.read()
		with open(onclickurl,'wb') as code:
			code.write(onclickfinalfile)
		count += 100
		print ("Successfully downloaded %s" % onclickurl)
	
	# if the source page doesn't contain the specific file that we want or 
	# the user want to use the Selenium, we use the Selenium to 
	# scrpe the dynamic content of the website 
	if (count == 0 and overwrite == True) or helper_count == -1:
		# increase the count to break out of the loop once we have tried to use selenium 
		# for one time
		count += 100
		# set the overwrite to false to avoid duplication
		get_files(myurl = myurl,Type = Type, folder = folder, 
			overwrite = False, contains = contains, count = count, filepath = filepath)
	else:
		# say goodbye
		print ('-----')
		print ('Finished sraping from %s' % myurl)
		print ('-----')




