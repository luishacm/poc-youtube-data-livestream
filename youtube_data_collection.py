import json
import requests


response = requests.get("https://youtube.googleapis.com/youtube/v3/videos?part=liveStreamingDetails,snippet,statistics,topicDetails&id=8q6un4-zz8Y&key=AIzaSyAkIqVg6rGifvYtlnCuQTP0f2eD-Bu5npA")

response_json = response.json()
pretty_json = json.dumps(response_json, indent=4)
print(pretty_json)