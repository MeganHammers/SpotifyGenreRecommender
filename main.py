#authorization
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import statistics

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

#sample artist URIs
fob_uri = 'spotify:artist:4UXqAaa6dQYAk18Lv7PEgX'
lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
beethoven_uri = 'spotify:artist:2wOqMjp9TyABvtHdOSOTUS'

#User music input - what if they don't pick an artist?
artist_query = input("What's an artist that you like?")
search_res = spotify.search(q=artist_query,type='artist')['artists']['items']
artist_uri = search_res[0]['uri']

#Genre input
seed_genres = {'acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass',
               'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill',
               'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house',
               'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic',
               'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove',
               'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays',
               'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance',
               'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal',
               'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera',
               'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop',
               'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton',
               'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo',
               'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish',
               'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish',
               'work-out', 'world-music'}

genre_pick = '?'

while genre_pick not in seed_genres:
    print("Here's a list of genres to explore!")
    print(seed_genres)
    genre_pick = input("Type your choice here: ")
print("Good choices! Lemme serve up some tracks for you!")
print()

#Finds features of user inputted artist
top_ten = spotify.artist_top_tracks(artist_uri)
danciness_list = []
energy_list = []
valence_list = []
tempo_list = []
mode_list = []

for track in top_ten['tracks'][:10]:
    features = spotify.audio_features(track['id'])[0] #why does this give me a list with one item and a dict inside?
    danciness_list.append(features['danceability'])
    energy_list.append(features['energy'])
    valence_list.append(features['valence'])
    tempo_list.append(features['tempo'])
    mode_list.append(features['mode'])
    #print()

dev_scale = 1.25 #multiplier for stdev. 1.0 only returns 1 result for some artists/genres. Needs fine tuning. Expand to user input
danciness_avg, danciness_stdev = statistics.mean(danciness_list), dev_scale * statistics.stdev(danciness_list)
energy_avg,    energy_stdev    = statistics.mean(energy_list),    dev_scale * statistics.stdev(energy_list)
valence_avg,   valence_stdev   = statistics.mean(valence_list),   dev_scale * statistics.stdev(valence_list)
tempo_avg,     tempo_stdev     = statistics.mean(tempo_list),     dev_scale * statistics.stdev(tempo_list)

#Fetching reccs based on user choices and printing them
reccs = spotify.recommendations(seed_genres=[genre_pick],
                                min_danceability = danciness_avg - danciness_stdev, max_danceability = danciness_avg + danciness_stdev,
                                min_energy       = energy_avg    - energy_stdev,    max_energy       = energy_avg    + energy_stdev,
                                min_valence      = valence_avg   - valence_stdev,   max_valence      = valence_avg   + valence_stdev,
                                min_tempo        = tempo_avg     - tempo_stdev,     max_tempo        = tempo_avg     + tempo_stdev,
                                limit=10)['tracks']

for track in reccs:
    features = spotify.audio_features(track['id'])[0] #why does this give me a list with one item and a dict inside?
    print(track['name'] + ' - ' + str(track['artists'][0]['name']))
    print('audio     : ' + str(track['external_urls']['spotify']))
    print()
