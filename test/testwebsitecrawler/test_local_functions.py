import time
import os
import re  # to replace special charcters
import furl  # to split full URL into fragments like scheme, subdomain, path, etc.
from lxml import html  # to handle xml & html files and scrape the webpages
import shutil	# subdirectories & files
from urllib.parse import urlparse  # to extract host name from category page URL listed in websites_to_crawl.csv file

# from selenium.webdriver import Firefox
from selenium import webdriver

# from filelock import FileLock


def getDriver():
    # driverpath = 'C:\Program Files (x86)\geckodriver.exe'   # Firefox webdriver path
    driverpath = 'C:\Program Files (x86)\chromedriver.exe'    # Chrome webdriver path

    # driver = Firefox(executable_path = driverpath)          # get firefox webdriver instance
    driver = webdriver.Chrome(driverpath)                     # get chrome webdriver instance
    return driver


def splitShortenAndCreateFullURL(row, splitProdUrl):
	categoryHostName = urlparse(row[0]).netloc  # parse category page url to get netloc e.g. "www.woolworths.com.au"
	if len(splitProdUrl)>1:
		urlWOSpecialChar = re.sub(r'\W+', r'-', splitProdUrl[1])
		prodPage = urlWOSpecialChar.strip("-")
		prodPgUrl = categoryHostName + splitProdUrl[1]
	else:
		urlWOSpecialChar = re.sub(r'\W+', r'-', splitProdUrl[0])
		prodPage = urlWOSpecialChar.strip("-")
		prodPgUrl = categoryHostName + splitProdUrl[0]

	prodPage = "-".join(prodPage.split("-")[:15])

	return prodPage, prodPgUrl


def createFiles(localDir, domain, row):
	os.chdir(localDir)  # change directory to ../savedwebsites
	if os.path.exists(localDir+"/"+domain):  # create company directory eg ../savedwebsites/jbhifi if doesn't exists
		shutil.rmtree(localDir+"/"+domain)   # otherwise remove above directory & files inside, then recreate it for fresh copy
				
	os.mkdir(domain)  # create company directory to save .html files on daily schedule

	categoryPgDriver = getDriver()  # get chrome driver to use further for search/crawl the webpages
	categoryPgDriver.get(row[0])  # get/load category/specials page URL

	time.sleep(10)
	
	categoryPgSource = categoryPgDriver.page_source  # get source code of category web page

	xmltree = html.fromstring(categoryPgSource)  # parses an xml/html section from a string constant
	productLinks = xmltree.xpath(row[1])  # get all the href attribute values from category web page i.e. URLs of the product pages

	os.chdir(domain)

	# with FileLock("sales-original-source.html.lock"):
	# create "sales-original-source.html" file and save category page source code
	with open("sales-original-source.html", "w+", encoding="utf-8") as categoryPg:
		categoryPg.write(categoryPgSource)
		categoryPg.close()

	# with FileLock("specials.html.lock"):
	# create "specials.html" file, create product page URLs having FTP host name 
	# create individual product page and save it's source code in the same file
	with open("specials.html", "w+", encoding="utf-8") as specialsFile:
		# loop through all the product links list above
		# i=1 counter used in product file creation
		for productLink in productLinks:
			fragmentedProdUrl = furl.furl(productLink)  # fragment product url into URL components path, segments, etc.
			splitProdUrl = productLink.split(fragmentedProdUrl.origin)  # split origin of into netloc, etc. i.e. get netloc="www.woolworths.com.au"

			# find out the length of the split/parsed prod page url

			shortenedProdPgNameAndFullURL = splitShortenAndCreateFullURL(row, splitProdUrl)

			specialsFile.write("<a class='fc_products' href='https://savedwebsites.findcheap.com.au/"+domain+"/"+shortenedProdPgNameAndFullURL[0]+".html'>"+shortenedProdPgNameAndFullURL[0]+"</a><br/>")  # create prod page urls in specials.html

			prodPgDriver = getDriver()  # get driver for individual products
			prodPgDriver.get("https://"+shortenedProdPgNameAndFullURL[1])  # get web page of product
			prodPgSource = prodPgDriver.page_source  # get source code of product page
			prodPgDriver.quit()  # quit the driver connection so that it will close browser's all windows

			# with FileLock(prodPage+".html.lock"):
			# create product's .html file containing product source code
			
			with open(shortenedProdPgNameAndFullURL[0]+".html", "w+", encoding="utf-8") as prodPg:
				# i=i+1 counter used in product file creation
				prodPg.write(prodPgSource)
			prodPg.close()
	specialsFile.close()
	categoryPgDriver.quit()  # quit the driver connection so that it will close browser's all windows
