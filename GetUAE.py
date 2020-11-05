import os
import time
import requests
from BaseGetUniDatabase import BaseGetUniDatabase
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select

class GetUAE(BaseGetUniDatabase):

    # Use a link to a html file with search results to create an instance
    def __init__(self, path):
        self.path = path # path to folder with html files with search results
        self.links=[]     # links for universities at CAA website
        self.universities=[] # university names
        self.websites=[] #university websites
        self.country = 'UAE'
        self.public = ['United Arab Emirates University',
                       'Zayed University',
                       'Higher Colleges Of Technology']
        self.browser = webdriver.Firefox(executable_path = 'geckodriver.exe')


    def updateLinks(self):
        # retrieves ids of all the universities in the html file
        for filename in os.listdir(self.path):
            with open(os.path.join(self.path, filename), 'r') as f: # open in readonly mode
                # do your stuff
                contents = f.read()

            soup = BeautifulSoup(contents, 'lxml')

            # self.links.append(soup)
            for uni in soup.find_all('tr'):
                # retrieve id
                self.links.append('https://www.caa.ae/' + uni.td.a.get('href'))
                self.universities.append(uni.td.a.text.lower().title())
                website = uni.find(
                                   'span', class_='vuetable-actions'
                                   ).a.get('href')
                if website == 'javascript:void(0);':
                    self.websites.append(None)
                    continue
                self.websites.append(website)

    def getData(self) -> list:
        # rerieves all the data about each university in the html file
        data = []
        for id in range(len(self.universities)):
             data.append(self.getSingleUniData(id))

        return(data)

    def getSingleUniData(self, id) -> tuple:
        # return a turple with a university information
        resp = requests.get(self.links[id])
        soup=BeautifulSoup(resp.text, "html5lib")

        name = self.getUniName(id)
        country = self.getUniCountry()
        funding = self.getFunding(id)
        website = self.getUniWebsite(id)
        majors = self.getUniMajors(id)

        return(country, name, funding, website, majors)

    def getUniName(self, id) -> str:
        # retrieve uni name
        return(self.universities[id])

    def getFunding(self, id) -> str:
        # retrieve uni type of funding
        if self.universities[id] not in self.public:
            return('Private')
        else:
            return('Public')

    def getUniCountry(self) -> str:
        # retrieve uni country
        return('United Arab Emirates')

    def getUniWebsite(self, id) -> str:
        # retrieve uni website
        return(self.websites[id])

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
