import bs4 as bs
from urllib.request import urlopen
from Episode import Episode

class Anime:
    
    def __init__(self, source):
        if type(source) == type(""):
            self.url = source
            self.name = self.get_name()
            self.current_episode = 1
            self.get_episodes()
        elif type(source) == type(dict()):
            self.url = source['url']
            self.name = source['name']
            self.current_episode = source['current_episode']
            self.episodes = []
            for ep in source['episodes']:
                self.episodes.append(Episode(ep['url'], self))
            

    def get_name(self):
        req = urlopen(self.url)
        soup = bs.BeautifulSoup(req.read(), features="html.parser")
        return soup.find('div', {'class': "infotitle c"}).text

    def get_episodes(self):
        self.episodes = []
        req = urlopen(self.url)
        soup = bs.BeautifulSoup(req.read(), features="html.parser")
        div = soup.find('div', {'class': "linetitle2 c2"})
        episode_links = div.find_all('a')
        episode_links.reverse()
        for link in episode_links:
            self.episodes.append(Episode(link.get('href'), self))

        
    def get_next_episode(self):
        return len(self.episodes)+1

    def dictionary(self):
        episode_dictionaries = []
        for ep in self.episodes:
            episode_dictionaries.append(ep.dictionary())
        return {'name': self.name, 'url': self.url, 'current_episode': self.current_episode, 'episodes': episode_dictionaries}

    def __eq__(self, other):
        return self.name == other.name

    def query(self):
        return {'name': self.name}
