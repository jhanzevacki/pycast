# Pycast README

### Description

Pycast is a script created for managing podcast subscriptions, downloading and copying podcast episodes.

### Reason for writing Pycast

This is my first atempt at writing some code after learning the basics of Python on Codecademy and finishing my first project. I had fun making this and are even more excited to learn new things and maybe improve this simple script on the way. I hope that this is readable since english is not my first language.

I wanted an easy way to download podcasts and copy them to my mp3 player which I use when exercising. Couple of years ago I used an iPod nano which I loved because of its small dimensions, light weight and to me the best feature, a clip on the backside. Since they went out of production and are somewhat replaced by smartphones which are for me too big and heavy when running, I use cheap Sony mp3 player which gets the job done but lacks the software like iTunes for easy downloading and syncing.

### Running Pycast

#### 1. To run Pycast first open script Pycast.py in text editor and set "downloads_directory_path" (line 4) variable to your podcast downloads directory. Now you are redy to run the script. 

#### 2. Start Pycast by running:

    python3 -i Pycast.py

#### 3. To subscribe to a new podcast run:

    Podcast("podcast_name", "RSS_feed_link")

#### 4. After subscribing run:

    update() --> to update all subscriptions or run:

    podcast_name.up() --> to update just this one podcast

#### 5. To see latest episodes run:

    podcast_name.ep() --> by default it will show last 10 episodes but you can specify the number by entering it as method argument eg. (podcast_name.ep(4) will show last 4 episodes)

#### 6. To download episode/episodes run:

    podcast_name.dl() --> downloads latest episode

    podcast_name.dl([6]) --> downloads episode 6

    podcast_name.dl([7, 2, 5, 16]) --> downloads episodes 7, 2, 5, 16

    podcast_name.dl("a") --> downloads all episodes

#### 7. To copy downloaded episodes to another directory (device) run:

    sync2("path_to_the_directory_you_wnat_to_copy_podcasts_to")
    

### How to unsubscribe or edit subscriptions

Navigate to your podcast download directory and open hidden file named ".subscriptions.csv". To unsubscribe simply remove the line containing podcast name and RSS link or edit them if you need to.
