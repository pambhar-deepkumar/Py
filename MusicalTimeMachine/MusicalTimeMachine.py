import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

client_id = CLIENT_ID
client_secret = CLIENT_SECRET
base_url = "https://www.billboard.com/charts/hot-100/"

if __name__ == '__main__':
    # Scraping Billboard 100
    date = input("Which year do you want to travel to? Type the date in format YYYY-MM-DD: ")
    response = requests.get(base_url + date)
    scraped_data = BeautifulSoup(response.text, "html.parser")
    list_of_songs = [elem.text.strip() for elem in
                     scraped_data.find_all(name="h3", id="title-of-a-story", class_='a-no-trucate')]

    # Spotify Authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/callback",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
    )
    user_id = sp.current_user()["id"]
    print(f"Done with the authentication userid: {user_id}")

    print("Searching for the songs on Spotify...")
    # Searching Spotify for songs by title
    song_uris = []
    year = date.split("-")[0]
    for song in list_of_songs:
        result = sp.search(q=f"track:{song} year:{year}", type="track")
        try:
            uri = result["tracks"]["items"][0]["uri"]
            song_uris.append(uri)
        except IndexError:
            print(f"{song} doesn't exist in Spotify. Skipped.")
    print(f"Creating a new spotify playlist named: {date} Billboard 100")

    # Creating a new private playlist in Spotify
    playlist_id = sp.user_playlist_create(user_id, name=date+" Billboard 100", public=False)['id']
    print(f"Adding songs to playlist : {date} Billboard 100....")

    # Adding songs found into the new playlist
    sp.playlist_add_items(playlist_id=playlist_id,items=song_uris)
    print(f"Done ! Enjoy the songs :)")