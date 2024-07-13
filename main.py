#!/usr/bin/env python3
"""
Filename: main.py
Author: qdow
Date updated: 2024-07-13
Description: Searches a user's playlists for a specific song and lists which playlists contain the song

NOTE:
        this is currently the rough draft first working version
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from decouple import config
import sys


CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
USER_NAME = config('USER_NAME')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://localhost:1234/",
                                               scope="user-library-read playlist-read-private"))


def search_playlists(song_uri):
    """
    Searches all of a user's playlists for a specific song
    :param song_uri: The URI as a command line argument of the song to search for
    :return: A dictionary by ID and title of the playlists which contain the song searched for
    """
    # get all users playlists
    all_playlists = sp.user_playlists(USER_NAME)
    playlist_ids = []
    while all_playlists:
        for playlist in all_playlists['items']:
            playlist_ids.append(playlist['id'])
        if all_playlists['next']:
            all_playlists = sp.next(all_playlists)
        else:
            all_playlists = None

    # create dictionary of playlist ids and lists of song ids
    playlist_items = {}
    for pl_id in playlist_ids:
        playlist = sp.playlist_items(pl_id)['items']
        if not playlist:    # skip empty playlists
            continue
        song_ids = []
        for item in playlist:
            if not item['track']:   # skip local songs
                continue
            song_ids.append(item['track']['id'])
        playlist_items[pl_id] = song_ids

    included_pl = {}
    for pl_id in playlist_items:
        if song_uri in playlist_items[pl_id]:
            included_pl[pl_id] = (sp.playlist(pl_id)['name'])
    if included_pl == {}:
        return False
    else:
        return included_pl


if __name__ == '__main__':
    results = search_playlists(sys.argv[1])
    if results is not False:
        for i in results:
            print(results[i])
    else:
        print('None')
