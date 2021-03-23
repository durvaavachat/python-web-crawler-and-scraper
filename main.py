import logging	# to create log files
from datetime import date
import csv
import tldextract

# include files
from websitecrawler.local_functions import *
from websitecrawler.ftp_functions import *


# Create and configure logger
logging.basicConfig(filename=os.getcwd()+"/logs/"+str(date.today())+".log", format='%(asctime)s %(message) s', filemode='w')

# set name of the directory to which websites are going to save as a global variable
savedWebsitesDirName = "/savedwebsites/"

# main program
def main():
	localDir = os.getcwd() + savedWebsitesDirName	# set working directory
	
	with open('webpages_to_crawl.csv') as csv_file:
		csvReader = csv.reader(csv_file, delimiter=',')		# store website URLs and xpaths into variable

		# loop through csv array which includes urls[0] and xpaths[1]
		for row in csvReader:
			try:
				domain = tldextract.extract(row[0]).domain  # get domain without ext ie .com.au

				# Save Files to Disk
				createFiles(localDir, domain, row)
				
				# Upload Files to FTP
				uploadFiles(localDir, domain)
				
			except Exception:
				logging.exception("Exception occurred while scraping \""+domain+"\" website")
				# logger=logging.getLogger() 							#Create an object
				# logger.exception(logging.DEBUG) 						#Set the threshold of logger to DEBUG
				pass


# start main program
if __name__ == "__main__":
	main()
