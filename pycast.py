import os, csv, feedparser, requests, shutil
from typing import ClassVar


# Set the download directory path:
download_directory_path = "SET_YOUR_DOWNLOADS_PATH"

# Subscriptions file path:
subscriptions_file_path = "{}/.subscriptions.csv".format(download_directory_path)

# Functions:

# Function checks if file ".subscriptions.csv" exists in downloads directory and if the file dosen't exist it creates it.
def create_subscriptions_file():
    if ".subscriptions.csv" not in os.listdir(download_directory_path):
        with open(subscriptions_file_path, "w") as subscriptions_file:
            field_names = ["podcast_name", "rss_link"]
            writer = csv.DictWriter(subscriptions_file, fieldnames=field_names)
            writer.writeheader()
    return

# Function ads podcast name and coresponding rss_link to subscriptions file
def add_subscription(podcast_name, rss_link):
    podcast_names_list = []
    with open(subscriptions_file_path) as subscriptions_file:
        reader = csv.DictReader(subscriptions_file)
        for row in reader:
            podcast_names_list.append(row["podcast_name"])
    if podcast_name not in podcast_names_list:
        with open(subscriptions_file_path, "a") as subscriptions_file:
            field_names = ["podcast_name", "rss_link"]
            writer = csv.DictWriter(subscriptions_file, fieldnames=field_names)
            writer.writerow({"podcast_name": podcast_name, "rss_link": rss_link})
        print()
    return

# Creates the podcast directory and hidden ".episodes.csv" file if they dont exist:
def create_podcast_files(podcast_name, podcast_path):
    if podcast_name not in os.listdir(download_directory_path):
        os.mkdir(podcast_path)
    if ".episodes.csv" not in os.listdir(podcast_path):
        with open("{}/.episodes.csv".format(podcast_path), "w") as episodes_file:
            field_names = ["publishing_date", "episode_name", "download_link"]
            writer = csv.DictWriter(episodes_file, fieldnames=field_names)
            writer.writeheader()
    return

# Function takes RSS link as an argument, downloads the RSS file and using feedparser library converts the file into the form of dictionary containing dictionaries from which we take the necessary data and append it to a list in the form of ["episode_name", "publishing_date", "download_link"], ...,] for all episodes. This list gets returned by the function
def parse_rss_data(rss_link):
    data_list = []
    rss_data = feedparser.parse(rss_link)
    for i in range(len(rss_data.entries)):
        lst = []
        try:
            lst.append(rss_data.entries[i].published[:17])
        except IndexError:
            continue
        try:
            lst.append(rss_data.entries[i].title)
        except IndexError:
            continue
        try:
            lst.append(rss_data.entries[i].links[1]['href'])
        except IndexError:
            continue
        data_list.append(lst)
    return data_list

# Update names
def update_names():
    with open(subscriptions_file_path) as subscriptions_file:
        reader = csv.DictReader(subscriptions_file)
        for row in reader:
            globals()[row["podcast_name"]] = Podcast(row["podcast_name"], row["rss_link"])
    return

# Function takes the return of parse_rss_data() function and updates the hidden ".episodes.csv file in coresponding download directory"
def update_episodes(data_list, podcast_path):
    with open("{}/.episodes.csv".format(podcast_path), "w") as episodes_file:
        field_names = ["publishing_date", "episode_name", "download_link"]
        writer = csv.DictWriter(episodes_file, fieldnames=field_names)
        writer.writeheader()
        for entrie in data_list:
            writer.writerow({"publishing_date": entrie[0], "episode_name": entrie[1], "download_link": entrie[2]})
    return

# Function updates all podcasts
def update():
    print("\n Updating ...")
    with open(subscriptions_file_path) as subscriptions_file:
        reader = csv.DictReader(subscriptions_file)
        for row in reader:
            row["podcast_name"] = Podcast(row["podcast_name"], row["rss_link"]).up()
    update_names()
    print("\n Update complete\n")
    return

# Print episodes from episodes file
def print_episodes(podcast_name, podcast_path, number_of_episodes):
    print("\n  {} episodes:\n\n".format(podcast_name))
    episodes_list = []
    with open("{}/.episodes.csv".format(podcast_path)) as episodes_file:
        reader = csv.DictReader(episodes_file)
        for row in reader:
            episodes_list.append([row["publishing_date"], row["episode_name"]])
    for i in range(1, number_of_episodes + 1):
        print(" {}. [{}] - {}\n".format(i, episodes_list[i - 1][0], episodes_list[i-1][1]))
    return

# Function takes episodes path and returns a list in the form [[episode_name, download_link], ...] for all episodes.
def download_list(episodes_path):
    download_list = []
    with open("{}/.episodes.csv".format(episodes_path)) as episodes_file:
        reader = csv.DictReader(episodes_file)
        for row in reader:
            download_list.append([row["episode_name"], row["download_link"]])
    return download_list

# Function takes episodes list in the form [[episode_name, download_link], ...] for all episodes that are in coresponding ".episodes.csv file and downloads them in coresponding directory.
def download(episodes_list, episodes_to_download, download_path):
    print("\n Downloading ...")
    if episodes_to_download == "a":
        episodes_to_download = [i + 1 for i in range(len(episodes_list))]
    for episode in episodes_to_download:
        episode -= 1
        download_file = requests.get(episodes_list[episode][1])
        with open("{}/{}.mp3".format(download_path, episodes_list[episode][0]), "wb") as file:
            file.write(download_file.content)
    print("\n Download complete\n")
    return

# Function takes copy destination path and there creates podcast directory to which all of the podcasts from download directory are copied to.
def sync2(sync2_directory):
    if "PODCASTS" not in os.listdir(sync2_directory):
        os.mkdir("{}/PODCASTS".format(sync2_directory))
    print("\n Syncing ...\n")
    shutil.copytree(download_directory_path, "{}/PODCASTS".format(sync2_directory), copy_function=shutil.copy2, dirs_exist_ok=True)
    print(" Sync complete\n")
    return

# Function prints the script startp text
def print_opening():
    print(("--" * 40).center(80))
    print("Pycast".center(80))
    print(("--" * 40).center(80))
    print()

# Classes:

class Podcast:

    def __init__(self, name, rss_link):
        self.name = name
        self.rss_link = rss_link
        self.path = "{}/{}".format(download_directory_path, self.name)
        add_subscription(self.name, self.rss_link)
        create_podcast_files(self.name, self.path)
    
    def __str__(self) -> str:
        return "\nSubscribed to {} podcast\n".format(self.name)

    def __repr__(self) -> str:
        return self.__str__()

    def up(self):
        """Method updates podcast episodes"""
        update_episodes(parse_rss_data(self.rss_link), self.path)

    def ep(self, number_of_episodes=5):
        """Print episodes list by default 5 but can be specified by entering number as argument"""
        print_episodes(self.name, self.path, number_of_episodes)

    def dl(self, episodes_to_download=[1]):
        """Method takes list of episode numbers as argument and downloads them. By default without argument latest episode is downloaded"""
        download(download_list(self.path), episodes_to_download, self.path)


# Start script:

print_opening()
create_subscriptions_file()
update_names()
