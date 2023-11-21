from Anime import Anime
from validators import validator
from db import db
import pymongo


class AnimeCollection:
    def __init__(self):
        self.database = db.AnimeCollection
        self.tracked = self.get_tracked()
        self.collection = self.get_collection()
        self.anime_list_tracked = self.get_anime_list_from_tracked()
        self.anime_list_database = self.get_anime_list_from_database()
        self.sync_database()


    def get_collection(self):
        try:
            return self.database.anime.find()
        except Exception as e:
            print(type(e))
            return []

    def get_tracked(self):
        tracked = open("tracked.txt", 'r')
        tracking_list = []
        for line in tracked.readlines():
            tracking_list.append(line.strip())
        tracked.close()
        return tracking_list

    def add_tracked(self, url):
        tracked = open('tracked.txt', 'a')
        tracked.write(url+'\n')
        tracked.close()
        self.anime_list_tracked.append(Anime(url))

    def get_anime_list_from_tracked(self):
        anime_list_tracked = []
        for url in self.tracked:
            anime_list_tracked.append(Anime(url))
        return anime_list_tracked

    def get_anime_list_from_database(self):
        anime_list_database = []
        for anime in self.get_collection():
            anime_list_database.append(Anime(anime))
        return anime_list_database

    def set_validator(self):
        self.database.create_collection("anime", **validator)
        self.database.anime.create_index([('name', pymongo.ASCENDING)], unique=True)

    def insert_anime(self, anime):
        try:
            self.database.anime.insert_one(anime.dictionary())
            print(f"{anime.name} added to database")
            return True
        except Exception as e:
            print(f"{anime.name} failed to add")
            print(f"Error Type: {type(e)}")
            return False

    def anime_set_current_episode(self, anime, new_current):
        anime.current_episode = new_current
        self.database.anime.update_one(anime.query(), {'$set': {'current_episode': new_current}})

    def anime_update_episodes(self, anime):
        episode_list = []
        for ep in anime.episodes:
            episode_list.append(ep.dictionary())
        self.database.anime.update_one(anime.query(), {'$set': {'episodes': episode_list}})

    def sync_database(self):
        for anime1 in self.anime_list_tracked:
            found = False
            for anime2 in self.anime_list_database:
                if anime1 == anime2:
                    found = True
                    if len(anime1.episodes) > len(anime2.episodes):
                        self.anime_update_episodes(anime1)
            if not found:
                self.insert_anime(anime1)
        self.anime_list_database = self.get_anime_list_from_database()
