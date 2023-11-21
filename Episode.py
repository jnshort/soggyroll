class Episode:
    def __init__(self, source, anime):
        self.name = anime.name
        self.episode_number = anime.get_next_episode()
        if source.startswith("https://animeheaven.me/"):
            self.url = source
        else:
            self.url = "https://animeheaven.me/" + source

    def query(self):
        return {'name': self.name, 'episode_number': self.episode_number}

    def dictionary(self):
        return {'name': self.name, 'episode_number': self.episode_number, 'url': self.url}

