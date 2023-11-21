from AnimeCollection import AnimeCollection
from urllib.request import urlopen
import webbrowser
import bs4 as bs


def main_menu(coll):
    print("*" * 50)
    print("\t\tMain Menu")
    print("1) Add new anime")
    print("2) Anime Collection")
    print("3) Exit")
    
    inp = input("Enter choice: ")

    match inp:
        case "1":
            add_anime(coll)
            return True
        case "2":
            anime = select_anime(coll)
            watching = True
            while watching:
                watching = anime_menu(coll, anime)
            return True
        case _:
            return False


def anime_menu(coll, anime):
    print("Selected: " + anime.name)
    print(f"1) Watch next ({anime.current_episode})")
    print("2) Update next episode")
    print("3) Exit")
    action = input("Enter choice: ")
    match action:
        case "1":
            try:
                episode = anime.episodes[anime.current_episode-1]  
                coll.anime_set_current_episode(anime, anime.current_episode + 1)
                webbrowser.open_new(episode.url)
            except IndexError:
                print("Episode not out yet")
                print(f"Opening episode list for: {anime.url}")
                webbrowser.open_new(anime.url)


            return True
        case "2":
            max = len(anime.episodes)
            valid = False
            while not valid:
                print(f"There are currently {max} episodes")
                new_ep = input("Enter episode number: ")
                if new_ep.isalnum():
                    if int(new_ep) in range(max+1):
                        coll.anime_set_current_episode(anime, int(new_ep))
                        valid = True
            return True
        case _:
            return False


def add_anime(coll):
    print("*" * 50)
    adding = True
    while adding:
        print("Adding new anime")
        url = input("Enter url: ")
        coll.add_tracked(url)
        choice = input("Would you like to add another? (y/n)")
        match choice.upper():
            case "Y":
                pass
            case _:
                adding = False


def select_anime(coll):
    print("*" * 50)
    print("Select an anime")
    i = 0
    for anime in coll.anime_list_database:
        i += 1
        print(f"{i}) {anime.name}")
    choice = ""
    valid = False
    while not valid:
        choice = input("Enter choice: ")
        if choice.isalnum():
            if int(choice) in range(len(coll.anime_list_database)+1):
                valid = True
    return coll.anime_list_database[int(choice)-1]


def main():
    coll = AnimeCollection()
    active = True
    while active:
        active = main_menu(coll)

main()
