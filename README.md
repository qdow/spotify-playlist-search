# Spotify Playlist Search

## Table of Contents
1. [Introduction](#introduction)
2. [Usage](#usage)
3. [Planned Features](#planned-features)
4. [Recent Updates](#recent-updates)

## Introduction
This program allows you to find out which of your playlists (if any) contains a specific song.


## Usage
You must first create a .env file with your own Spotify client ID and secret, which you can generate on the Spotify developer dashboard [here](https://developer.spotify.com/dashboard/applications).<br>
In addition to `CLIENT_ID` and `CLIENT_SECRET` in the .env file, create a variable called `USER_NAME` with a string containing your Spotify username.

Right now, the way to search is to add the desired song's URI as a command line argument when running the file.<br>
Example: `python main.py 7th29u6DX01vM4KJlIBr1T` <br>
To learn how to find the URI of a song, [look here](https://community.spotify.com/t5/FAQs/Basics-of-a-Spotify-URL/ta-p/919201).<br>
One limitation is that only the Spotify profile's public playlists can be searched. 
You can search private playlists if you find the playlist's URI, however, that is not a feature of this program.

## Planned Features
- Searching using the full song's URL (so you don't have to manually extract the URI)
- A nicer results printout
- Code cleanup (not really a feature, but it needs to be done)

## Recent Updates
Last updated 12 Jul 2024
- Committed first rough working draft
