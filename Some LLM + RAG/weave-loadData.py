import weaviate  # Make sure weaviate is imported
from weaviate import Client
import json
import requests

client = Client(
    url="http://localhost:8080/",
)

# Try deleting class if it exists
try:
    client.schema.delete_class("SimSearch")
except weaviate.exceptions.UnexpectedStatusCodeError as e:
    print(f"Error deleting class: {e}")
    print("Class 'SimSearch' not found, skipping deletion.")

# Define schema for the data we'll be using
class_obj = {
    "class": "SimSearch",
    "vectorizer": "text2vec-transformers"
}
client.schema.create_class(class_obj)

# Download data
url = 'http://localhost:8000/data.json'
resp = requests.get(url)
data = json.loads(resp.text)

# Send data to Weaviate to vectorize
with client.batch as batch:
    batch.batch_size = 100
    # Batch import all data
    for i, d in enumerate(data):
        print(f"\nImporting datum: {i}")

        properties = {
            "musicGenre": d["MusicGenre"],
            "songTitle": d["SongTitle"],
            "artist": d["Artist"],
        }
        print(f"Properties: {properties}")

        client.batch.add_data_object(properties, "SimSearch")

