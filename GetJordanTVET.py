import requests
import re
from BaseGetUniDatabase import BaseGetUniDatabase
from bs4 import BeautifulSoup


class GetJordanTVET(BaseGetUniDatabase):

    # Use a link to a html file with search results to create an instance
    def __init__(self, path):
        self.path = path # path to folder with html files with search results
        self.links=[]     # links for universities at WHED website
        self.country='Jordan'
        self.funding='Public'
        self.orgs = []

    def updateLinks(self):
        # retrieves ids of all the universities in the html file
        with open(self.path, 'r') as f: # open in readonly mode
            # do your stuff
            contents = f.read()

        soup = BeautifulSoup(contents, 'lxml')
        for org in soup.find_all('li'):
            self.links.append(org.a.get('href'))
            self.orgs.append(org.a.text)

    def getData(self) -> list:
        # rerieves all the data about each university in the html file
        data = []
        for i in range(len(self.links)):
            resp = requests.get(self.links[i])
            soup = BeautifulSoup(resp.text, 'lxml')
            data.append(self.getSingleOrgData(i, soup))

        return(data)

    def getSingleOrgData(self, id, html) -> tuple:
        # return a turple with a university information
        name = self.getOrgName(id)
        country = self.getOrgCountry()
        funding = self.getFunding()
        website = self.getOrgWebsite(html)
        major =  self.getOrgMajors()

        return(country, name, funding, website, major)

    def getOrgName(self, id) -> str:
        # retrieve uni name
        return(self.orgs[id])

    def getFunding(self) -> str:
        # retrieve uni type of funding
        return(self.funding)

    def getOrgCountry(self) -> str:
        # retrieve uni country
        return(self.country)

    def getOrgWebsite(self, html) -> str:
        # retrieve uni website
        try:
            return(html.find('div', string=re.compile('E-mail')).text)
        except Exception:
            return(None)


    def getOrgMajors(self) -> str:
        # retrieve majors
        return(None)
