import json
import base64
from google.cloud import storage
from datetime import datetime
import functions_framework

@functions_framework.cloud_event
def process_spotify_data(event, context):
    print(f"Received event: {event}")  # Log the received event
    
    try:
        # Decode the Pub/Sub message
        data = json.loads(base64.b64decode(event['data']).decode('utf-8'))
    except Exception as e:
        print(f"Error decoding message: {e}")
        return
    
    # Initialize GCS client
    client = storage.Client()
    processed_bucket_name = 'spotify-etl-1'
    
    try:
        processed_bucket = client.bucket(processed_bucket_name)
    except Exception as e:
        print(f"Error accessing bucket: {e}")
        return

    # Process data
    processed_data = process_data(data)  # Extract album information

    # Save processed data to GCS bucket
    timestamp = datetime.utcnow().isoformat().replace(":", "-").replace(".", "-")
    processed_blob_name = f'processed_spotify_data_{timestamp}.json'
    processed_blob = processed_bucket.blob(processed_blob_name)

    try:
        processed_blob.upload_from_string(json.dumps(processed_data))
        print(f"Processed data saved to {processed_blob_name}.")
    except Exception as e:
        print(f"Error uploading to GCS: {e}")

def process_data(data):
    albums_info = []
    
    # Extract album information from the JSON structure
    for item in data.get('items', []):
        track = item.get('track')
        if track and 'album' in track:
            album = track['album']
            album_info = {
                'album_id': album.get('id'),
                'album_name': album.get('name'),
                'release_date': album.get('release_date'),
                'total_tracks': album.get('total_tracks'),
                'artists': [{'name': artist['name'], 'id': artist['id']} for artist in album.get('artists', [])],
                'external_url': album.get('external_urls', {}).get('spotify'),
                'images': album.get('images', [])
            }
            albums_info.append(album_info)
    
    return albums_info  # Return the extracted album information
