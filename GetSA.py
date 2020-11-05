import requests
import os
from BaseGetUniDatabase import BaseGetUniDatabase
from bs4 import BeautifulSoup
import re
import pandas

class GetSA(BaseGetUniDatabase):

    # Use a link to a html file with search results to create an instance
    def __init__(self, path):
        self.path = path # path to folder with html files with search results
        self.links=[]     # links for universities at WHED website
        self.soups=[] # extracted table rows with university profile

    def updateLinks(self):
        # retrieves ids of all the universities in the html file
        for filename in os.listdir(self.path):
            with open(os.path.join(self.path, filename), 'r') as f: # open in readonly mode
                # do your stuff
                contents = f.read()

            soup = BeautifulSoup(contents, 'lxml')

            for uni in soup.find_all(['ul','tbody']):
                # retrieve uni profiles on MoE website
                self.soups.extend(uni.find_all('tr'))

                links = uni.find_all('li')
                for link in links:
                    self.links.append('https://www.moe.gov.sa/' + link.a.get('href'))

    def getData(self) -> list:
        # rerieves all the data about each university in the html file
        data = []
        for id in range(len(self.links)):
            data.append(self.getSingleUniDataFromUrl(id))

        for soup in self.soups:
            data.append(self.getSingleUniDataFromSoup(soup))


        return(data)

    def getSingleUniDataFromUrl(self, id) -> tuple:
        # return a turple with a university information
        resp = requests.get(self.links[id])
        soup=BeautifulSoup(resp.text, "html5lib").find(id="ReadSpeakerDiv")

        name = self.getUniName(soup)
        country = 'Saudi Arabia'
        funding = 'Public'
        website = self.getUniWebsite(soup)
        majors = self.getUniMajors(soup)
        return(name, country, funding, website, majors)

    def getSingleUniDataFromSoup(self, soup) -> tuple:
        # return a turple with a university information
        tds = soup.find_all('td')
        name = tds[1].text
        country = 'Saudi Arabia'
        funding = 'Private'
        website = "uknown website"
        if len(tds) == 4:
            majors = tds[3].text
        else:
            majors = tds[4].text

        return(name, country, funding, website, majors.lower())

    def getUniName(self, soup) -> str:
        # retrieve uni name
        try:
            return(" ".join(soup.h1.text.split())) # remove non-breaking spaces
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
            return(soup.a.get('href'))
        except Exception:
            return('unknown link')

    def getUniMajors(self, soup) -> str:
        # retrieve majors
        #
        try:
            pattern = re.compile(
                (r'('
                 r'(?<=[Ff]aculty\sof\s)([A-Z]\w*)'
                 r'|'
                 r'(?<=[Cc]ollege\sof\s)([A-Z]\w*)'
                 r')'
                 r'(\sand\s)?([A-Z]\w*)?(\s[A-Z]\w*)*'), re.VERBOSE)

            soup = soup.encode("utf-8").decode('utf-8')
            majors = re.findall(pattern, soup)

            return(set([''.join(major).lower() for major in majors]))

        except Exception:
            return('unknown majors')
