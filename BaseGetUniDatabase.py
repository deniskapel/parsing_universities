from abc import ABC, abstractmethod

class BaseGetUniDatabase(ABC):
    ''' Basic Class to download lists of universities from certain websites.
    '''
    def __init__(self):
        self.path = path # path to html file or a link to a database
        self.links=[] # links to a single university on A database website

    # updates self.links with links to single universities on a database website
    @abstractmethod
    def updateLinks(self):
        pass

    # Retrieves data from self.links about each university
    @abstractmethod
    def getData(self) -> list:
        pass
