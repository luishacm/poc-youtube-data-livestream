from dotenv import load_dotenv
import requests
import pandas as pd
import os
from datetime import datetime
from typing import Dict, Any, List
import time

load_dotenv()
api_key: str = os.environ.get("YOUTUBE_API_KEY")

def organize_data(response_json: Dict[str, Any]) -> pd.DataFrame:
    """
    Organizes the JSON data from YouTube API into a DataFrame.

    Parameters:
    - response_json (Dict[str, Any]): The JSON response from YouTube API.

    Returns:
    - pd.DataFrame: A DataFrame containing organized data.
    """
    data = response_json["items"][0]
    snippet = data["snippet"]
    stats = data["statistics"]
    topics_details = data["topicDetails"]
    live_details = data["liveStreamingDetails"]

    organized_data = {
        "channel_title": [snippet.get("channelTitle")],
        "livestream_title": [snippet.get("title")],
        "live_id": [data.get("id")],
        "created_at": [snippet.get("publishedAt")],
        "current_date": [datetime.now().isoformat()],
        "concurrent_viewers_count": [live_details.get("concurrentViewers")],
        "like_count": [stats.get("likeCount")],
        "view_count": [stats.get("viewCount")],
        "topic_categories": [", ".join(topics_details.get("topicCategories", []))],
        "thumbnail__maxres_url": [snippet["thumbnails"]["maxres"].get("url")],
        "description": [snippet.get("description")]
    }
    df = pd.DataFrame.from_records(organized_data)

    return df


def get_channel_data(channel_ids: List[str], old_df: pd.DataFrame, excel_name: str) -> None:
    """
    Fetches and saves the channel data for multiple channel IDs.

    Parameters:
    - channel_ids (List[str]): List of channel IDs to fetch data for.

    """
    for channel_id in channel_ids:
        response = requests.get(f"https://youtube.googleapis.com/youtube/v3/videos?part=liveStreamingDetails,snippet,statistics,topicDetails&id={channel_id}&key={api_key}")
        response_json = response.json()
        df = organize_data(response_json)
        old_df = pd.concat([old_df, df], ignore_index=True)
    old_df.to_excel(f"{excel_name}.xlsx", index=False)

if __name__ == "__main__":
    excel_name = "channels_data"
    channel_ids_to_monitor = ["-gsnysgeWP4", "iYst4wufCgc", "jfKfPfyJRdk"]
    while True:
        df = pd.read_excel(f"{excel_name}.xlsx")
        get_channel_data(channel_ids_to_monitor, df, excel_name)
        time.sleep(60)