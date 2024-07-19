# Spotify Playlist Search

## Table of Contents
1. [Introduction](#introduction)
2. [Usage](#usage)
3. [Planned Features](#planned-features)
4. [Recent Updates](#recent-updates)

## Introduction
This program uses the *[Spotipy](https://spotipy.readthedocs.io/en/2.24.0/)* Python library to
allow you to find out which of your playlists (if any) contains a specific song.


## Usage
***PLEASE NOTE:*** If you have a lot of playlists, it may take a while for the program gather them all up before it's ready to search them.
I have over 250+ playlists on my account (which is why I wanted to create this tool in the first place) and it takes a few minutes to finish gathering them. Please be patient.<br>

You must first create a .env file with your own Spotify client ID and secret, which you can generate on the Spotify developer dashboard [here](https://developer.spotify.com/dashboard/applications).<br>
In addition to `CLIENT_ID` and `CLIENT_SECRET` in the .env file, create a variable called `USER_NAME` with a string containing your Spotify username.

Run the program with: `python main.py` in the directory which contains the main.py file.<br>
When the program asks for the URL of the song you would like to search for, 
you can find the song's url by going to Spotify, right clicking on the desired song, choosing 'Share', then 'Copy Song Link'.<br>

The first time you run the program, it will grab all your playlists from Spotify and save the data in a json file called `playlist_data.json`.
Unless you add or update playlists, you will want to comment out the code for getting your playlists from Spotify and instead load the playlist data file so it is faster.
Comments in the code instruct which lines will be needed for what purpose.

This program searches both your public and private playlists. 

## Planned Features and Updates
- Implementing error handling for incorrect URLs. Right now, the program expects a correct song URL
- Searching only playlists created by user (exclude playlists by other authors)

## Recent Updates
Last updated 14 Jul 2024
- Changed the structure of the playlist dictionary
- Added ability to save your playlist data as a json file to easily load up so you don't have to gather them from Spotify every single time

13 Jul 2024
- Made it so instead of running the program with the song ID as a command line argument, the program prompts the user for the song URL while running
- Which also allowed for the ability to continue searching for additional songs without needing to rerun the program
- Added ability to search using the full song's URL (so you don't have to manually extract the ID)
- Separated gathering playlists and searching playlists into separate functions to reduce the need to regather playlists
- Added support for private playlists and fixed related bugs

12 Jul 2024
- Committed first rough working draft
