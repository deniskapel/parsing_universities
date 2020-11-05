import os
import time
from BaseGetUniDatabase import BaseGetUniDatabase
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
import re

class GetJordan(BaseGetUniDatabase):

    # Use a link to a html file with search results to create an instance
    def __init__(self):
        self.path = 'http://rce.mohe.gov.jo/StudyInJordan/en/' # path to folder with html files with search results
        self.links=[]     # links for universities at CAA website
        self.universities=[] # university names
        self.websites=[] #university websites
        self.country = 'Jordan'


    def updateLinks(self):
        pass


    def getData(self) -> list:
        # rerieves all the data about each university in the html file
        resp = requests.get(self.path)
        soup=BeautifulSoup((resp.text).encode('ascii', 'ignore'), "html5lib")

        pattern = "item \w* clearfix"
        temp = soup.find_all('div', class_=re.compile(pattern))
        # temp = soup.find_all('div', class_="item")

        data = []

        for grouping in temp:
            data.extend(self.extractUniversities(grouping))
            # data.extend(grouping)

        # data = []
        # for id in range(len(self.universities)):
        #      data.append(self.getSingleUniData(id))
        #
        return(data)

    def extractUniversities(self, html):
        unis = html.find_all('div', class_="univdiv")
        data = []
        funding = html.p.text

        stpwrd = "Community Colleges affiliated to Al-Balqa Applied University"
        if funding != stpwrd:
            for uni in unis:
                data.append(self.getSingleUniData(uni, funding))
        else:
            pattern="col-md-12 pull-left"
            data.extend(
                        self.extractColleges(
                                             html.find('div', class_=pattern)))

        return(data)

    def getSingleUniData(self, html, funding) -> tuple:
        # return a turple with a university information
        name = self.getUniName(html)
        country = self.getUniCountry()
        funding = self.getFunding(funding)
        if html.a != None:
            website = self.getUniWebsite(html.a)
        else:
            website = self.getUniWebsite(html)

        # majors = self.getUniMajors(id)
        return(country, name, funding, website)

    def extractColleges(self, html) -> tuple:
        # return a turple with a university information
        funding = ""
        # temp = html.p.find_next_siblings()
        data = []
        # data = html.descendants
        for child in html.children:
            if child.name == None:
                continue
            if child.name == "p":
                funding = child.text
            if re.search('(clearfix)|(Affiliated)', str(child)) != None:
                continue
            else:
                data.append(self.getSingleUniData(child, funding))

        return(data)

    def getUniName(self, html) -> str:
        # retrieve uni name
        return(html.text)

    def getFunding(self, string) -> str:
        # retrieve uni type of funding
        if re.search("Public", string) != None:
            return('Public')
        elif re.search("Private", string) != None:
            return("Private")
        elif re.search(r"(A|a)ffiliated", string) != None:
            return("Public")
        # if string == 'Public Universities':
        #     return("Public")
        # elif string == 'Private Universities':
        #     return("Private")
        # elif string == 'Private Colleges':
        #     return("Private")
        elif string == "Programs in partnership with foreign universities":
            return('Partnership')
        elif string == "Regional Institutes and Universities":
            return('Private')
        return(string)

    def getUniCountry(self) -> str:
        # retrieve uni country
        return(self.country)

    def getUniWebsite(self, html) -> str:
        # retrieve uni website
        url = html.get('href')
        if url == '#hei':
            return(None)

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
