# python-web-crawler-and-scraper

# Overview
This python-selenium project crawls and scrapes data from different web pages and uploads local data files to FTP.

# Motivation
Sometimes websites are not able to crawl using plugins on WordPress if javascript is disabled on your browser (any browser). And this was the motivation to write a Python-selenium script and cralw the webpages. 

# Technical Aspects
The actual flow of the script goes like:
1. Decide the webpages to crawl
2. Write xpath to reach to the product URLs
3. List out all the webpages and associated xpaths in .csv file
4. Read .csv file into the Python-selenium script
5. Check whether the directory is present or not (this is because this script is going to run daily using Windows Task Scheduler. As it is expected to have fresh webpages on daily basis, if the directory is present, delete it and create new each day)
6. Get and save source code of the category page into .html
7. Collect all the product page URLs, create appropriate URLs using these which will have FTP server domain name and save them in a .html file
8. Crate individual product pages and save source code of each of them in it
9. Once all the product pages of particular category have been crawled, it will check directory existance locally, check same directory is available on FTP or not, if directory is present on FTP, script will delete it and create new directory and upload all the files inside on FTP server
10. Further this data/files will be used to scrape data using plugin in WordPress
 
To achieve this, Selenium Chrome Webdriver and FTP Utilities have been used.

# Let's see Installation of Python and it's modules/libraries using pip
  - [Python and Selenium installation](https://www.youtube.com/watch?v=Xjv1sY630Uc)
  - To install the available Python modules and libraries you can use pip command 
    e.g. type below command in command prompt and hit enter. It will install selenium in your virtual environment.
    > **pip install selenium**
  - To write xpaths you can refer this [xpath cheatsheet](https://devhints.io/xpath)
  - To run this project you can direct to the folder containing main.py file and hit below command to execute the project 
    > **python main.py**
    OR if you are comfortable with PyCharm, then you will have to open project directory in PyCharm and set the Configuration by setting up path to main.py as a Script Path and then Run the project by clicking on little green play arrow
  
# Files used to run the code and directories/files created after it's execution are:
- CSV file
  The CSV file webpages_to_crawl.csv will look somthing like this:

  ![Contents of  csv file](https://user-images.githubusercontent.com/27036102/112404024-a685d700-8d63-11eb-89c7-6bfe217e48e1.png)

- Directories and files uploaded on FTP:

  [Directories named as Category name on server](https://github.com/durvaavachat/python-web-crawler-and-scraper/files/6201624/Category.directories.on.FTP.pdf)

  [Specials page](https://github.com/durvaavachat/python-web-crawler-and-scraper/files/6201628/Links.of.Posts.on.a.Category.page.pdf)

  [Individual product pages](https://github.com/durvaavachat/python-web-crawler-and-scraper/files/6201626/Posts.on.Category.page.pdf)


