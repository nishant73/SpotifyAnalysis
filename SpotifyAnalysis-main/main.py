import json
import base64
from google.cloud import pubsub_v1
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def fetch_spotify_data(event, context):
    # Set up Spotify API credentials
    client_id = 'My-Id'  # Replace with your actual client ID
    client_secret = 'My-Secret'  # Replace with your actual client secret
    
    # Authenticate using client credentials
    credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=credentials)

    # Extract the Spotify URL from the event data
    if 'data' not in event:
        print("No data found in the event.")
        return
    
    # Decode the message data from base64
    spotify_url = json.loads(base64.b64decode(event['data']).decode('utf-8')).get("https://open.spotify.com/playlist/37i9dQZEVXbLZ52XmnySJg")
    if not spotify_url:
        print("No Spotify URL provided.")
        return

    # Use the full URL directly with Spotipy
    try:
        results = sp.track(spotify_url)  # Try to fetch track data
    except spotipy.exceptions.SpotifyException:
        try:
            results = sp.album(spotify_url)  # Try to fetch album data
        except spotipy.exceptions.SpotifyException:
            try:
                results = sp.artist(spotify_url)  # Try to fetch artist data
            except spotipy.exceptions.SpotifyException as e:
                print(f"Failed to fetch data for URL: {spotify_url}. Error: {e}")
                return

    # Publish the data to Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path('my-project-id', 'spotify-etl')  # Replace with your project ID and topic

    # Convert data to JSON string and publish
    publisher.publish(topic_path, json.dumps(results, default=str).encode('utf-8'))
    print("Data published to Pub/Sub successfully.")

