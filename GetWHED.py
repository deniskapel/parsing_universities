import requests
from BaseGetUniDatabase import BaseGetUniDatabase
from bs4 import BeautifulSoup
import os

class GetWHED(BaseGetUniDatabase):

    # Use a link to a html file with search results to create an instance
    def __init__(self, path):
        self.path = path # path to folder with html files with search results
        self.links=[]     # links for universities at WHED website

    def updateLinks(self):
        # retrieves ids of all the universities in the html file
        for filename in os.listdir(self.path):
            with open(os.path.join(self.path, filename), 'r') as f: # open in readonly mode
                # do your stuff
                contents = f.read()

            soup = BeautifulSoup(contents, 'lxml')

            for uni in soup.find_all('li'):
                # retrieve id
                self.links.append('https://www.whed.net/' + uni.h3.a.get('href'))

    def getData(self) -> list:
        # rerieves all the data about each university in the html file
        data = []
        for id in range(len(self.links)):
            data.append(self.getSingleUniData(id))

        return(data)

    def getSingleUniData(self, id) -> tuple:
        # return a turple with a university information
        resp = requests.get(self.links[id])
        soup=BeautifulSoup(resp.text, "html5lib")

        name = self.getUniName(soup)
        country = self.getUniCountry(soup)
        funding = self.getFunding(soup)
        website = self.getUniWebsite(soup)
        majors = self.getUniMajors(soup)
        return(name, country, funding, website, majors)


    def getUniName(self, soup) -> str:
        # retrieve uni name
        try:
            return(' '.join(soup.find(class_='detail_right').text.split()))
        except Exception:
            return('unknown UniName')

    def getFunding(self, soup) -> str:
        # retrieve uni type of funding
        try:
            return(" ".join(soup.find(
                             'span', class_='dt', string='Institution Funding'
                             ).next_sibling.next_sibling.get_text().split())
                   )
        except Exception:
            return('No funding data')

    def getUniCountry(self, soup) -> str:
        # retrieve uni country
        try:
            return(soup.find(class_="country").text)
        except Exception:
            return('unknown Country')


    def getUniWebsite(self, soup) -> str:
        # retrieve uni website
        try:
            return(soup.find(class_="lien").text)
        except Exception:
            return('unknown link')

    def getUniMajors(self, soup) -> str:
        # retrieve majors
        #
        try:
            elems = soup.find_all('span', class_='libelle', string='Fields of study:')

            majors = []
            for elem in elems:
                majors.extend(elem.next_sibling.text.split(', '))

            return(set(majors))
        except Exception:
            return('unknown majors')
