import os
import time
from BaseGetUniDatabase import BaseGetUniDatabase
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
import re

class GetOman(BaseGetUniDatabase):

    # Use a link to a html file with search results to create an instance
    def __init__(self, path):
        self.path = path # path to folder with xml files with search results
        self.links=[]     # links for universities at CAA website
        self.universities=[] # university names
        self.websites=[] #university websites
        self.country = 'Oman'
        self.funding = 'Private'
        self.majors = []


    def updateLinks(self):
        # retrieves ids of all the universities in the html file
        pass

    def getData(self) -> list:
        # rerieves all the data about each university in the html file
        for filename in os.listdir(self.path):
            with open(os.path.join(self.path, filename), 'r') as f: # open in readonly mode
                # do your stuff
                contents = f.read()

            contents = re.sub(r'\w+:(?=[A-Z])', '', contents)
            soup = BeautifulSoup(contents.encode('ascii', 'ignore'), 'xml')

            self.universities.extend(self.extractUniversities(soup))
            self.websites.extend(self.extractWebsites(soup))

            data = []

            for id in range(len(self.universities)):
                data.append(self.getSingleUniData(id))

            return(data)

    def extractUniversities(self, soup) -> list:
        return(soup.find_all('Font',
                             attrs={'Face':"Lucida Sans",
                                    'Size':"12",
                                    'Color':'#006C8F'}))

    def extractWebsites(self, soup) -> list:
        no_tags = ''
        for row in soup.find_all('Data'):
            no_tags += row.text
        pattern = re.compile('www\.(?!mohe).*\.c?om'
                             '|'
                             'www\..*\.org')
        results = re.findall(pattern, no_tags)
        results = list(dict.fromkeys(results)) # remove duplicates, keep order
        return(results)

    def getSingleUniData(self, id) -> tuple:
        # return a turple with a university information
        name = self.getUniName(id)
        country = self.getUniCountry()
        funding = self.getFunding()
        website = self.getUniWebsite(id)
        return(country, name, funding, website)

    def getUniName(self, id) -> str:
        # retrieve uni name
        return(self.universities[id].text)

    def getFunding(self) -> str:
        # retrieve uni type of funding
        return(self.funding)

    def getUniCountry(self) -> str:
        # retrieve uni country
        return(self.country)

    def getUniWebsite(self, id) -> str:
        # retrieve uni website
        return(self.websites[id])

        return(url)

    def getUniMajors(self, id) -> str:
        # retrieve majors
        try:
            data = []
            for tr in self.loadMajors(self.links[id]):
                data.append(tr.td.a.text.lower())
            return(data)
        except Exception:
            return(None)

    def loadMajors(self, url) -> list:
        # load a html table of majors from a given url using selenium
        self.browser.get(url)
        self.updateDynamicData() # click necessary data
        soup = BeautifulSoup(
                             (self.browser.page_source).encode('ascii', 'ignore'),
                             "html5lib"
                             )
        return(soup.find_all('tr')[7:]) # skip first elems with no relevant info


    def updateDynamicData(self):
        # updates loaded dynamic data by clicking necessary buttons
        dropdown = "//div[@class='selectize-control form-control form-control-sm single']"
        button = "//div[@class='selectize-dropdown-content']/div[text()='100']"
        self.waitLoading()
        self.browser.find_element_by_xpath(dropdown).click()
        self.waitLoading()
        self.browser.find_element_by_xpath(button).click()
        self.waitLoading()

    def waitLoading(self, seconds=5):
        # take a 5-sec pause to give dynamic data time to load
        time.sleep(seconds)
