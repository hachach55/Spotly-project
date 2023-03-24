import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from .models import TrackModel


def get_all_saved_tracks(limit_step=50):
    user = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='8fffefe586fa4711ae28c0f0ea3c5084',
                                                     client_secret='10a514b5df1f4663bed5b0a446e2b153',
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
            # tracks.append({'name': track['track']['name'],
            #                'artist': track['track']['artists'][0]['name'],
            #                'added_at': track['added_at']})
            count += 1
            added_at = datetime.strptime(track['added_at'], '%Y-%m-%dT%H:%M:%SZ')
            formatted_date = added_at.strftime('%d-%B-%Y, %H:%M')
            tracks.append(TrackModel(id=count,
                                     title=track['track']['name'],
                                     artist=track['track']['artists'][0]['name'],
                                     album=track['track']['album']['name'],
                                     added=formatted_date))
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

if __name__ == '__main__':
    saved_tracks = get_all_saved_tracks()

    pass