import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime
from .models import SongsLibrary


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
            tracks.append(SongsLibrary(id=count,
                                       title=track['track']['name'],
                                       artist=track['track']['artists'][0]['name'],
                                       added=formatted_date))
            print(f"finished fetching {count} tracks")

    # print(f"You have {count} saved songs!")
    return tracks