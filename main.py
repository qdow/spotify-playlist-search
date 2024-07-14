#!/usr/bin/env python3
"""
Filename: main.py
Author: qdow
Date updated: 2024-07-13
Description: Searches a user's playlists for a specific song and lists which playlists contain the song
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from decouple import config


CLIENT_ID = config('CLIENT_ID')
CLIENT_SECRET = config('CLIENT_SECRET')
USER_NAME = config('USER_NAME')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://localhost:1234/",
                                               scope="user-library-read playlist-read-private"))


def gather_playlists():
    """
    Gathers all of a user's playlists in a dictionary of playlist IDs and song IDs
    :return: A dictionary by ID of playlists and lists of song IDs in each playlist
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
    return playlist_items


def search_for_song(pl_dict, song_id):
    """
    Searches for user's playlists containing a specific song.
    :param pl_dict: Dictionary of the IDs of the playlists with lists of the songs' IDs
    :param song_id: ID as a string of the song to search for
    :return: Dictionary of playlist ID and name of any playlists containing the song.
             Returns False if no playlists are found.
    """
    included_pl = {}
    for pl_id in pl_dict:
        if song_id in pl_dict[pl_id]:
            included_pl[pl_id] = (sp.playlist(pl_id)['name'])
    if included_pl == {}:
        return False
    else:
        return included_pl


def extract_song():
    """
    Takes the url of a song on Spotify and gets the song's ID and title
    Assumes url is in this format:
        https://open.spotify.com/track/33i4H7iDxIes1d8Nd0S3QF?si=qvCA_Jv0QjiN8-2hXL5h5Q
    :return: Tuple with song ID and song title
    """
    url = input('Enter the URL of the song to search for: ')
    print()
    song_id = url[31:53]
    title = sp.track(song_id)['name']
    return song_id, title


if __name__ == '__main__':
    print('Gathering playlists...\n')
    playlists = gather_playlists()
    print('Playlists gathered!\n')
    end = ''
    while end != 'q':
        song_info = extract_song()
        results = search_for_song(playlists, song_info[0])
        if results is not False:
            print(f'The song "{song_info[1]}" is on these playlists:')
            for i in results:
                print("   ", results[i])
        else:
            print("Song is not in any of user's playlists.")
        end = input('\nPress q to quit or any other key to continue: ')
        print()
    print('Done!')
