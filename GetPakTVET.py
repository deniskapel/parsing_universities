from BaseGetUniDatabase import BaseGetUniDatabase
from bs4 import BeautifulSoup

class GetPakTVET(BaseGetUniDatabase):

    # Use a link to a html file with search results to create an instance
    def __init__(self, path):
        self.path = path # path to folder with html files with search results
        self.links=[]     # links for universities at WHED website
        self.country='Pakistan'

    def updateLinks(self):
        # retrieves ids of all the universities in the html file
        pass

    def getData(self) -> list:
        # rerieves all the data about each university in the html file
        with open(self.path, 'r') as f: # open in readonly mode
            # do your stuff
            contents = f.read()

        soup = BeautifulSoup(contents, 'lxml')
        data = []
        for row in soup.find_all('tr'):
            if row.text[0] != '\xa0':
                data.append(self.getSingleOrgData(row))
            else:
                # pass
                data[-1][-1] += (", " + self.getOrgMajors(row)) # join other majors
            # data.extend(tmp)
        return(data)

    def getSingleOrgData(self, html) -> tuple:
        # return a turple with a university information
        name = self.getOrgName(html.td.next_sibling)
        country = self.getOrgCountry()
        funding = self.getFunding()
        website = self.getOrgWebsite()
        major =  self.getOrgMajors(html)

        return([country, name, funding, website, major])

    def getOrgName(self, html) -> str:
        # retrieve uni name
        return(html.text)

    def getFunding(self) -> str:
        # retrieve uni type of funding
        return(None)

    def getOrgCountry(self) -> str:
        # retrieve uni country
        return(self.country)

    def getOrgWebsite(self) -> str:
        # retrieve uni website
        return(None)

    def getOrgMajors(self, html) -> str:
        # retrieve majors
        return(html.find_all('td')[4].text)
