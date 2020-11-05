import os
import time
from BaseGetUniDatabase import BaseGetUniDatabase
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import requests
import re

class GetLebanon(BaseGetUniDatabase):

    # Use a link to a html file with search results to create an instance
    def __init__(self):
        self.path = 'http://www.higher-edu.gov.lb/arabic/List_univ.htm' # path to folder with html files with search results
        self.links=[]     # links for universities at CAA website
        self.universities=[] # university names
        self.websites=[] #university websites
        self.country = 'Lebanon'


    def updateLinks(self):
        pass


    def getData(self) -> list:
        # rerieves all the data about each university in the html file
        resp = requests.get(self.path)
        soup=BeautifulSoup((resp.text).encode('ascii', 'ignore'), "html5lib")

        pattern = 'mso-yfti-irow:[1-9].*'
        unis = soup.find_all('tr', style=re.compile(pattern))

        data = []

        for uni in unis:
            data.append(self.getSingleUniData(uni))

        return(data)


    def getSingleUniData(self, html) -> tuple:
        # return a turple with a university information
        name = self.getUniName(html)
        website = self.getUniWebsite(html)
        country = self.getUniCountry()
        funding = self.getFunding(name)
        return(country, name, funding, website)

    def getUniName(self, html) -> str:
        # retrieve uni name
        # pattern = 'MsoNormal'
        # return(html.td.next_elem)
        return(re.sub(
                      '[^A-Za-z \(\)-]+',
                      '',
                      html.td.next_sibling.next_sibling.text.strip()))

    def getFunding(self, string) -> str:
        # retrieve uni type of funding
        if re.search("Lebanese  University", string) != None:
            return('Private')
        return('Public')

    def getUniCountry(self) -> str:
        # retrieve uni country
        return(self.country)

    def getUniWebsite(self, html) -> str:
        # retrieve uni website
        pattern = "width:148.85pt.*"
        url = html.find('td', style=re.compile(pattern)).text
        pattern = "(?<=@).*(?=\s)"
        website = re.findall(pattern, url)
        return('www.' +"".join(set(website)))

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
