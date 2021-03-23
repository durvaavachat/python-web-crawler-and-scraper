import os
import ftputil  # to access all ftp utilities such as connection etc.
from configparser import RawConfigParser


file = "test_config.ini"
parser = RawConfigParser()
parser.read(file)
host = parser['ftp_connect']['host']
user = parser['ftp_connect']['user']
pwd = parser['ftp_connect']['pwd']


# connect to FTP and return the connection
def getFtpHostConnection():
    ftpHost = ftputil.FTPHost(host, user, pwd)
    return ftpHost
    

def uploadFiles(localDir, domain):
	ftpHost = getFtpHostConnection()  # get FTP connection
	ftpDir = ftpHost.getcwd()  # get current working directory of FTP

	if os.path.isdir(localDir+domain):  # check whether the company name folder is present on disk/local
		if ftpHost.path.isdir(ftpDir+domain):  # check whether the company name folder is present on FTP
			ftpHost.rmtree(domain, ignore_errors=False, onerror=None)  # remove entire directory with the files present inside any for daily schedule

		ftpHost.mkdir(domain)
		ftpHost.chdir(domain)  

		filesToUpload = os.listdir(localDir+domain)  # list out the files inside local company directory

		# loop through the list of files in company directory to upload them on FTP
		for fileToUpload in filesToUpload:
			ftpHost.upload(localDir+domain+"/"+fileToUpload, ftpDir+domain+"/"+fileToUpload)		
	ftpHost.close()	
