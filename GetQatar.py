import os
import time
import requests
from BaseGetUniDatabase import BaseGetUniDatabase
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select

class GetQatar(BaseGetUniDatabase):

    # Use a link to a html file with search results to create an instance
    def __init__(self, url):
        self.path = url # path to folder with html files with search results
        self.country = 'Qatar'
        self.public = ['Community College of Qatar',
                       'Doha Institute for Graduate Studies',
                       'Hamad Bin Khalifa University',
                       'Qatar University']

    def updateLinks(self):
        pass
        # retrieves ids of all the universities in the html file


    def getData(self) -> list:
        # rerieves all the data about each university from url
        # self.browser.get(self.path)
        data = []
        resp = requests.get(self.path)
        soup = BeautifulSoup((resp.text).encode('ascii', 'ignore'),
                             "html5lib")

        for tr in soup.find_all('tr')[1:]: # ingore the table heading row
            data.append(self.getSingleUniData(tr))

        return(data)

    def getSingleUniData(self, html) -> tuple:
        # return a turple with a university information
        name = self.getUniName(html.a)
        country = self.getUniCountry()
        funding = self.getFunding(name)
        website = self.getUniWebsite(html.a)

        return(country, name, funding, website)

    def getUniName(self, html) -> str:
        # retrieve uni name
        return(" ".join(html.text.split()))

    def getFunding(self, name) -> str:
        # retrieve uni type of funding
        if name not in self.public:
            return('Private')
        else:
            return('Public')

    def getUniCountry(self) -> str:
        # retrieve uni country
        return(self.country)

    def getUniWebsite(self, html) -> str:
        # retrieve uni website
        return(html.get('href'))
