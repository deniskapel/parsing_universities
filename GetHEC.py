import requests
import time
from BaseGetUniDatabase import BaseGetUniDatabase
from bs4 import BeautifulSoup
from selenium import webdriver
import sys

class GetHEC(BaseGetUniDatabase):

    def __init__(self):
        # path to a link with all the universities on www.hec.gov.pk
        self.path = "https://www.hec.gov.pk/english/universities/pages/recognised.aspx#k="
        self.links = [] # links to a single university on A database website
        # selenium for parsing dynamic websites
        self.browser = webdriver.Firefox(executable_path = 'geckodriver.exe')

    def updateLinks(self):
        # retrieves links to pages with listing of universities (216 on October 14,2020)
        for i in range(0,22): # total range(0,22)
            if i != 0:
                self.links.append(self.path + '#s=' + str(i) + '1')
                continue
            self.links.append(self.path)

    def getData(self) -> list:
        # rerieves all the data about each university in the html file
        data = []
        for link in self.links:
            data.extend(self.extractUniversities(link))

        return(data)

    def extractUniversities(self, url) -> list:
        # extract the info about all the universities on the html page
        self.browser.get(url)
        time.sleep(15)
        soup=BeautifulSoup(self.browser.page_source, "html5lib")
        data = soup.tbody.find_all('tr')
        temp = []
        for row in data:
            temp.append(self.getSingleUniData(row))

        return(temp)

    def getSingleUniData(self, row) -> tuple:
        # return a turple with a university information retrieved from a <td></td>
        cell = row.td
        name = self.getUniName(cell) # rertieve single cell
        hec_url = cell.a.get('href')
        website = self.getUniWebsite(hec_url)
        funding = self.getFunding(cell)
        field = self.getUniMajors(cell)
        country = 'Pakistan'

        return(name, country, funding, website, field, hec_url)

    def getUniName(self, html) -> str:
        # retrieve uni name
        try:
            return(html.text)
        except Exception:
            return('unknown UniName')

    def getFunding(self, html) -> str:
        # retrieve uni type of funding
        try:
            return(html.findNext('td').text)
        except Exception:
            return('No funding data')

    def getUniWebsite(self, url) -> str:
        # retrieve uni website
        try:
            resp = requests.get(url)
            soup=BeautifulSoup(resp.text, "html5lib")
            return(
                soup.find(
                    'h3', string="Visit Website"
                    ).next_sibling.next_sibling.get('href'))
        except Exception:
            return('unknown link')

    def getUniMajors(self, html) -> str:
        # retrieve majors
        #
        try:
            return(
                html.findNext('td').findNext('td').findNext('td').text
                )
        except Exception:
            return('unknown majors')
