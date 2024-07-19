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


def find_playlist_ids():
    """
    Gets the IDs of all user's playlists
    :return: List of playlist IDs
    """
    all_playlists = sp.user_playlists(USER_NAME)
    playlist_ids = []
    while all_playlists:
        for playlist in all_playlists['items']:
            playlist_ids.append(playlist['id'])
        if all_playlists['next']:
            all_playlists = sp.next(all_playlists)
        else:
            all_playlists = None
    return playlist_ids


def gather_playlists():
    """
    Gathers all of a user's playlists in a dictionary of playlist details and dictionary of song details
    Uses function "find_playlist_ids()" to get a list of playlist IDs.
    :return: A dictionary of playlist id, title, and dictionary of song details
    """
    playlist_ids = find_playlist_ids()
    playlist_items = []
    for pl_id in playlist_ids:
        pl_dict = {
            'id': pl_id,
            'title': sp.playlist(pl_id)['name']
        }

        print(sp.playlist(pl_id)['name'])  # TEST

        playlist = sp.playlist_items(pl_id)['items']
        if not playlist:    # skip empty playlists
            continue
        songs_list = []  # now get details for every song and add to list
        for item in playlist:
            song_dict = {}
            if not item['track']:   # skip local songs
                continue
            song_id = item['track']['id']
            song_dict['id'] = song_id
            if song_id is None:
                continue
            song_dict['title'] = sp.track(song_id)['name']
            songs_list.append(song_dict)
        pl_dict['songs'] = songs_list
        playlist_items.append(pl_dict)
    return playlist_items


def save_pl_dict(pl_dict):
    """
    Saves dictionary of playlist IDs and song IDs to a json file for easy access
    :param pl_dict: Dictionary of playlists
    """
    with open('playlist_data.json', 'w') as outfile:
        json.dump(pl_dict, outfile)
    print('Playlists saved.')


def read_pl_dict():
    """
    Loads in an existing playlist dictionary json file
    :return: Dictionary loaded from json file
    """
    with open('playlist_data.json', 'r') as infile:
        print('Playlists loaded.')
        return json.load(infile)


def search_for_song(pl_dict, song_id):
    """
    Searches for user's playlists containing a specific song.
    :param pl_dict: Dictionary of the IDs of the playlists with lists of the songs' IDs
    :param song_id: ID as a string of the song to search for
    :return: Dictionary of playlist ID and name of any playlists containing the song.
             Returns False if no playlists are found.
    """
    included_pl = {}
    for playlist in pl_dict:
        for song in playlist['songs']:
            if song['id'] == song_id:
                included_pl[playlist['id']] = playlist['title']
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
    # ONLY RUN THIS PART WHEN YOU NEED TO REWRITE THE PLAYLIST DATA
    print('Gathering playlists...\n')
    playlists = gather_playlists()
    print('Playlists gathered!\n')
    # SAVE PLAYLIST DICT
    save_pl_dict(playlists)

    # OTHERWISE READ PLAYLIST DICT
    # playlists = read_pl_dict()

    end = ''
    while end != 'q':
        song_info = extract_song()
        results = search_for_song(playlists, song_info[0])
        if results is not False:
            print(f'The song "{song_info[1]}" is on these playlists:')
            for i in results:
                print("   ", results[i])
        else:
            print(f'The song "{song_info[1]}" is not in any of the playlists.')
        end = input('\nPress q to quit or any other key to continue: ')
        print()

    print('Done!')
