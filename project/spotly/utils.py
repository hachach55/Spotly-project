import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

from .models import TrackModel, DetailedPlaylistModel


def get_all_saved_tracks(limit_step=50):
    user = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='8fffefe586fa4711ae28c0f0ea3c5084',
                                                     client_secret='classified',
                                                     redirect_uri="http://localhost:8080",
                                                     scope='user-library-read'))
    tracks = list()
    count = 0
    for offset in range(0, 100000000, limit_step):
        response = user.current_user_saved_tracks(limit=limit_step,
                                                  offset=offset)

        if len(response['items']) == 0:
            break
        for track in response['items']:
            count += 1
            added_at = datetime.strptime(track['added_at'], '%Y-%m-%dT%H:%M:%SZ')
            formatted_date = added_at.strftime('%d-%B-%Y, %H:%M')
            new_track = TrackModel(id=count,
                                   title=track['track']['name'],
                                   artist=track['track']['artists'][0]['name'],
                                   album=track['track']['album']['name'],
                                   added=formatted_date)

            new_track.save()
            tracks.append(new_track)
            print(f"finished fetching {count} tracks")

    # print(f"You have {count} saved songs!")
    return tracks


def get_saved_tracks_grouped_by_artist(limit_step=50):
    saved_tracks = get_all_saved_tracks()
    grouped_tracks = {}

    for track in saved_tracks:
        if track.artist not in grouped_tracks:
            grouped_tracks[track.artist] = list()
        grouped_tracks[track.artist].append(track)

    return grouped_tracks


def get_saved_tracks_grouped_by_album(limit_step=50):
    saved_tracks = get_all_saved_tracks()
    grouped_tracks = {}

    for track in saved_tracks:
        if track.album not in grouped_tracks:
            grouped_tracks[track.album] = list()
        grouped_tracks[track.album].append(track)

    return grouped_tracks


def get_user_playlists(limit_step=50, public_only=True):
    user = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='8fffefe586fa4711ae28c0f0ea3c5084',
                                                     client_secret='10a514b5df1f4663bed5b0a446e2b153',
                                                     redirect_uri="http://localhost:8080",
                                                     scope='playlist-read-private'))

    user_id = user.me()
    playlists = list()

    for offset in range(0, 10000000, limit_step):

        response = user.user_playlists(user_id['id'], limit=limit_step, offset=offset)
        if len(response['items']) == 0:
            break
        for playlist in response['items']:
            if playlist['owner']['id'] == user_id['id'] and playlist['public'] == public_only:
                new_playlist = DetailedPlaylistModel(playlist_id=playlist['id'],
                                                     name=playlist['name'],
                                                     total_tracks=playlist['tracks']['total'],
                                                     )
                new_playlist.save()
                playlists.append(new_playlist)

    return playlists


def get_playlists_tracks(limit_step=100):
    user = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='8fffefe586fa4711ae28c0f0ea3c5084',
                                                     client_secret='10a514b5df1f4663bed5b0a446e2b153',
                                                     redirect_uri="http://localhost:8080",
                                                     scope='user-library-read'))
    playlists = get_user_playlists()

    for playlist in playlists:

        tracks = list()
        for offset in range(0, 10000000, limit_step):
            response = user.playlist_items(playlist.playlist_id, limit=limit_step, offset=offset)
            if len(response['items']) == 0:
                break
            for track in response['items']:
                added_at = datetime.strptime(track['added_at'], '%Y-%m-%dT%H:%M:%SZ')
                formatted_date = added_at.strftime('%d-%B-%Y, %H:%M')
                new_track = TrackModel(title=track['track']['name'],
                                       artist=', '.join([artist['name'] for artist in track['track']['artists']]),
                                       album=track['track']['album']['name'],
                                       added=formatted_date)
                new_track.save()
                tracks.append(new_track)

        playlist.tracks.add(*tracks)
        print('finished fetching tracks for playlist: ', playlist.name)

    return playlists


if __name__ == '__main__':
    playlists = get_playlists_tracks()

    pass
